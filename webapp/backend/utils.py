from string import Template

def get_number_of_wins(sparql, driverId): 

    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    select (COUNT(*) as ?wins) where {

        ?driver a f1:Driver.
        ?driver f1:hasDrivenIn ?drive .
        FILTER (?driver = f1:driver$driverId)

        ?drive f1:cp_position_after_race "1"^^xsd:int ;
            f1:during ?rwe.

        #Get the result only of the last race of the year
        FILTER(?rwe = ?race){
            select distinct ?race where {
                ?race f1:round ?round;
                    f1:year ?y;
                    FILTER (?round = ?lastRace && ?y = ?year){
                        select (MAX(?round) as ?lastRace) ?year where {
                            ?raceWeekends f1:round ?round;
                                        f1:year ?year.
                        }
                        group by ?year
                        order by asc(?year)
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

    SELECT ?cons ?name where { 

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
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_races_count(sparql, driverId):
    
    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_pole_positions_count(sparql, driverId):
    
    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_wins_count(sparql, driverId):
    
    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_pole_positions_count(sparql, driverId):
    
    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_top_ten_position_by_year(sparql, driverId):
    
    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_top_five_position_by_year(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_podiums(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def get_percentage_of_podiums_wrt_total_races(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def best_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def worts_finish_in_qualifying_and_race(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def count_times_q3_reached(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def count_first_in_qualifying_and_won_race(sparql, driverId):

    query = Template("""
    """).safe_substitute(driverId=driverId)

    sparql.setQuery(query)
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0]
    return r["wins"]["value"]

def driver_championship_positions_year_by_year(sparql, driverId):

    query = Template("""
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