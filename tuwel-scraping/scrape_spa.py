from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from contextlib import closing
import requests
from requests.exceptions import RequestException
import re
from rdflib import Graph
import fastnumbers as fn
from rdflib.namespace import RDF, FOAF, XSD
from rdflib import URIRef, BNode, Literal, Namespace




class ClassicalScraper:
    def __init__(self):
        self.url = ''

    def simple_get(self, url):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.
        """
        try:
            with closing(requests.get(url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None


    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200 
                and content_type is not None 
                and content_type.find('html') > -1)


    def log_error(self, e):
        """
        It is always a good idea to log errors. 
        This function just prints them, but you can
        make it do anything.
        """
        print(e)

    # def get_academic_programs(self, url):
    #     """
    #     Downloads the page and extracts the links to the academic programs
    #     """
    #     response = self.simple_get(url)

    #     if response is not None:
    #         html = BeautifulSoup(response, 'html.parser')
    #         print(html)
    #         # for a in html.select('a'):
    #         #     print(a)

    #             # if a.link.find('https://tiss.tuwien.ac.at/curriculum/public/curriculum.xhtml?key=') > -1:
    #             #     return (a.text, a.link)
    #     else:
    #         # Raise an exception if we failed to get any data from the url
    #         raise Exception('Error retrieving contents at {}'.format(url))

