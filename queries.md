# Queries: 

---

##### Query 1: Who is the last italian driver to win a driver championship? And in which year?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>
PREFIX countries: <http://eulersharp.sourceforge.net/2003/03swap/countries#>

SELECT ?driver ?name ?surname ?year WHERE {

    ?driver person:firstName ?name ;
    	    person:lastName ?surname ; 
		    f1:hasDrivenIn ?drive ; 
    		f1:nationality countries:it . 
    
    ?drive f1:during ?rwe ; 
    	   f1:cp_position_after_race "1"^^xsd:int . 
   	
    ?rwe f1:year ?year .

    #Get the result only of the last race of every year
    FILTER(?rwe = ?race)
    {
        SELECT DISTINCT ?race WHERE {
            ?race f1:round ?round;
                  f1:year ?y;
                  FILTER (?round = ?lastRace && ?y = ?year)
            	  {
                		SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                        	?raceWeekends f1:round ?round;
                                      f1:year ?year.
                    	}
                    	GROUP BY ?year
            	  }
        }
    }	
            
}
ORDER BY DESC (?year) 
LIMIT 1


```

##### Query 2: Which is, for every year, the most liked race?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?year ?name ?rate WHERE {
	
    ?rw f1:name ?name ;
        f1:year ?year; 
        f1:fans_rating ?rate
    
    FILTER (?year = ?yearR && ?rate = ?maxRate)
    
    {
    	SELECT ?yearR (MAX(?rate) AS ?maxRate) WHERE {
          	?rw f1:year ?yearR; 
   			    f1:fans_rating ?rate .
		}
        GROUP BY ?yearR

    }         
}   
ORDER BY ?year
```

##### Query 3: Which is the team with the biggest number of victories of the constructor championship? And with how many wins?

```sparql
PREFIX dbpedia_f1: <https://dbpedia.org/ontology/FormulaOneTeam#>
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?team ?teamName (COUNT(?team) as ?wins) WHERE {

    ?team rdf:type dbpedia_f1:FormulaOneTeam;
          f1:name ?teamName.

    ?team f1:participateIn ?part.
    ?part f1:cp_position_after_race ?finalPos.
    ?part f1:during ?rwe.

    #Get the result only of the last race of the year
    FILTER(?rwe = ?race){
        SELECT distinct ?race WHERE {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  f1:year ?y;
                  FILTER (?round = ?lastRace && ?y = ?year){
                SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                    ?raceWeekends a f1:RaceWeekend;
                                  f1:round ?round;
                                  f1:year ?year.
                }
                GROUP BY ?year
                ORDER BY asc(?year)
            }
        }
    }

    #Get only the teams that won
    FILTER(?finalPos = "1"^^xsd:int)

}
GROUP BY ?team ?teamName
ORDER BY desc(?wins)
LIMIT 1
```

##### Query 4: Who is the pilot with the biggest number of victories of the driver championship?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?driver ?name ?surname (COUNT(?driver) as ?wins) WHERE {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_position_after_race ?finalPos ;
           f1:during ?rwe.

    #Get the result only of the last race of the year
    FILTER(?rwe = ?race){
        SELECT distinct ?race WHERE {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  f1:year ?y;
                  FILTER (?round = ?lastRace && ?y = ?year){
                SELECT (MAX(?round) as ?lastRace) ?year WHERE {
                    ?raceWeekends a f1:RaceWeekend;
                                  f1:round ?round;
                                  f1:year ?year.
                }
                GROUP BY ?year
                ORDER BY asc(?year)
            }
        }
    }

    #Get only the teams that won
    FILTER(?finalPos = "1"^^xsd:int)

}
GROUP BY ?driver ?name ?surname
ORDER BY desc(?wins)
LIMIT 1
```

##### Query 5: Who is the pilot with the best lap time in a given circuit? Return also the year when he did the lap and the lap time

```sparql
PREFIX : <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX prs: <https://w3id.org/MON/person.owl#>

SELECT ?pilot ?name ?year (MIN(?lap_time) AS ?best_lap_time ) WHERE {
    ?circuit :name "Circuit de Monaco".
    ?raceWeekend :takePlaceIn ?circuit;
                 :year ?year .
    ?race :during ?raceWeekend;
          :race_fastest_lap ?lap_time.
    ?pilot :hasDrivenIn ?race;
           prs:firstName ?pilotName;
           prs:lastName ?pilotSurname.
    BIND(CONCAT(?pilotName," ", ?pilotSurname) AS ?name)
}
GROUP BY ?pilot ?name ?year
ORDER BY ?best_lap_time
LIMIT 1
```

##### Query 6: Which is the team with the fastest pit-stop in a given race?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?team ?teamName ?fpt WHERE {
    ?drive f1:driveFor ?team.
    ?team f1:name ?teamName.
    ?drive f1:fastest_pitstop ?fpt.
    ?drive f1:during ?rwe . 
            
    ?rwe f1:name "Australian Grand Prix"^^xsd:string . 
    ?rwe f1:year "2019"^^xsd:int 
    FILTER (?fpt = ?fastestPit)
    {
        SELECT (MIN(?fpt) as ?fastestPit) WHERE { 
            ?drive f1:fastest_pitstop ?fpt.
            ?drive f1:during ?rwe . 
            
            ?rwe f1:name "Australian Grand Prix"^^xsd:string . 
            ?rwe f1:year "2019"^^xsd:int
            
        }  
    }
}
```

