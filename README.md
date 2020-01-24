# Introduction to Semantic Systems - WS 2019

## Participants
* 8725866 Helmuth Breitenfellner
* 09227679 Laszlo Kiraly
* 0125536 Gerald Weber  
* 01425692 Cem Bicer  

## App

### Description

### Datasets

- [Kaggle Survey 2019](https://www.kaggle.com/c/kaggle-survey-2019), [Kaggle Survey 2018](https://www.kaggle.com/kaggle/kaggle-survey-2018)
- [Stackoverflow Survey 2019](https://insights.stackoverflow.com/survey/2019), [Stackoverflow Survey 2018](https://insights.stackoverflow.com/survey/2018)
- [Github Octoverse 2019](https://github.blog/2019-11-06-the-state-of-the-octoverse-2019/)
  did not work out, only summary no dataset, use [graphql api](https://medium.com/@fabiomolinar/using-githubs-graphql-to-retrieve-a-list-of-repositories-their-commits-and-some-other-stuff-ccbbb4e96d78) instead?
- [TISS TU Wien LV Daten Current](https://tiss.tuwien.ac.at/course/courseList.xhtml?dswid=6403&dsrid=238)

### Ontologies

#### Kaggle

#### Stackoverflow

#### Github

##### Example Query

**Top 10 Starred Repositories**

https://developer.github.com/v4/explorer
```graphql
query{
  search(type: REPOSITORY, query: "language:python", first:10) {
    userCount
    edges {
      node {
        ... on Repository {
          name
          url
          stargazers {
            totalCount
          }
          owner{
            login
          }
        }
      }
    }
  }
}
```

#### Tiss

### App Ontology

merged ontology

### Knowledge Graph

### Queries


## Todos

- Create ontologies for your dataset
- Find join points in different ontologies
- rdf ids 
- Check Viet Nam vs Stackoverflow