class SpaScraper(webdriver.Chrome):
    regex_python = r'\Wpython\W'
    regex_java = r'\Wjava\W'
    regex_haskell = r'\Whaskell\W'
    regex_r = r'\WR\W'
    regex_bash = r'\Wbash\W'
    regex_c = r'\Wc\W'
    regex_javascript = r'\Wjavascript\W'
    regex_sql = r'\Wsql\W'
    regex_matlab = r'\Wmatlab\W'
    regex_typescript = r'\Wtypescript\W'
    graph = Graph()
    namespace_group1 = Namespace('http://www.semanticweb.org/sws/ws2019/group1#')
    namespace_schema = Namespace('http://schema.org/')



    def __init__(self, addr, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument('lang=en')
        self.browser = super(SpaScraper, self).__init__(options=options) #*args, **kwargs)
        # self.browser = webdriver.Chrome(options=options)
        self.implicitly_wait(6)
        self.get(addr)


    def find_data_science_and_click(self):
        elem = browser.find_element_by_id('contentInner')
        innerHtml = elem.get_attribute("innerHTML")
        # get data science curriculum
        data_science = None
        for a in elem.find_elements_by_tag_name('a'):
            if (a.get_attribute('innerHTML').strip() == "Master programme Data Science"):
                data_science = (a.get_attribute('innerHTML').strip(), a.get_attribute('href'))
                a.click()
                break


    def extract_title(self, elem):
        """
        Extract title from course page.
        """
        title = elem.find_elements_by_tag_name('h1') # [0].get_attribute('innerHtml')
        result = re.match(r'\d+\.\d+ (.*)', title[0].text)
        if result != None:
            if result.group(1) != None:
                title = result.group(1)
                # print(title)
            return title
        else:
            return ''

    def extract_subtitle(self, elem):
        """
        Extract subtitle from course page.
        """
        sub_title = elem.find_elements_by_id('subHeader') # [0].get_attribute('innerHtml')
        text = sub_title[0].text
        return text

    def extract_lecturers(self, elem):
        """
        Extract lecturers as tuples (name, anchor). Anchor is None if URI not available.
        """
        # h2 = innerHtml.find_elements_by_tag_name('h2')
        result = []
        lecturers = []
        lecturers_html = elem.find_element_by_xpath("//h2[.='Lecturers']/following-sibling::ul")
        for lecturer in lecturers_html.find_elements_by_tag_name('li'):
            lecturers.append(lecturer.text)
        for lecturer in lecturers:
            try:
                # anchor = elem.find_element_by_xpath("//a[text()='{}']".format(lecturer))
                anchor = browser.find_element_by_link_text(lecturer)
                # print(anchor.get_attribute('href'))
                result.append((lecturer, anchor.get_attribute('href')))
            except Exception as e:
                print(e)
                result.append((lecturer, None))
        return result


    def extract_course_id(self, elem):
        """
        Extract course id from title.
        """
        course_id = 'no course id'
        title = elem.find_elements_by_tag_name('h1')
        result = re.match(r'(\d+\.\d+) .*', title[0].text)
        if result != None:
            if result.group(1) != None:
                course_id = result.group(1)
                # print(course_id)
            return course_id
        else:
            return course_id


    def find_language(self, html, language_regex):
        """
        Check if course description contains language.
        """
        result = re.search(language_regex, html, re.IGNORECASE)
        if result != None:
            # for match in result.regs:
                # print(html[match[0]: match[1]])
            return len(result.regs) > 0
        else:
            return False


    def extract_ects(self, sub_title):
        """
        Extract ECTS from subtitle.
        """
        result = -1
        ects = re.search(r'(\d+\W\d+)EC', sub_title)
        if ects != None:
            if ects.group(1) != None:
                tmp = fn.fast_float(ects.group(1), default=-1)
                if tmp > -1:
                    result = tmp
        return result


    def append_lecture(self, graph, url, title, sub_title, course_id, ects, lecturers, contains_python, contains_haskell, contains_java, contains_r):
        """
        Append lecture to graph.
        """
        lecture_uri = URIRef(url)
        # create lecture
        graph.add( (lecture_uri, RDF.type, SpaScraper.namespace_group1['TU-Lecture'] ) )
        graph.add( (lecture_uri, SpaScraper.namespace_schema['name'], Literal(title)) )
        graph.add( (lecture_uri, SpaScraper.namespace_group1['description'], Literal(sub_title)) )
        graph.add( (lecture_uri, SpaScraper.namespace_group1['courseId'], Literal(course_id)) )
        graph.add( (lecture_uri, SpaScraper.namespace_group1['ects'], Literal(ects, datatype=XSD.decimal)) )

        # add lecturers
        if lecturers != None:
            for lecturer in lecturers:
                lecturer_id = URIRef("http://www.semanticweb.org/sws/ws2019/group1#" + lecturer[0].replace(' ', '_').replace(',', ''))
                lecturer_name = Literal(lecturer[0])
                graph.add( (lecturer_id, RDF.type, SpaScraper.namespace_group1['Lecturer']) )
                graph.add( (lecturer_id, SpaScraper.namespace_schema['name'], lecturer_name) )
                graph.add( (lecture_uri, SpaScraper.namespace_group1['instructor'], lecturer_id) )
                if lecturer[1] != None:
                    lecturer_uri = URIRef(lecturer[1])
                    graph.add( (lecturer_id, SpaScraper.namespace_schema['URL'], lecturer_uri) )

        # add language
        if contains_python:
            graph.add( (lecture_uri, SpaScraper.namespace_group1['dealsWith'], SpaScraper.namespace_group1['Python'] ) )
        if contains_haskell:
            graph.add( (lecture_uri, SpaScraper.namespace_group1['dealsWith'], SpaScraper.namespace_group1['Haskell'] ) )
        if contains_java:
            graph.add( (lecture_uri, SpaScraper.namespace_group1['dealsWith'], SpaScraper.namespace_group1['Java'] ) )
        if contains_r:
            graph.add( (lecture_uri, SpaScraper.namespace_group1['dealsWith'], SpaScraper.namespace_group1['R'] ) )

        return graph


if __name__ == "__main__":
    try:
        browser = SpaScraper('https://tiss.tuwien.ac.at/curriculum/studyCodes.xhtml?locale=en')
        WebDriverWait(browser,10).until(ExpectedConditions.visibility_of_element_located((By.ID, "contentInner")))
        browser.find_data_science_and_click()

        WebDriverWait(browser, 10).until(ExpectedConditions.visibility_of_element_located((By.ID, 'contentInner')))
        elem = browser.find_element_by_id('j_id_2e:nodeTable_data')
        innerHtml = elem.get_attribute("innerHTML")
        # create list of courses
        course_list = []
        for div in elem.find_elements_by_class_name('courseTitle'):
            for a in div.find_elements_by_tag_name('a'):
                course_list.append((a.get_attribute('innerHTML').strip(), a.get_attribute('href')))
        # extract content for each course
        counter = 1000
        for tup in course_list:
            browser.get(tup[1])
            WebDriverWait(browser, 10).until(ExpectedConditions.visibility_of_element_located((By.ID, 'contentInner')))
            elem = browser.find_element_by_id('contentInner')
            innerHtml = elem.get_attribute("innerHTML")
            # print(innerHtml)
            title = browser.extract_title(elem)
            sub_title = browser.extract_subtitle(elem)
            course_id = browser.extract_course_id(elem)
            ects = browser.extract_ects(sub_title)
            lecturers = browser.extract_lecturers(elem)
            contains_python = browser.find_language(innerHtml, SpaScraper.regex_python)
            contains_haskell = browser.find_language(innerHtml, SpaScraper.regex_haskell)
            contains_java = browser.find_language(innerHtml, SpaScraper.regex_java)
            contains_r = browser.find_language(innerHtml, SpaScraper.regex_r)
            SpaScraper.graph = browser.append_lecture(SpaScraper.graph, tup[1], title, sub_title, course_id, ects, lecturers, contains_python, contains_haskell, contains_java, contains_r)
            
            counter -= 1
            if counter < 0:
                break
        # print(SpaScraper.graph.serialize(format='turtle'))
        SpaScraper.graph.serialize(destination='tuwel-data-science.ttl', format='turtle')

    except Exception as e:
        print(e)
    finally:
        browser.quit()