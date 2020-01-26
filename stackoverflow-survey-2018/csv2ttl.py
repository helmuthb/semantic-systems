import csv
import urllib.parse
from csv2individuals import map_dev_role

"""
This script RDFizes the stackoverflow survey results from 2018 (in csv format).
"""

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

def print_prefix():
    print("""@prefix group1: <http://www.semanticweb.org/sws/ws2019/group1#> .\n@prefix dbpedia: <http://www.dbpedia.org/resource/> .\n""")

def print_home_location(name, raw):
    print(user(name) + ' ' + group1('homeLocation') + ' ' + dbpedia(raw.replace(' ', '_')) + ' ;')

def print_employee_role(raw):
    print('\t<!-- TODO: remove or change employment status -->')
    print('\t' + group1('hasRole') + ' ' + group1('"' + raw + '"') + ' ;')

def print_developer_roles(raw):
    developer_roles = get_developer_roles(raw)
    print_dev_roles = ''
    for i, dev_role in enumerate(developer_roles):
        mapped_dev_role = map_dev_role(dev_role)
        print_dev_roles += group1(mapped_dev_role.replace(' ', '_'))
        if i < len(developer_roles)-1:
            print_dev_roles += ', '
    print('\t' + group1('hasDeveloperRole') + ' ' + print_dev_roles + ' ;')

def print_experience_years(raw):
    print('\t<!-- TODO: rename experience range values (e.g. no encoding but IDs) -->')
    print('\t' + group1('hasExperienceRange') + ' ' + group1(urllib.parse.quote(raw)) + ' ;')

def print_is_searching_job(raw):
    print('\t' + group1('isSearchingJob') + ' ' + str(is_searching_job(raw)).lower() + ' ;')

def print_salary(raw):
    print('\t' + group1('salary') + ' "' + raw + '"^^xsd:integer ;')

def print_programming_languages(raw):
    programming_languages = get_programming_languages(raw)
    print_prog_langs = ''
    for i, lang in enumerate(programming_languages):
        print_prog_langs += group1(lang)
        if i < len(programming_languages)-1:
            print_prog_langs += ', '
    print('\t' + group1('devlopsIn') + ' ' + group1(lang) + ' ;')

def print_gender(raw):
    print('\t' + group1('gender') + ' ' + group1(get_gender(raw)) + ' ;')

def print_age(raw):
    print('\t<!-- TOOD: get mapping to age range -->')
    print('\t' + group1('hasAgeRange') + ' ' + group1(urllib.parse.quote(raw)) + ' .')

def main():
    with open('./edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        print_prefix()
    
        for row in csv_reader:
            name = row[0]
        
            print_home_location(name, row[1])
            print_employee_role(row[2])
            print_developer_roles(row[3])
            # do we need this?
            print_experience_years(row[4])
            print_is_searching_job(row[5])
            print_salary(row[9])
            print_programming_languages(row[11])
            print_gender(row[12])
            print_age(row[13])
            print()
            print()

if __name__ == "__main__":
    main()