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
    if computer_language == 'C++':
        return 'Cplusplus'
    if computer_language == 'C#':
        return 'Csharp'
    if computer_language == 'F#':
        return 'Fsharp'
    if computer_language == 'Delphi/Object Pascal':
        return 'Delphi ObjectPascal'
    return computer_language

def parse_computer_languages(raw):
    tmp_comp_langs = raw.split(';')
    for comp_lang in tmp_comp_langs:
        if comp_lang not in comp_langs:
            comp_langs.append(comp_lang)

def write_comp_langs_to_file():
    with open('../generated/generated_comp_langs.xml', mode='w') as f:
        f.write('\t<!-- STACKOVERFLOW: COMPUTER LANGUAGES -->\n')
        f.write('\n')
        for lang in comp_langs:
            comp_lang = map_computer_language(lang)
            f.write(COMPUTER_LANGUAGES_BASE % (comp_lang.replace(' ', '_')) + '\n')
            f.write('\n')
            f.write('\n')

def main():    
    with open('../../edited_survey_results_public.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            parse_computer_languages(row[6])
        
        # sort all first
        comp_langs.sort()
    
        write_comp_langs_to_file()

if __name__ == "__main__":
    main()
    