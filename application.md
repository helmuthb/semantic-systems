# Application

Jobsta

## Description

Is a service hub for interested persons and companies. Based on TU Vienna lectures and ...



## Datasources

Github [Repositories, Stars, Issues, Language, (Country?)]
Kaggle [Users, Job-Role, Country, Salary, Language]
Stackoverflow [Users, Job-Role, Country, Salary, Language]
TISS [Lectures(Title, Description, ECTS, Programming-Language), Lecturer (Name)]


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


## Extensions

- Create hierarchy for job roles


## Exclusions

- Remove timestamps, only current data 

## Learning

[OpenRefine](https://www.youtube.com/watch?v=XdpzmGxA33U)