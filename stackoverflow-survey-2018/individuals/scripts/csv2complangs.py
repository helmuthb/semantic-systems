import csv

"""
This script creates RDFized computer languages from the stackoverflow survey results from 2018, which is in csv format.
"""

COMPUTER_LANGUAGES_BASE = '\t<owl:NamedIndividual rdf:about="http://www.semanticweb.org/sws/ws2019/group1#%s">\n\t\t<rdf:type rdf:resource="https://schema.org/ComputerLanguage"/>\n\t</owl:NamedIndividual>'

comp_langs = []

"""
Check the mappings.md file for the mapping rules
"""
def map_computer_language(computer_language):
    if computer_language == 'Bash/Shell':
        return 'Bash'
    return computer_language

def parse_computer_languages(raw):
    tmp_comp_langs = raw.split(';')
    for comp_lang in tmp_comp_langs:
        if comp_lang not in comp_langs:
            comp_langs.append(comp_lang)

def print_comp_langs():
    for lang in comp_langs:
        comp_lang = map_computer_language(lang)
        print(COMPUTER_LANGUAGES_BASE % (comp_lang.replace(' ', '_')))
        print()
        print()

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
    
        print('\t<!-- STACKOVERFLOW: COMPUTER LANGUAGES -->')
        print()
        for row in csv_reader:
            parse_computer_languages(row[6])
        
        # sort all first
        comp_langs.sort()
    
        print_comp_langs()

if __name__ == "__main__":
    main()
    