#! /usr/bin/env python

import pandas as pd
import math

# read in repositories with fork counts and issue counts
df_repos = pd.read_csv('repos_issues.csv')

# get repository name
df_repos['name'] = df_repos.url.str.replace(
       'https://api.github.com/repos/', '')

rdf_header = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
@prefix schema: <http://schema.org/>
@prefix group1: <http://www.semanticweb.org/sws/ws2019/group1#>
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>
"""

# encode quotes in text
def quote(t):
    if t is float and math.isnan(t):
        t = ''
    return str(t).replace('"', '\\"')

# get language
def get_lang(r):
    lang = quote(r['language'])
    if lang == 'C++':
        lang = 'Cplusplus'
    if lang == 'C#':
        lang = 'Csharp'
    if lang == 'F#':
        lang = 'Fsharp'
    if lang == 'Emacs Lisp' or lang == 'Common Lisp':
        lang = 'Lisp'
    if lang == 'Jupyter Notebook':
        lang = 'Python'
    if lang == 'Objective-C++':
        lang = 'Objective-Cplusplus'
    if lang == 'Web Ontology Language':
        lang = 'OWL'
    # replace all ' ' with '-'
    lang = lang.replace(' ', '-')
    # replace all '\'' with '-'
    lang = lang.replace('\'', '-')
    return lang

# write block for one repo
def write_block(f, r):
    # print(r)
    lang = get_lang(r)
    name = quote(r['name'])
    description = quote(r['description'])
    f.write("\n")
    f.write("<" + r['url'] + "> rdf:type group1:GitHubRepository ;\n")
    f.write("    group1:isDevelopedIn group1:" + lang + " ;\n")
    f.write("    schema:name \"" + name + "\"^^xsd:string ;\n")
    # f.write("    group1:description \"" + description + "\"^^xsd:string ;\n")
    f.write("    group1:issues \"" + str(r.issues) + "\"^^xsd:integer ;\n")
    f.write("    group1:popularity \"" + str(r.forks) + "\"^^xsd:integer .\n")

with open('repos.ttl', 'w') as rdf_file:
    # create header
    rdf_file.write(rdf_header)
    # loop through data
    for repo in df_repos.iterrows():
        write_block(rdf_file, repo[1])
