# required libraries
from copyreg import constructor
import pandas as pd
import os
from pathlib import Path
# Load the required libraries
from rdflib import Graph, Literal, RDF, URIRef, Namespace
# rdflib knows about some namespaces, like FOAF
from rdflib.namespace import FOAF, XSD
# CHECK DATE 
import datetime

#------------------ SETTING PATHS -----------------------#

path = str(Path(os.path.abspath(os.getcwd())).parent.absolute())

# parameters and URLs
constructorURL = path + '/project/data/constructors.csv'
constructor_resultsURL = path + '/project/data/constructor_results.csv'
constructorStandingsURL = path + '/project/data/constructor_standings.csv'
pitstopsURL =  '/project/data/pit_stops.csv'

# saving folder
savePath =  path + '/project/rdf/'  

# Construct the formula1 ontology namespaces not known by RDFlib
CNS = Namespace("http://eulersharp.sourceforge.net/2003/03swap/countries#")
F1 = Namespace("http://www.dei.unipd.it/database2/Formula1Ontology#")

#this function create and load all the given constrcutor partecipations (a partecipation includes all the constructor performance informations in a given race weekend)
#@param constructorId of the given constrcutor 
#@param Constructor node 
#@param g graph where to add the nodes
def loadConstructorPartecipations(constructorId, Constructor, g):

    print("Processing constructor:"+str(constructorId))
    
    # Load the csv files
    results = pd.read_csv(constructor_resultsURL, sep=',', index_col='constructorResultsId')
    constructors_standings = pd.read_csv(constructorStandingsURL, sep=',', index_col='constructorStandingsId')

    #searching all the race results of the given constructor, this is the constructor partecipation
    constructorPartecipations = results.loc[results['constructorId'] == constructorId] 

    for index, row in constructorPartecipations.iterrows():
        
        #create id for the partecipation
        idPartecipation = "partecipation"+str(index)
            
        #create the Partecipate object
        Partecipate = URIRef(F1[idPartecipation])
            
        # Add triples using store's add() method
        g.add((Partecipate, RDF.type, F1.Partecipate))

        #----------ADD CONSTRUCTOR STANDING INFOMRATION ------#
       
        #searching the constructor standing informations (points, number of victories and position) after the partecipation 
        dr = constructors_standings.loc[(constructors_standings['constructorId'] == constructorId) & (constructors_standings['raceId'] == row['raceId'])] 
        g.add((Partecipate, F1['points_after_race'], Literal(constructors_standings['points'].iloc[0], datatype=XSD.int)))
        g.add((Partecipate, F1['position_after_race'], Literal(constructors_standings['position'].iloc[0], datatype=XSD.int)))
        g.add((Partecipate, F1['number_of_wins'], Literal(constructors_standings['wins'].iloc[0], datatype=XSD.int)))

        #-------------ADD RACE WEEKEND INFORMATION ------# 

        #add the race_weekend associated to the drive
        idRWE = "raceWeekEnd"+str(row['raceId'])
        g.add((Partecipate, F1['during'], URIRef(F1[idRWE])))  


        #add the drive
        g.add((Constructor, F1['appearIn'], Partecipate))

#--------------- MAIN ---------------- #

# Load the CSV files in memory
constructors = pd.read_csv(constructorURL, sep=',', index_col='constructorId')

#create the graph
g = Graph()

# Bind the namespaces to a prefix for more readable output
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("countries", CNS)
g.bind("f1", F1)

#iterate over the constructors dataframe
for index, row in constructors.iterrows():
    # Create the node to add to the Graph
    # the node has the namespace + the league id as URI
    
    #create id for the Driver
    idCons = "constructor"+str(index)
    
    #create the Driver object
    Constructor = URIRef(F1[idCons])
    
    # Add triples using store's add() method.
    g.add((Constructor, RDF.type, F1.Constructor))
    g.add((Constructor, F1['name'], Literal(row['name'], datatype=XSD.string))) 

    #TODO: add country
    
    loadConstructorPartecipations(index, Constructor, g)


# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'constructors.ttl', 'w') as file:
    file.write(g.serialize(format='turtle'))
