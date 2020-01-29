import csv
import urllib.parse

"""
This script creates RDFized age ranges from the stackoverflow survey results from 2018, which is in csv format.
"""

AGE_RANGE_BASE = """\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">
        <rdf:type rdf:resource="http://www.semanticweb.org/sws/ws2019/group1#AgeRange"/>
        <minAge rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">%d</minAge>
        <maxAge rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">%d</maxAge>
    </owl:NamedIndividual>"""

AGE_RANGE_NO_MAX_BASE = """\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">
        <rdf:type rdf:resource="http://www.semanticweb.org/sws/ws2019/group1#AgeRange"/>
        <minAge rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">%d</minAge>
    </owl:NamedIndividual>"""

age_ranges = []

"""
Check the mappings.md file for the mapping rules
"""
def parse_age_range(raw):
    if raw == 'Under 18 years old':
        return { 'id': raw, 'min': 0, 'max': 17 }
    if raw == '65 years or older':
        return { 'id': raw, 'min': 65 }
    range_only = raw[:-10]
    min_max = range_only.split(' - ')
    return { 'id': range_only, 'min': int(min_max[0]), 'max': int(min_max[1]) }

def write_age_ranges_to_file():
    with open('../generated/generated_age_ranges.xml', mode='w') as f:
        f.write('\t<!-- STACKOVERFLOW: AGE RANGES -->\n')
        f.write('\n')
        for ar in age_ranges:
            if 'max' not in ar:
                f.write(AGE_RANGE_NO_MAX_BASE % (urllib.parse.quote(ar['id']), ar['min']) + '\n')
            else:
                f.write(AGE_RANGE_BASE % (urllib.parse.quote(ar['id']), ar['min'], ar['max']) + '\n')
            f.write('\n')
            f.write('\n')

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            if parse_age_range(row[8]) not in age_ranges:
                age_ranges.append(parse_age_range(row[8]))
    
        write_age_ranges_to_file()

if __name__ == "__main__":
    main()
    