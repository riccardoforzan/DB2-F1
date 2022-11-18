queries = [ """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select (COUNT(*) as ?wins) where {

    ?driver person:firstName " NAME " ;
           person:lastName " SURNAME " ; 
           f1:hasDrivenIn ?drive .

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

} """ , """


PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons ?name WHERE { 
 	
    ?driver person:firstName " NAME " ; 
            person:lastName " SURNAME " ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:driveFor ?cons . 

    ?cons f1:name ?name
    
} 
GROUP BY ?cons ?name 

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons ?name where { 

    ?driver person:firstName " NAME " ; 
            person:lastName " SURNAME " ; 
            f1:hasDrivenIn ?drive .

    ?drive f1:driveFor ?cons ;
            f1:race_position "1"^^xsd:int . 

    ?cons f1:name ?name .
}  
GROUP BY ?cons ?name

""", """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(DISTINCT ?year) as ?nSeasons)  where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:during ?raceWeekend . 
    ?raceWeekend f1:year ?year . 

}

""" , """ 

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .

    ?drive a f1:Drive
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nPolePosition)  where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:quali_position "1"^^xsd:int
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nRaceVictories)  where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:race_position "1"^^xsd:int
}

""" , """ 

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?year (COUNT(*) as ?top10Finishes) where { 

    ?driver person:firstName " NAME " ; 
            person:lastName " SURNAME " ; 
            f1:hasDrivenIn ?drive .

    ?drive f1:race_position ?race_pos ; 
           f1:during ?rwe .

    ?rwe f1:year ?year .
    FILTER (?race_pos <= 10)

}  
GROUP BY ?year
ORDER BY ?year

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>
SELECT ?year (COUNT(*) as ?top5Finishes) where { 

    ?driver person:firstName " NAME " ; 
            person:lastName " SURNAME " ; 
            f1:hasDrivenIn ?drive .

    ?drive f1:race_position ?race_pos ; 
           f1:during ?rwe .

    ?rwe f1:year ?year .
    FILTER (?race_pos <= 5)

}  
GROUP BY ?year
ORDER BY ?year

""" , """ 

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nPodiums)  WHERE { 
 	?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
			f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?position .
    FILTER (?position = 1 || ?position = 2 || ?position = 3)
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (?nPolePosition / ?nRaces * 100 as ?perc) where { 
    {
        SELECT (COUNT(*) as ?nPolePosition)  where { 
            ?driver person:firstName " NAME " ;
                    person:lastName " SURNAME " ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:quali_position "1"^^xsd:int
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
                ?driver person:firstName " NAME " ;
                        person:lastName " SURNAME " ;
                        f1:hasDrivenIn ?drive .

                ?drive a f1:Drive
       }

    }
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (?nVictories / ?nRaces * 100 as ?perc) where { 
    {
        SELECT (COUNT(*) as ?nVictories)  where { 
            ?driver person:firstName " NAME " ;
                    person:lastName " SURNAME " ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:race_position "1"^^xsd:int
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
                ?driver person:firstName " NAME " ;
                        person:lastName " SURNAME " ;
                        f1:hasDrivenIn ?drive .

                ?drive a f1:Drive
       }

    }
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (MIN(?quali_position) as ?bestQuali) (MIN(?race_position) as ?bestRace)   where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?race_position ; 
           f1:quali_position ?quali_position
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (MAX(?quali_position) as ?worstQuali) (MAX(?race_position) as ?worstRace)   where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?race_position ; 
           f1:quali_position ?quali_position
}

""" , """
 
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(DISTINCT ?drive) as ?q3_quali) where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:q3_time ?q3_time

} 

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver (COUNT(?drive) as ?dnf) where {
    ?driver a f1:Driver;
            f1:hasDrivenIn ?drive.

    ?drive f1:status ?status.

    #Get the driver which last name is
    ?driver person:lastName " SURNAME " .

    #Exclude all the drives that have been completed
    FILTER ( ?status != "Finished" && REGEX(?status, "^(?!.*Lap).*$"))
}
GROUP BY ?driver

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nVictoryFromPole)  where { 
    ?driver person:firstName " NAME " ;
            person:lastName " SURNAME " ;
            f1:hasDrivenIn ?drive .
    ?drive f1:race_position "1"^^xsd:int . 
    ?drive f1:quali_position "1"^^xsd:int . 
}

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?year ?points where {

    ?driver person:firstName " NAME " ;
           person:lastName " SURNAME " ; 
           f1:hasDrivenIn ?drive .

    ?drive f1:during ?rwe ; 
           f1:cp_points_after_race ?points . 

    ?rwe f1:year ?year .

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
ORDER BY ?year

""" , """

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?year ?cp_pos where {

    ?driver person:firstName " NAME " ;
           person:lastName " SURNAME " ; 
           f1:hasDrivenIn ?drive .

    ?drive f1:during ?rwe ; 
           f1:cp_position_after_race ?cp_pos . 

    ?rwe f1:year ?year .

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
ORDER BY ?year """ 
] 
