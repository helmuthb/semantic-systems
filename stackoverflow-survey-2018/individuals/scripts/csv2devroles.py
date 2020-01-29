import csv

"""
This script creates RDFized dev roles from the stackoverflow survey results from 2018, which is in csv format.
"""

EMPLOYEE_ROLE_BASE = '\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">\n\t\t<rdf:type rdf:resource="https://schema.org/EmployeeRole"/>\n\t</owl:NamedIndividual>'

dev_roles = []

"""
Check the mappings.md file for the mapping rules
"""
def map_dev_role(role):
    if role == 'C-suite executive (CEO, CTO, etc.)' or role == 'Product manager' or role == 'Educator or academic researcher':
        return 'Manager'
    if role == 'Data scientist or machine learning specialist':
        return 'Data Scientist'
    if role == 'Database administrator':
        return 'DBA or Database Engineer'
    if role == 'Back-end developer' \
        or role == 'Front-end developer' \
        or role == 'Full-stack developer' \
        or role == 'Desktop or enterprise applications developer' \
        or role == 'DevOps specialist' \
        or role == 'Embedded applications or devices developer' \
        or role == 'Engineering manager' \
        or role == 'Game or graphics developer' \
        or role == 'Mobile developer' \
        or role == 'QA or test developer':
        return 'Software Engineer'
    if role == 'Educator or academic researcher':
        return 'Research Scientist'
    return role

def parse_dev_roles(raw):
    tmp_dev_roles = raw.split(';')
    for role in tmp_dev_roles:
        if role not in dev_roles:
            dev_roles.append(role)

def write_dev_roles_to_file():
    with open('../generated/generated_dev_roles.xml', mode='w') as f:
        f.write('\t<!-- STACKOVERFLOW: DEVELOPER ROLES -->\n')
        f.write('\n')
        for role in dev_roles:
            dev_role = map_dev_role(role)
            f.write(EMPLOYEE_ROLE_BASE % (dev_role.replace(' ', '_')) + '\n')
            f.write('\n')
            f.write('\n')

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            parse_dev_roles(row[2])
        
        # sort all first
        dev_roles.sort()
    
        write_dev_roles_to_file()

if __name__ == "__main__":
    main()
    