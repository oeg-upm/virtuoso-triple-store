import rdflib
import os
import re
import argparse
from SPARQLWrapper import SPARQLWrapper, JSON, N3, POST, DIGEST, XML
from rdflib.term import URIRef, Literal

def insert_data(graph_uri, filepath):

    sparql = SPARQLWrapper("http://localhost:8890/sparql-auth")
    sparql.setHTTPAuth(DIGEST)
    sparql.setCredentials('demo1','mysecret')
    sparql.setMethod(POST)

    g = rdflib.Graph()
    g.parse(filepath, format="turtle")

    # We have to reestructure the data in order to give it the format
    # of SPARQL queries, e.g. with the prefixes instead of the whole URI's.

    query = ""
    for prefix, ns in g.namespaces():
        query = query + "PREFIX {}: <{}>".format(prefix, ns) + "\n"

    triples = ""
    for s, p, o in g:
        for prefix, ns in g.namespaces():
            if ns in s:
                subject = s.replace(ns, prefix + ":")
            if ns in p:
                predicate = p.replace(ns, prefix + ":")
            if ns in o and type(o) is URIRef:
                object = o.replace(ns, prefix + ":")
            elif type(o) is Literal and ns in o.datatype:
                datatype = str(o.datatype).replace(ns, prefix + ":")

        if type(o) is URIRef:
            
            triples = triples + subject + " " + predicate + " " + object + " ." + "\n"
            
        if type(o) is Literal:
            if o.datatype is not None:
                triples = triples + subject + " " + predicate + " " + "\"" + o + "\"" + "^^" + datatype + " ." + "\n"
            elif o.language is not None:
                triples = triples + subject + " " + predicate + " " + "\"" + o + "\"" + "@" + o.language + " ." + "\n"

    query = query + "INSERT INTO <{}> ".format(graph_uri) + "{" + triples + "}"

    sparql.setQuery(query)
    sparql.queryType = "INSERT"

    results = sparql.query()


if __name__ == "__main__":
    
    # How to execute the model
    # Example:
    # python insert_query.py http://localhost:8890/building ttl_files/building_example.ttl

    parser = argparse.ArgumentParser()
    parser.add_argument("named_graph_uri", help="Name of the graph where to store data", type=str)
    parser.add_argument("filepath", help="Path to the rdf file to store", type=str)

    args = parser.parse_args()

    insert_data(args.named_graph_uri, args.filepath)