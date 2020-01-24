import csv
import urllib.parse

def group1(string):
    return 'group1:' + string

def schema(string):
    return 'schema:' + string

def dbpedia(string):
    return 'dbpedia:' + string

def user(name):
    return group1(name)

def get_developer_roles(raw):
    return raw.split(';')

def is_searching_job(raw):
    if 'not' in raw:
        return False
    return True

def get_programming_languages(raw):
    return raw.split(';')

def get_gender(raw):
    if raw == 'Female':
        return 'Female'
    if raw == 'Male':
        return 'Male'
    return 'Other'

with open('./edited_survey_results_public.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    print("""@prefix group1: <http://www.semanticweb.org/sws/ws2019/group1#>\n@prefix dbpedia: <http://www.dbpedia.org/resource/>\n""")
    
    for row in csv_reader:
        name = row[0]

        # home location
        print(user(name) + ' ' + group1('homeLocation') + ' ' + dbpedia(row[1].replace(' ', '_')))

        # employee role
        print('<!-- TODO: remove or change employment status -->')
        print(user(name) + ' ' + group1('hasRole') + ' ' + group1('"' + row[2] + '"'))

        # developer roles
        developer_roles = get_developer_roles(row[3])
        for dev_role in developer_roles:
            print(user(name) + ' ' + group1('hasDeveloperRole') + ' ' + group1(urllib.parse.quote(dev_role)))

        # experience in years
        print('<!-- TODO: rename experience ranges -->')
        print(user(name) + ' ' + group1('hasExperienceRange') + ' ' + group1(urllib.parse.quote(row[4])))

        # searching job
        if is_searching_job(row[5]):
            print(user(name) + ' ' + group1('isSearchingJob') + ' "YES"')
        else:
            print(user(name) + ' ' + group1('isSearchingJob') + ' "NO"')

        # salary
        print(user(name) + ' ' + group1('salary') + ' "' + row[9] + '"')

        # programming languages
        programming_languages = get_programming_languages(row[11])
        for lang in programming_languages:
            print(user(name) + ' ' + group1('developsIn') + ' ' + group1(lang))

        # gender
        print(user(name) + ' ' + group1('gender') + ' ' + group1(get_gender(row[12])))

        # age
        print('<!-- TOOD: get mapping to age range -->')
        print(user(name) + ' ' + group1('hasAgeRange') + ' ' + group1(urllib.parse.quote(row[13])))

        print()
        print()
