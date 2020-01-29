# MAPPINGS:





## General

Instead of url-encoding the roles, just replace every space (' ') with an underscore ('\_').





## ID:

##### STACKOVERFLOW:

- prepend 'S' on IDs (i.e. "Respondent" field)





## Salary:

##### STACKOVERFLOW:

- convert '9.00E+05' to '900000'





## Country:

##### KAGGLE:

- 'United Kingdom of Great Britain and Northern Ireland' -> 'United Kingdom
- 'Iran, Islamic Republic of...' -> 'Iran'
- 'United States of America' -> 'United States'

##### STACKOVERFLOW:

- 'Iran, Islamic Republic of...' -> 'Iran'




## Gender:

##### KAGGLE:

- map 'Prefer to self-describe' -> 'Other

##### STACKOVERFLOW:

- map everything that is not 'Male' or 'Female' to 'Other'




## Developer roles:

##### KAGGLE:

- 'DBA/Database Engineer'               -> 'DBA or Database Engineer'
- 'Product/Project Manager'             -> 'Manager'
- 'Data Analyst' and 'Business Analyst' -> 'Data or Business Analyst'

##### STACKOVERFLOW:

- 'C-suite executive (CEO, CTO, etc.)'                                -> 'Manager'
- 'Data scientist or machine learning specialist'                     -> 'Data Scientist'
- 'Database administrator'                                            -> 'DBA or Database Engineer'
- 'Product manager'                                                   -> 'Product or Project Manager'
- 'Back-end Developer', 'Front-end developer', 'Full-stack developer' -> 'Software Engineer'
- 'Desktop or enterprise applications developer'                      -> 'Software Engineer'
- 'DevOps specialist'                                                 -> 'Software Engineer'
- 'Embedded applications or devices developer'                        -> 'Software Engineer'
- 'Engineering manager'                                               -> 'Manager'
- 'Educator or academic researcher'                                   -> 'Research Scientist'
- 'Game or graphics developer'                                        -> 'Software Engineer'
- 'Mobile developer'                                                  -> 'Software Engineer'
- 'QA or test developer'                                              -> 'Software Engineer'





## Computer languages:

##### KAGGLE:

- 'C#'         -> 'Csharp'
- 'C++'        -> 'Cplusplus'
- 'Javascript' -> 'JavaScript'

##### STACKOVERFLOW:

- 'Bash/Shell'           -> 'Bash'
- 'C#'                   -> 'Csharp'
- 'C++'                  -> 'Cplusplus'
- 'F#'                   -> 'Fsharp'
- 'Delphi/Object Pascal' -> 'Delphi ObjectPascal'