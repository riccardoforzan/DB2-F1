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
driversURL = path + '/project/data/drivers.csv'

# saving folder
savePath =  path + '/project/rdf/'  

# Construct the country and the formula1 ontology namespaces not known by RDFlib
CNS = Namespace("http://eulersharp.sourceforge.net/2003/03swap/countries#")
F1 = Namespace("http://www.dei.unipd.it/database2/Formula1Ontology#")

# Load the CSV files in memory
drivers = pd.read_csv(driversURL, sep=',', index_col='driverId')

#create the graph
g = Graph()

# Bind the namespaces to a prefix for more readable output
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("countries", CNS)
g.bind("f1", F1)

#iterate over the league dataframe
for index, row in drivers.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the league id as URI
    
    #create id for the Driver
    idD = "driver"+str(index)
    
    #create the Driver object
    Driver = URIRef(F1[idD])
    
    # Add triples using store's add() method.
    g.add((Driver, RDF.type, F1.Driver))
    g.add((Driver, F1['firstName'], Literal(row['forename'], datatype=XSD.string))) 
    g.add((Driver, F1['lastName'], Literal(row['surname'], datatype=XSD.string)))

    #check if the driver number is present
    if row['number'] != '\\N':
        g.add((Driver, F1['driverNumber'], Literal(row['number'], datatype=XSD.int)))
    g.add((Driver, F1['driverCode'], Literal(row['code'], datatype=XSD.string)))       

    #TODO: add nationality 
    
    #TODO: create the drive node associated



# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'drivers.ttl', 'w') as file:
    file.write(g.serialize(format='turtle'))
