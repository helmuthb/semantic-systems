// functions for querying SPARQL server and parse results
const url = 'https://jena.helmuth.at/jobsta/query';
const prefix = `
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX group1: <http://www.semanticweb.org/sws/ws2019/group1#>
PREFIX schema: <http://schema.org/>
PREFIX dbpedia: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sc: <http://purl.org/science/owl/sciencecommons/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>`;

// generic SPARQL query (SELECT, ASK, ...)
var querySPARQL = async function(query) {
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/sparql-query',
      'Accept': 'application/sparql-results+json'
    },
    body: prefix + '\n' + query
  });
  return await response.json();
}

// specific SPARQL query: ASK - will return only true or false
var askSPARQL = async function(query) {
  const json = await querySPARQL(query);
  return json.boolean;
}

// specific SPARQL query: SELECT - will return list of objects
var selectSPARQL = async function(query) {
  const json = await querySPARQL(query);
  let result = [];
  let names = json.head.vars;
  for (row of json.results.bindings) {
    // special case: only one variable requested
    if (names.length == 1) {
      result.push(row[names[0]].value);
    }
    else {
      let row_val = {};
      for (name of names) {
        row_val[name] = row[name].value;
      }
      result.push(row_val);
    }
  }
  console.log(json);
  console.log(result);
  return result;
}