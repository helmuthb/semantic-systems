# Application

Jobsta

## Description

Is a service hub for interested persons and companies. Based on TU Vienna lectures and ...



## Datasources

Github [Repositories, Stars, Issues, Programming-Language, (Country?)]
Kaggle [Users, Job-Role, Country, Salary, Programming-Language]
Stackoverflow [Users, Job-Role, Country, Salary, Programming-Language]
TISS [Lectures(Course_ID, Title, Description, ECTS, Programming-Language, URL), Lecturer (Name, URL)]


## Queries

As a (software developer) I live in (Country) and I can program in (Python) and I want at least (XXX USD per year). Should I stay or should I go?
> Yes/No/Country

As a student I want to learn language (Python). Which courses should I take?
> TU Wien Courses

As a (Python) programmer, at which repositories with most stars can I coloborate?
> Repositories Github

Which (Python) repositories have the most issues open?
> 

Which role should I aspire to earn the most money with age (XX) in (country)?
> Job-Role




## Preprocessing

- Merge columns (combine Stackoverflow, Kaggle, Github)
- Merge entries of merged columns
- add links to individuals, e.g. kaggle.com/dataset/xyx#1234, tiss.tuwien.ac.at/courses#ARAC,... as identifier in the about attribute


## Extensions

- Create hierarchy for job roles


## Exclusions

- Remove timestamps, only current data 

## Learning

[OpenRefine](https://www.youtube.com/watch?v=XdpzmGxA33U)

## app

- web ui with rest endpoints to jena
- cli with click/python https://click.palletsprojects.com/en/7.x/
