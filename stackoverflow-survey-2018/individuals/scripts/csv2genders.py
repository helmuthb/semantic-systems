import csv

"""
This script creates RDFized genders from the stackoverflow survey results from 2018, which is in csv format.
"""

GENDER_BASE = '\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">\n\t\t<rdf:type rdf:resource="http://www.semanticweb.org/sws/ws2019/group1#Gender"/>\n\t\t<schema:name rdf:datatype="http://www.w3.org/2001/XMLSchema#string">%s</schema:name>\n\t</owl:NamedIndividual>'

genders = []

"""
Check the mappings.md file for the mapping rules
"""
def map_gender(raw):
    if raw == 'Female':
        return 'Female'
    if raw == 'Male':
        return 'Male'
    return 'Other'

def write_genders_to_file():
    with open('../generated/generated_genders.xml', mode='w') as f:
        f.write('\t<!-- STACKOVERFLOW: GENDERS -->\n')
        f.write('\n')
        for g in genders:
            f.write(GENDER_BASE % (g.replace(' ', '_'), g) + '\n')
            f.write('\n')
            f.write('\n')

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            if map_gender(row[7]) not in genders:
                genders.append(map_gender(row[7]))
        
        # sort all first
        genders.sort()
    
        write_genders_to_file()

if __name__ == "__main__":
    main()
    