##### Query 7: Which is the team with the fastest pit-stop in absolute? And with which time?
```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?name ?fpt WHERE { 
	?drive f1:fastest_pitstop ?fpt.
    ?drive f1:driveFor ?cons .
    ?cons f1:name ?name
    
    FILTER (?fpt = ?fastestPit)
    {
        SELECT (MIN(?fpt) as ?fastestPit) WHERE { 
            ?drive f1:fastest_pitstop ?fpt.
        }  
    }
}
```

##### Query 8: Who is the pilot that has won the driver championship in a given year? And with how many points?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX prs: <https://w3id.org/MON/person.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?pilot ?pilotName ?pilotSurname ?maxpoints WHERE{
    ?pilot f1:hasDrivenIn ?drive;
           prs:firstName ?pilotName;
           prs:lastName ?pilotSurname.
    ?drive f1:cp_points_after_race ?maxpoints;
    	   f1:during ?raceWeekend.
    ?raceWeekend f1:year ?year.

    FILTER (?year = "2021"^^xsd:int)
    {
	SELECT ?year (MAX(?points) AS ?maxpoints) WHERE {
		?raceWeekend f1:year ?year .
    	?drive a f1:Drive;
            f1:during ?raceWeekend;
            f1:cp_points_after_race ?points.
	}
        GROUPBY (?year)
	}
}
```

##### Query 9: Which is the team that has won the constructor championship in a given year? And with how many points?

```sparql
    PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?team ?teamName ?maxpoints WHERE {
        ?partecipate f1:cp_points_after_race ?maxpoints;
                    f1:during ?raceWeekend .
        ?raceWeekend f1:year "2016"^^xsd:int .
        ?team f1:participateIn ?partecipate ;
            f1:name ?teamName .
        {
            SELECT (MAX(?points) AS ?maxpoints) WHERE {
            ?raceWeekend f1:year "2016"^^xsd:int .
            ?partecipate a f1:Participate;
                    f1:during ?raceWeekend;
                    f1:cp_points_after_race ?points.
            }
        }
    }
```

##### Query 10: How many races have been done in every nation in a given year?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?nation (COUNT(?raceWeekend) AS ?totalRaces) WHERE {
    ?circuit f1:hasCountry ?nation.
    ?raceWeekend f1:takePlaceIn ?circuit;
                 f1:year "2021"^^xsd:int .
}
GROUP BY ?nation
```

##### Query 11: Which is the final driver championship standing for a given year?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?driver ?name ?surname ?finalPoints WHERE {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_position_after_race ?finalPos ;
           f1:cp_points_after_race ?finalPoints ;
           f1:during ?rwe.

    #Get the result only of the last race of the given year
    FILTER(?rwe = ?race){
        SELECT distinct ?race WHERE {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  FILTER (?round = ?lastRace){
                SELECT (MAX(?round) as ?lastRace) WHERE {
                    ?raceWeekends f1:round ?round;
                                  f1:year "2021"^^xsd:int .
                }
            }
        }
    }

}
ORDER BY desc(?finalPoints)
```

##### Query 12: Which is the driver championship standing after a given race week-end?


```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?driver ?name ?surname ?finalPoints WHERE {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_position_after_race ?finalPos ;
           f1:cp_points_after_race ?finalPoints ;
           f1:during ?rwe.

    ?rwe f1:round "3"^^xsd:int;
         f1:year "2021"^^xsd:int . 

}
ORDER BY desc(?finalPoints)
```

##### Query 13: Which is the driver with the biggest number of points gained in the driver championship? And with how many points?

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?driver ?name ?surname ?finalPoints WHERE {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_points_after_race ?finalPoints . 
    
    FILTER (?finalPoints = ?maxPoints) {
        SELECT (MAX (?points) as ?maxPoints) WHERE {
            ?drive a f1:Drive . 
        	?drive f1:cp_points_after_race ?points 
    	}
    }

}
```

##### Driver Statistics Queries used in our WebApp 

