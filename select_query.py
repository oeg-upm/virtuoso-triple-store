import rdflib
import os
from SPARQLWrapper import SPARQLWrapper, JSON, N3, POST, DIGEST

graph_uri = "<http://localhost:8890/serge>"

query = "SELECT ?s FROM {} ".format(graph_uri) + "WHERE {?s ?p ?o}"

sparql = SPARQLWrapper("http://localhost:8890/sparql")
sparql.setQuery(query)

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["s"])