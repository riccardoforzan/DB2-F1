from string import Template

def get_number_of_cp_wins(sparql, driverId): 

    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT (COUNT(*) as ?wins) WHERE {

        ?driver a f1:Driver.
        ?driver f1:hasDrivenIn ?drive .
        FILTER (?driver = f1:driver$driverId)

        ?drive f1:cp_position_after_race "1"^^xsd:int ;
            f1:during ?rwe.

        #Get the result only of the last race of the year
        FILTER(?rwe = ?race){
            SELECT distinct ?race WHERE {
                ?race f1:round ?round;
                    f1:year ?y;
                    FILTER (?round = ?lastRace && ?y = ?year){
                        SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                            ?raceWeekends f1:round ?round;
                                        f1:year ?year.
                        }
                        GROUP BY ?year
                        ORDER BY asc(?year)
                }
            }
        }

    }
    
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_teams(sparql, driverId):
    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT ?cons ?name WHERE { 

        ?driver a f1:Driver.
        FILTER (?driver = f1:driver$driverId)

        ?driver f1:hasDrivenIn ?drive .

        ?drive f1:driveFor ?cons . 

        ?cons f1:name ?name
        
    } 
    GROUP BY ?cons ?name 
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]

    cons = [] 

    for key, value in r.items():
        if(key == "name"):
            cons.append(value['value'])

    return cons

def get_teams_won(sparql, driverId):
    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT ?cons ?name WHERE { 

            ?driver a f1:Driver.
            FILTER (?driver = f1:driver$driverId)

            ?driver f1:hasDrivenIn ?drive .

        ?drive f1:driveFor ?cons ;
                f1:race_position "1"^^xsd:int . 

        ?cons f1:name ?name .
    }  
    GROUP BY ?cons ?name
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]

    cons = [] 

    for key, value in r.items():
        if(key == "name"):
            cons.append(value['value'])

    return cons

def get_seasons_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (COUNT(DISTINCT ?year) as ?nSeasons)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:during ?raceWeekend . 
        ?raceWeekend f1:year ?year . 
            
    }
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_races_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        
        ?drive a f1:Drive
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_pole_positions_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (COUNT(*) as ?nPolePosition)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driveId)
        ?drive f1:quali_position "1"^^xsd:int
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_wins_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (COUNT(*) as ?nRaceVictories)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position "1"^^xsd:int
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_top_ten_position_by_year(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>
    SELECT ?year (COUNT(*) as ?top10Finishes) WHERE { 
        
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        
        ?drive f1:race_position ?race_pos ; 
            f1:during ?rwe .
        
        ?rwe f1:year ?year .
        FILTER (?race_pos <= 10)
        
    }  
    GROUP BY ?year
    ORDER BY ?year

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_top_five_position_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>
    SELECT ?year (COUNT(*) as ?top5Finishes) WHERE { 
        
        ?driver f1:hasDrivenIn ?drive .
        FILTER($driver = f1:driver$driverId)
        
        ?drive f1:race_position ?race_pos ; 
            f1:during ?rwe .
        
        ?rwe f1:year ?year .
        FILTER (?race_pos <= 5)
        
    }  
    GROUP BY ?year
    ORDER BY ?year

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_podiums(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (COUNT(*) as ?nPodiums)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER($driver = f1:driver$driverId)
        ?drive f1:race_position ?position .
        FILTER (?position = 1 || ?position = 2 || ?position = 3)
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_percentage_of_podiums_wrt_total_races(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (?nPolePosition / ?nRaces * 100 as ?perc) WHERE { 
        {
            SELECT (COUNT(*) as ?nPolePosition)  WHERE { 
                ?driver f1:hasDrivenIn ?drive .
                FILTER(?driver = f1:driver$driverId)
                ?drive f1:race_position ?position .
                FILTER (?position = 1 || ?position = 2 || ?position = 3)
            }
        } 
        {
            SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
                    ?driver f1:hasDrivenIn ?drive .
                    FILTER(?driver = f1:driver$driverId)
                    ?drive a f1:Drive
        }
            
        }
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_percentage_of_wins_wrt_total_races(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (?nVictories / ?nRaces * 100 as ?perc) WHERE { 
        {
            SELECT (COUNT(*) as ?nVictories)  WHERE { 
                ?driver f1:hasDrivenIn ?drive .
                FILTER(?driver = f1:driver$driverId)
                ?drive f1:race_position "1"^^xsd:int
            }
        } 
        {
            SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
                    ?driver f1:hasDrivenIn ?drive .
                    FILTER(?driver = f1:driver$driverId)

                    ?drive a f1:Drive
            }   
        }
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def best_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (MIN(?quali_position) as ?bestQuali) (MIN(?race_position) as ?bestRace)   WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position ?race_position ; 
            f1:quali_position ?quali_position
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def worts_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT (MAX(?quali_position) as ?worstQuali) (MAX(?race_position) as ?worstRace)   WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position ?race_position ; 
            f1:quali_position ?quali_position
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def count_times_q3_reached(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (COUNT(DISTINCT ?drive) as ?q3_quali) WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:q3_time ?q3_time
        
    } 

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def count_first_in_qualifying_and_won_race(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (COUNT(*) as ?nVictoryFromPole)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position "1"^^xsd:int . 
        ?drive f1:quali_position "1"^^xsd:int . 
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def driver_championship_points_year_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT ?year ?points WHERE {

        ?driver f1:hasDrivenIn ?drive .
    	FILTER(?driver = f1:driver$driverId)
                
        ?drive f1:during ?rwe ; 
            f1:cp_points_after_race ?points . 
        
        ?rwe f1:year ?year .

        #Get the result only of the last race of the year
        FILTER(?rwe = ?race){
            SELECT distinct ?race WHERE {
                ?race f1:round ?round;
                    f1:year ?y;
                    FILTER (?round = ?lastRace && ?y = ?year){
                        SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                            ?raceWeekends f1:round ?round;
                                        f1:year ?year.
                        }
                        GROUP BY ?year
                        ORDER BY asc(?year)
                }
            }
        }	

    } 
    ORDER BY ?year

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def driver_championship_positions_year_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT ?year ?cp_pos WHERE {

        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
                
        ?drive f1:during ?rwe ; 
            f1:cp_position_after_race ?cp_pos . 
        
        ?rwe f1:year ?year .

        #Get the result only of the last race of the year
        FILTER(?rwe = ?race){
            SELECT distinct ?race WHERE {
                ?race f1:round ?round;
                    f1:year ?y;
                    FILTER (?round = ?lastRace && ?y = ?year){
                        SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                            ?raceWeekends f1:round ?round;
                                        f1:year ?year.
                        }
                        GROUP BY ?year
                        ORDER BY asc(?year)
                }
            }
        }	

    } 
    ORDER BY ?year

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def driver_dnf(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#>

    SELECT ?driver (COUNT(?drive) as ?dnf) WHERE {
        ?driver a f1:Driver;
                f1:hasDrivenIn ?drive.
    	FILTER(?driver = f1:driver$driverId)

        ?drive f1:status ?status . 

        #Exclude all the drives that have been completed
        FILTER ( ?status != "Finished" && REGEX(?status, "^(?!.*Lap).*$"))
    }
    GROUP BY ?driver

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

"""
@param sparql configured wrapper
@param driverId ID of the driver for which stats are requested
@return dictionary with all the driver stats
"""
def driverStats(sparql, driverId):

    stats = {}

    try:
        stats['wins'] = get_number_of_wins(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['constructors'] = get_teams(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['constructors_wins'] = get_teams_won(sparql, driverId)
    except Exception as e:
        print(e)
    
    return stats