<ol>
    <li>Number of championship that he has won</li>
    <li>For which constructors has driven</li>
    <li>For which constructors did he win a race</li>
    <li>How many seasons</li>
    <li>How many races</li>
    <li>How many pole positions</li>
    <li>How many victories</li>
    <li>How many times finishes in the first 10 position every year (consistency indicator)</li>
    <li>How many times finishes in the first 5 position every year (consistency indicator)</li>
    <li>How many podiums</li>
    <li>Percentage of podiums to total number of races</li>
    <li>Percentage of victories to total number of races</li>
    <li>Best finish in qualifying and race</li>
    <li>Worst finish in qualifying and race</li>
    <li>Number of times it reached Q3</li>
    <li>How many DNF in his career</li>
    <li>number of times that the driver started first and arrived first in a race</li>
    <li>How many points year per year in the championship</li>
    <li>Position year per year in the championship</li>   
    <li>Average points per race in every year</li>
</ol>


##### Query 1

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?wins) WHERE {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
		   f1:hasDrivenIn ?drive .
            
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
```

##### Query 2

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons ?name WHERE { 
 	
    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:driveFor ?cons . 

    ?cons f1:name ?name
    
} 
GROUP BY ?cons ?name 
```

##### Query 3

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons ?name where { 

    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .

    ?drive f1:driveFor ?cons ;
            f1:race_position "1"^^xsd:int . 

    ?cons f1:name ?name .
}  
GROUP BY ?cons ?name
```

##### Query 4

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(DISTINCT ?year) as ?nSeasons)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
	?drive f1:during ?raceWeekend . 
    ?raceWeekend f1:year ?year . 
        
}
```

##### Query 5

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
    
    ?drive a f1:Drive
}
```

##### Query 6

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nPolePosition)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
	?drive f1:quali_position "1"^^xsd:int
}

```
##### Query 7

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nRaceVictories)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
	?drive f1:race_position "1"^^xsd:int
}

```

##### Query 8

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>
SELECT ?year (COUNT(*) as ?top10Finishes) WHERE { 
 	
    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:race_position ?race_pos ; 
    	   f1:during ?rwe .
    
    ?rwe f1:year ?year .
    FILTER (?race_pos <= 10)
    
}  
GROUP BY ?year
ORDER BY ?year
```

##### Query 9

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>
SELECT ?year (COUNT(*) as ?top5Finishes) WHERE { 
 	
    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:race_position ?race_pos ; 
    	   f1:during ?rwe .
    
    ?rwe f1:year ?year .
    FILTER (?race_pos <= 5)
    
}  
GROUP BY ?year
ORDER BY ?year
```

##### Query 10

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nPodiums)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?position .
    FILTER (?position = 1 || ?position = 2 || ?position = 3)
}

```

##### Query 11

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (?nPolePosition / ?nRaces * 100 as ?perc) WHERE { 
    {
        SELECT (COUNT(*) as ?nPolePosition)  WHERE { 
            ?driver person:firstName "Lewis" ;
                    person:lastName "Hamilton" ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:race_position ?position .
       		FILTER (?position = 1 || ?position = 2 || ?position = 3)
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
                ?driver person:firstName "Lewis" ;
                        person:lastName "Hamilton" ;
                        f1:hasDrivenIn ?drive .

                ?drive a f1:Drive
       }
        
    }
}

```

##### Query 12

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (?nVictories / ?nRaces * 100 as ?perc) WHERE { 
    {
        SELECT (COUNT(*) as ?nVictories)  WHERE { 
            ?driver person:firstName "Lewis" ;
                    person:lastName "Hamilton" ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:race_position "1"^^xsd:int
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  WHERE { 
                ?driver person:firstName "Lewis" ;
                        person:lastName "Hamilton" ;
                        f1:hasDrivenIn ?drive .

                ?drive a f1:Drive
       }
        
    }
}

```

##### Query 13

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (MIN(?quali_position) as ?bestQuali) (MIN(?race_position) as ?bestRace)   WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?race_position ; 
    	   f1:quali_position ?quali_position
}

```

##### Query 14

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (MAX(?quali_position) as ?worstQuali) (MAX(?race_position) as ?worstRace)   WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
    ?drive f1:race_position ?race_position ; 
    	   f1:quali_position ?quali_position
}

```

##### Query 15

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(DISTINCT ?drive) as ?q3_quali) WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
    ?drive f1:q3_time ?q3_time
    
} 

```

##### Query 16

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver (COUNT(?drive) as ?dnf) where {

    ?driver person:lastName "Hamilton" .
            person:firstName "Lewis" . 
    ?driver f1:hasDrivenIn ?drive.

    ?drive f1:status ?status.

    #Exclude all the drives that have been completed
    FILTER ( ?status != "Finished" && REGEX(?status, "^(?!.*Lap).*$"))
}
GROUP BY ?driver
```

##### Query 17

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT (COUNT(*) as ?nVictoryFromPole)  WHERE { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
	?drive f1:race_position "1"^^xsd:int . 
    ?drive f1:quali_position "1"^^xsd:int . 
}

```

##### Query 18

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?year ?points WHERE {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
		   f1:hasDrivenIn ?drive .
            
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
```

##### Query 19

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?year ?cp_pos WHERE {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
		   f1:hasDrivenIn ?drive .
            
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
```