import csv

"""
This script creates RDFized individuals the stackoverflow survey results from 2018, which is in csv format.
"""

EMPLOYEE_ROLE_BASE = '\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">\n\t\t<rdf:type rdf:resource="https://schema.org/EmployeeRole"/>\n\t</owl:NamedIndividual>'

dev_roles = []

"""
Check the mappings.md file for the mapping rules
"""
def map_dev_role(role):
    if role.endswith(' (CEO, CTO, etc.)'):
        return role[:-17]
    if role.startswith('Data scientist'):
        return 'Data Scientist'
    if role == 'Database administrator':
        return 'DBA or Database Engineer'
    if role == 'Product manager':
        return 'Product or Project Manager'
    return role

with open('./edited_survey_results_public.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    for row in csv_reader:
        tmp_dev_roles = row[3].split(';')
        for role in tmp_dev_roles:
            if role not in dev_roles:
                dev_roles.append(role)
    
    dev_roles.sort()
    for role in dev_roles:
        dev_role = map_dev_role(role)
        print(EMPLOYEE_ROLE_BASE % (dev_role.replace(' ', '_')))
        print()
        print()
    