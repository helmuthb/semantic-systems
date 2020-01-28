import csv

"""
This script creates RDFized countries from the stackoverflow survey results from 2018, which is in csv format.
"""

COUNTRY_BASE = '\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">\n\t\t<rdf:type rdf:resource="http://schema.org/Country"/>\n\t\t<schema:name rdf:datatype="http://www.w3.org/2001/XMLSchema#string">%s</schema:name>\n\t</owl:NamedIndividual>'

countries = []

"""
Check the mappings.md file for the mapping rules
"""
def map_country(country):
    if country == 'Iran, Islamic Republic of...':
        return 'Iran'
    return country

def write_countries_to_file():
    with open('../generated/generated_countries.xml', mode='w') as f:
        f.write('\t<!-- STACKOVERFLOW: COUNTRIES -->\n')
        f.write('\n')
        for c in countries:    
            country = map_country(c)
            f.write(COUNTRY_BASE % (country.replace(' ', '_'), c) + '\n')
            f.write('\n')
            f.write('\n')

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            if row[1] not in countries:
                countries.append(row[1])
        
        # sort all first
        countries.sort()
    
        write_countries_to_file()

if __name__ == "__main__":
    main()
    