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
    
    r = ret["results"]["bindings"]

    cons = [] 

    for item in r:
        for key, value in item.items():
            if(key == "name"):
                cons.append(value['value'])

    return cons

def get_teams_won(sparql, driverId):
    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    
    r = ret["results"]["bindings"]

    cons = [] 

    for item in r:
        for key, value in item.items():
            if(key == "name"):
                cons.append(value['value'])

    return cons

def get_seasons_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    return r["nSeasons"]["value"]

def get_races_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        
        ?drive a f1:Drive
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["nRaces"]["value"]

def get_pole_positions_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (COUNT(*) as ?nPolePosition)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:quali_position "1"^^xsd:int
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["nPolePosition"]["value"]

def get_wins_count(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT (COUNT(*) as ?nRaceVictories)  WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position "1"^^xsd:int
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["nRaceVictories"]["value"]

def get_top_ten_position_by_year(sparql, driverId):
    
    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
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
    
    r = ret["results"]["bindings"]

    yf = {}

    for item in r:
        year = 0

        for key, value in item.items():
            if(key == "year"):
                year = (value['value'])                
            if(key == "top10Finishes"):
                yf[year] = value['value']

    return yf

def get_top_five_position_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
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
    
    r = ret["results"]["bindings"]

    tf = {}

    for item in r:
        year = 0

        for key, value in item.items():
            if(key == "year"):
                year = (value['value'])                
            if(key == "top5Finishes"):
                tf[year] = value['value']

    return tf

def get_podiums(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    return r["nPodiums"]["value"]

def get_percentage_of_podiums_wrt_total_races(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    return r["perc"]["value"]

def get_percentage_of_wins_wrt_total_races(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    return r["perc"]["value"]

def best_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX person: <https://w3id.org/MON/person.owl#Person>

    SELECT (MIN(?quali_position) as ?bestQuali) (MIN(?race_position) as ?bestRace) WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position ?race_position ; 
            f1:quali_position ?quali_position .
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return {
        "bestQuali" : r["bestQuali"]["value"],
        "bestRace" : r["bestRace"]["value"],
    }

def worst_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT (MAX(?quali_position) as ?worstQuali) (MAX(?race_position) as ?worstRace) WHERE { 
        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver$driverId)
        ?drive f1:race_position ?race_position ; 
            f1:quali_position ?quali_position
    }

    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return {
        "worstQuali" : r["worstQuali"]["value"],
        "worstRace" : r["worstRace"]["value"],
    }

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
    return r["q3_quali"]["value"]

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
    return r["nVictoryFromPole"]["value"]

def driver_championship_points_year_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    
    r = ret["results"]["bindings"]

    points = {}

    for item in r:
        year = 0

        for key, value in item.items():
            if(key == "year"):
                year = (value['value'])                
            if(key == "points"):
                points[year] = value['value']

    return points

def driver_championship_positions_year_by_year(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?year ?cp_pos WHERE {

        ?driver f1:hasDrivenIn ?drive .
        FILTER(?driver = f1:driver1)

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
    
    r = ret["results"]["bindings"]

    pos = {}

    for item in r:
        year = 0

        for key, value in item.items():
            if(key == "year"):
                year = (value['value'])                
            if(key == "cp_pos"):
                pos[year] = value['value']

    return pos

def driver_dnf(sparql, driverId):

    query = Template("""

    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

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
    return r["dnf"]["value"]

"""
@param sparql configured wrapper
@param driverId ID of the driver for which stats are requested
@return dictionary with all the driver stats
"""
def driver_stats(sparql, driverId):

    stats = {}

    try:
        stats['cp_win'] = get_number_of_cp_wins(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['constructor'] = get_teams(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['constructor_win'] = get_teams_won(sparql, driverId)
    except Exception as e:
        print(e)
    
    try:
        stats['season_number'] = get_seasons_count(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['races_number'] = get_races_count(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['pole_number'] = get_pole_positions_count(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['victories_number'] = get_wins_count(sparql, driverId)
    except Exception as e:
        print(e)
        
    try:
        stats['perc_vic_races'] = get_percentage_of_wins_wrt_total_races(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['podiums'] = get_podiums(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['perc_pod_races'] = get_percentage_of_podiums_wrt_total_races(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['best_quali'] = best_finish_in_qualifying_and_race(sparql, driverId)['bestQuali']
    except Exception as e:
        print(e)

    try:
        stats['worst_quali'] = worst_finish_in_qualifying_and_race(sparql, driverId)['worstQuali']
    except Exception as e:
        print(e)

    try:
        stats['best_race'] = best_finish_in_qualifying_and_race(sparql, driverId)['bestRace']
    except Exception as e:
        print(e)

    try:
        stats['worst_race'] = worst_finish_in_qualifying_and_race(sparql, driverId)['worstRace']
    except Exception as e:
        print(e)

    try:
        stats['q3_quali'] = count_times_q3_reached(sparql, driverId)
    except Exception as e:
        print(e)
    
    try:
        stats['dnf'] = driver_dnf(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        stats['victory_from_pole'] = count_first_in_qualifying_and_won_race(sparql, driverId)
    except Exception as e:
        print(e)  

    return stats

"""
@param sparql configured wrapper
@param driverId ID of the driver for which stats are requested
@return dictionary with all the driver charts
"""
def driver_charts(sparql, driverId):

    charts = {}

    try:
        charts["driver_championship_points_year_by_year"] = driver_championship_points_year_by_year(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        charts["driver_championship_positions_year_by_year"] = driver_championship_positions_year_by_year(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        charts["get_top_ten_position_by_year"] = get_top_ten_position_by_year(sparql, driverId)
    except Exception as e:
        print(e)

    try:
        charts["get_top_five_position_by_year"] = get_top_five_position_by_year(sparql, driverId)
    except Exception as e:
        print(e)

    return charts