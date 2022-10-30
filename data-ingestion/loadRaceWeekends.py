# required libraries
import pandas as pd
import os
from pathlib import Path
# Load the required libraries
from rdflib import Graph, Literal, RDF, URIRef, Namespace
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF, XSD
# CHECK DATE 
import datetime

path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())

# parameters and URLs
racesURL = path + '/project/data/races.csv'

# saving folder
savePath =  path + '/project/rdf/'  

F1 = Namespace("http://www.dei.unipd.it/database2/Formula1Ontology#")

# Load the CSV files in memory
races = pd.read_csv(racesURL, sep=',', index_col='raceId')

#create the graph
g = Graph()

# Bind the namespaces to a prefix for more readable output
g.bind("xsd", XSD)
g.bind("f1", F1)

#iterate over the league dataframe
for index, row in races.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the league id as URI
    
    #create id for the Driver
    idR = "race"+str(index)
    
    #create the Driver object
    Race = URIRef(F1[idR])
    
    # Add triples using store's add() method.
    g.add((Race, RDF.type, F1.RaceWeekend))
    g.add((Race, F1['name'], Literal(row['name'], datatype=XSD.string))) 
    g.add((Race, F1['year'], Literal(row['year'], datatype=XSD.int)))
    g.add((Race, F1['round'], Literal(row['round'], datatype=XSD.int)))
    g.add((Race, F1['date'], Literal(row['date'], datatype=XSD.date)))
   
    #TODO: add rating

    #create circuit node associate

    idC = 'circuit' + str(row['circuitId'])
    Circuit = URIRef(F1[idC])
    # add the triple
    g.add((Race, F1['locatedIn'], Circuit))   





# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'raceWeekend.ttl', 'w') as file:
    file.write(g.serialize(format='turtle'))
