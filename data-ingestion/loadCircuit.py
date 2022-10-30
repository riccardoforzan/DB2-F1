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
circuitURL = path + '/project/data/circuits.csv'

# saving folder
savePath =  path + '/project/rdf/'  

# Construct the country and the formula1 ontology namespaces not known by RDFlib
CNS = Namespace("http://eulersharp.sourceforge.net/2003/03swap/countries#")
F1 = Namespace("http://www.dei.unipd.it/database2/Formula1Ontology#")

# Load the CSV files in memory
circuits = pd.read_csv(circuitURL, sep=',', index_col='circuitId')

#create the graph
g = Graph()

# Bind the namespaces to a prefix for more readable output
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("countries", CNS)
g.bind("f1", F1)

#iterate over the league dataframe
for index, row in circuits.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the league id as URI
    
    #create id for the circuit
    idC = "circuit"+str(index)
    
    #create the circuit object
    Circuit = URIRef(F1[idC])
    
    # Add triples using store's add() method.
    g.add((Circuit, RDF.type, F1.Circuit))
    g.add((Circuit, F1['name'], Literal(row['name'], datatype=XSD.string)))    

    #check for altitude value (some values are missing and have a \N value instead)
    if not row['alt'] == '\\N':
        g.add((Circuit, F1['altitude'], Literal(row['alt'], datatype=XSD.int)))    
    
    # create the RDF node for the country associated to this circuit
    Country = URIRef(CNS[row['country'].replace(" ", "")])
    
    # add the edge connecting the Circuit and the Country 
    g.add((Circuit, F1['hasCountry'], Country))    


# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'circuits.ttl', 'w') as file:
    file.write(g.serialize(format='turtle'))
