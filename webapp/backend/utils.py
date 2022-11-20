from string import Template

def getNumberOfWins(sparql, driverId): 

    query = Template("""
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    select (COUNT(*) as ?wins) where {

        ?driver a f1:Driver.
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


"""
@param sparql configured wrapper
@param drivernId ID of the driver for which stats are requested
@return dictionary with all the driver stats
"""
def driverStats(sparql, driverId):

    stats = []

    try:
        stats['wins'] = getNumberOfWins(sparql, driverId)
    except Exception as e:
        print(e)