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
driversURL = path + '/project/data/drivers.csv'
resultsURL = path + '/project/data/results.csv'
qualifyngURL = path + '/project/data/qualifying.csv'
sprintURL = path + '/project/data/sprint_results.csv'
driversStandingsURL = path + '/project/data/driver_standings.csv'

# saving folder
savePath =  path + '/project/rdf/'  

# Construct the formula1 ontology namespaces not known by RDFlib
CNS = Namespace("http://eulersharp.sourceforge.net/2003/03swap/countries#")
F1 = Namespace("http://www.dei.unipd.it/database2/Formula1Ontology#")

#this function create and load all the given driver drives (a drives include all the pilot performances in a given race weekend)
#@param driverId of the given driver 
#@param Driver node 
#@param g graph where to add the nodes
def loadDriverDrives(driverId, Driver, g):

    print("Processing driver:"+str(driverId))
    
    # Load the results.csv, qualifying.csv and sprint_results.csv files
    results = pd.read_csv(resultsURL, sep=',', index_col='resultId')
    qualifying = pd.read_csv(qualifyngURL, sep=',', index_col='qualifyId')
    sprint_race = pd.read_csv(sprintURL, sep=',', index_col='resultId')
    driver_standings = pd.read_csv(driversStandingsURL, sep=',', index_col='driverStandingsId')

    #searching all the race results of the given driver, this is the driver drive
    driverDrives = results.loc[results['driverId'] == driverId] 

    for index, row in driverDrives.iterrows():
        
        #create id for the drive
        idDrive = "drive"+str(index)
            
        #create the Drive object
        Drive = URIRef(F1[idDrive])
            
        # Add triples using store's add() method
        g.add((Drive, RDF.type, F1.Drive))
        g.add((Drive, F1['race_position'], Literal(row['positionOrder'], datatype=XSD.string))) 
        g.add((Drive, F1['fast_lap'], Literal(row['fastestLapTime'], datatype=XSD.string)))

        #---------- ADD CONSTRUCTOR INFORMATIONS ----#

        #id of the constructor for which this driver drives
        idCons = "constructor"+str(row['constructorId'])
        g.add((Drive, F1['driveFor'], URIRef(F1[idCons])))
            
        #----------- ADD QUALI INFORMATIONS ---------#

        #searching the qualify of the given driver in the given drive 
        qualifyDriver = qualifying.loc[(qualifying['driverId'] == driverId) & (qualifying['raceId'] == row['raceId'])] 

        #check for quali time
        if qualifyDriver.size > 0:
            g.add((Drive, F1['quali_position'], Literal(qualifyDriver['position'].iloc[0], datatype=XSD.int)))
            g.add((Drive, F1['q1'], Literal(qualifyDriver['q1'].iloc[0], datatype=XSD.string)))
            g.add((Drive, F1['q2'], Literal(qualifyDriver['q2'].iloc[0], datatype=XSD.string)))
            g.add((Drive, F1['q3'], Literal(qualifyDriver['q3'].iloc[0], datatype=XSD.string)))

        #----------- ADD SPRINT RACE INFORMATIONS ---------#

        #searching the sprint_race position of the given driver in the given drive if present
        sprintDriver = sprint_race.loc[(sprint_race['driverId'] == driverId) & (sprint_race['raceId'] == row['raceId'])] 

        #check for sprint_race position
        if sprintDriver.size > 0:
            g.add((Drive, F1['quali_position'], Literal(sprintDriver['position'].iloc[0], datatype=XSD.string)))

        #----------ADD DRIVER STANDING INFOMRATION ------#
       
        #searching the driver standing informations (points, number of victories and position) after the drive 
        dr = driver_standings.loc[(driver_standings['driverId'] == driverId) & (driver_standings['raceId'] == row['raceId'])] 
        g.add((Drive, F1['points_after_race'], Literal(driver_standings['points'].iloc[0], datatype=XSD.int)))
        g.add((Drive, F1['position_after_race'], Literal(driver_standings['position'].iloc[0], datatype=XSD.int)))
        g.add((Drive, F1['number_of_wins'], Literal(driver_standings['wins'].iloc[0], datatype=XSD.int)))

        #-------------ADD RACE WEEKEND INFORMATION ------# 

        #add the race_weekend associated to the drive
        idRWE = "raceWeekEnd"+str(row['raceId'])
        g.add((Drive, F1['during'], URIRef(F1[idRWE])))  


        #add the drive
        g.add((Driver, F1['appearIn'], Drive))

#--------------- MAIN ---------------- #

# Load the CSV files in memory
drivers = pd.read_csv(driversURL, sep=',', index_col='driverId')

#create the graph
g = Graph()

# Bind the namespaces to a prefix for more readable output
g.bind("foaf", FOAF)
g.bind("xsd", XSD)
g.bind("countries", CNS)
g.bind("f1", F1)

#iterate over the drivers dataframe
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
    
    loadDriverDrives(index, Driver, g)


# print all the data in the Turtle format
print("--- saving serialization ---")
with open(savePath + 'drivers.ttl', 'w') as file:
    file.write(g.serialize(format='turtle'))
