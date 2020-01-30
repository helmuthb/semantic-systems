import csv
import urllib.parse
from csv2devroles import map_dev_role
from csv2complangs import map_computer_language
from csv2genders import map_gender
from csv2countries import map_country
from csv2ages import parse_age_range

"""
This script RDFizes the stackoverflow survey results from 2018 (in csv format).
"""

PREFIXES = [
    {
        'abbr': 'group1',
        'url': 'http://www.semanticweb.org/sws/ws2019/group1#'
    },
    {
        'abbr': 'schema',
        'url': 'http://schema.org/'
    },
    {
        'abbr': 'dbpedia',
        'url': 'http://dbpedia.org/resource/'
    },
    {
        'abbr': 'rdf',
        'url': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    },
    {
        'abbr': 'xsd',
        'url': 'http://www.w3.org/2001/XMLSchema#'
    }
]

def group1(string):
    return 'group1:' + string

def schema(string):
    return 'schema:' + string

def dbpedia(string):
    return 'dbpedia:' + string

def rdf(string):
    return 'rdf:' + string

def user(name):
    return group1(name)

def print_type_developer(f):
    f.write('\t' + rdf('type') + ' ' + group1('Developer') + ' ;\n')

def is_searching_job(raw):
    if 'not' in raw:
        return False
    return True

def print_prefix(f):
    for prefix in PREFIXES:
        f.write('@prefix ' + prefix['abbr'] + ': <' + prefix['url'] + '> .\n')
    f.write('\n')

def print_home_location(f, name, raw):
    f.write(user(name) + ' ' + schema('homeLocation') + ' ' + dbpedia(map_country(raw).replace(' ', '_')) + ' ;\n')

def print_developer_roles(f, raw):
    developer_roles = raw.split(';')
    print_dev_roles = ''
    roles_used = []
    for i, dev_role in enumerate(developer_roles):
        mapped_dev_role = map_dev_role(dev_role)
        if mapped_dev_role in roles_used:
            continue
        roles_used.append(mapped_dev_role)
        print_dev_roles += (group1(mapped_dev_role.replace(' ', '_')) + ', ')
    if print_dev_roles.endswith(', '):
        print_dev_roles = print_dev_roles[:-2]
    f.write('\t' + group1('hasRole') + ' ' + print_dev_roles + ' ;\n')

def print_experience_years(f, raw):
    f.write('\t' + group1('hasExperienceRange') + ' ' + group1(urllib.parse.quote(raw)) + ' ;\n')

def print_is_searching_job(f, raw):
    f.write('\t' + group1('isSearchingJob') + ' ' + str(is_searching_job(raw)).lower() + ' ;\n')

def print_salary(f, raw):
    f.write('\t' + group1('salary') + ' "' + raw + '"^^xsd:integer ;\n')

def print_computer_languages(f, raw):
    computer_languages = raw.split(';')
    print_prog_langs = ''
    for i, lang in enumerate(computer_languages):
        mapped_computer_language = map_computer_language(lang)
        print_prog_langs += group1(mapped_computer_language.replace(' ', '_'))
        if i < len(computer_languages)-1:
            print_prog_langs += ', '
    f.write('\t' + group1('developsIn') + ' ' + print_prog_langs + ' ;\n')

def print_gender(f, raw):
    f.write('\t' + schema('gender') + ' ' + group1(map_gender(raw)) + ' ;\n')

def print_age(f, raw):
    f.write('\t' + group1('hasAgeRange') + ' ' + group1(parse_age_range(raw)['id'].replace(' ', '')) + ' .\n')

def main():
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        with open('../generated/stackoverflow_individuals.ttl', mode='w') as f:
            print_prefix(f)
    
            for i, row in enumerate(csv_reader):
                if i == 0:
                    continue
                name = row[0]
        
                # HOME LOCATION MUST BE FIRST LINE !!
                print_home_location(f, name, row[1])
                print_type_developer(f)
                print_developer_roles(f, row[2])
                #print_experience_years(f, row[3])
                #print_is_searching_job(f, row[4])
                print_salary(f, row[5])
                print_computer_languages(f, row[6])
                print_gender(f, row[7])
                print_age(f, row[8])
                f.write('\n')
                f.write('\n')

if __name__ == "__main__":
    main()