# Queries

<ol>
<li>How many pole positions has a given pilot done on a given year?</li>
<li>How many races has a given pilot won in a given year?</li>
<li>Who is the pilot with the biggest number of race victory?</li>
<li>Which is the team with the biggest number of victories of the constructor championship?</li>
<li>Which is the pilot with the biggest number of victories of the driver championship?</li>
<li>Who is the pilot with the best lap time in a given circuit?</li>
<li>Which is the team with the fastest pit-stop in a given race?</li>
<li>Which is the team with the fastest pit-stop in absolute?</li>
<li>Who is the pilot that has won the driver championship in a given year?</li>
<li>Which is the team that has won the constructor championship in a given year?</li>
<li>How many races have been done in a given nation in a given year?</li>
<li>Which is the final driver championship standing for a given year?</li>
<li>Which is the driver championship standing after a given race week-end?</li>
<li>Which is the driver with the biggest number of points gained in the driver championship?</li>
</ol>

Driver statistics for our web app: For a given driver:
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
    
Constructor statistics: For a given constructor:
    <ol>
        <li>Number of championship that he has won</li>
        <li>Number of races</li>
        <li>Number of race win</li>
        <li>Number of podiums </li>
        <li>Number of pole positions</li>
        <li>Fastest pit-stop</li>
        <li>How many dnf for every year</li>
        <li>How many top 5 finish for every year</li>
        <li>How many top 10 finish for every year</li>
    </ol>
</ol>


---

##### Query 1

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX person: <https://w3id.org/MON/person.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?drive) as ?pole_positions) where {

    ?driver person:firstName "Lewis"^^xsd:string ;
            person:lastName "Hamilton"^^xsd:string ;
            f1:hasDrivenIn ?drive .

    ?drive f1:quali_position "1"^^xsd:int ;
   	       f1:during ?race_weekend .

    ?race_weekend f1:year "2021"^^xsd:int .

}
```

##### Query 2

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX person: <https://w3id.org/MON/person.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT (COUNT(DISTINCT ?drive) as ?pole_positions) where {

    ?driver person:firstName "Lewis"^^xsd:string ;
            person:lastName "Hamilton"^^xsd:string ;
            f1:hasDrivenIn ?drive .

    ?drive f1:race_position "1"^^xsd:int ;
           f1:during ?race_weekend .

    ?race_weekend f1:year "2021"^^xsd:int .

}
```

##### Query 3

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?driver ?name ?last_name(COUNT(*) as ?number_victory)  where {

    ?driver person:firstName ?name ;
            person:lastName ?last_name . 
    ?driver f1:hasDrivenIn ?drive .
    ?drive f1:race_position "1"^^xsd:int .
}
GROUP BY ?driver ?name ?last_name
ORDER BY DESC (?number_victory) 
LIMIT 1
```

##### Query 4

```sparql
PREFIX dbpedia_f1: <https://dbpedia.org/ontology/FormulaOneTeam#>
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

select ?team ?teamName (COUNT(?team) as ?wins) where {

    ?team rdf:type dbpedia_f1:FormulaOneTeam;
          f1:name ?teamName.

    ?team f1:participateIn ?part.
    ?part f1:cp_position_after_race ?finalPos.
    ?part f1:during ?rwe.

    #Get the result only of the last race of the year
    FILTER(?rwe = ?race){
        select distinct ?race where {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  f1:year ?y;
                  FILTER (?round = ?lastRace && ?y = ?year){
                select (MAX(?round) as ?lastRace) ?year where {
                    ?raceWeekends a f1:RaceWeekend;
                                  f1:round ?round;
                                  f1:year ?year.
                }
                group by ?year
                order by asc(?year)
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

##### Query 5 AA

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver ?name ?surname (COUNT(?driver) as ?wins) where {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_position_after_race ?finalPos ;
           f1:during ?rwe.

    #Get the result only of the last race of the year
    FILTER(?rwe = ?race){
        select distinct ?race where {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  f1:year ?y;
                  FILTER (?round = ?lastRace && ?y = ?year){
                select (MAX(?round) as ?lastRace) ?year where {
                    ?raceWeekends a f1:RaceWeekend;
                                  f1:round ?round;
                                  f1:year ?year.
                }
                group by ?year
                order by asc(?year)
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

##### Query 6

```sparql
PREFIX : <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX prs: <https://w3id.org/MON/person.owl#>

select ?pilot ?name ?year (MIN(?lap_time) AS ?best_lap_time ) where {
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
LIMIT 100
```

##### Query 7

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>

select ?team ?teamName where {
    ?drive f1:driveFor ?team.
    ?team f1:name ?teamName.
    {
        select ?drive (MIN(?fpt) as ?fastestPit) where { 
            ?drive a f1:Drive;
                f1:fastest_pitstop ?fpt.
            ?drive f1:driveFor ?team. 
        }
        group by ?drive
    }
}
```

##### Query 8

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
select (MIN(?pt) as ?absFastestPit) where { 
	?drive a f1:Drive;
        f1:fastest_pitstop ?pt.
}
```

##### Query 9

```sparql
PREFIX : <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX prs: <https://w3id.org/MON/person.owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

select DISTINCT ?pilot ?pilotName ?pilotSurname ?maxpoints where{
    ?pilot :hasDrivenIn ?drive;
           prs:firstName ?pilotName;
           prs:lastName ?pilotSurname.
    ?drive :cp_points_after_race ?maxpoints;
    		:during ?raceWeekend.
    ?raceWeekend :year ?year.

    FILTER (?year = "2021"^^xsd:int)
    {
	select ?year (MAX(?points) AS ?maxpoints) where {
		?raceWeekend :year ?year .
    	?drive a :Drive;
            :during ?raceWeekend;
            :cp_points_after_race ?points.
	}
        GROUPBY (?year)
	}
}
```

##### Query 10

```sparql
PREFIX : <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
select ?team ?teamName ?maxpoints where {
    ?partecipate :cp_points_after_race ?maxpoints;
                 :during ?raceWeekend .
    ?raceWeekend :year "2016"^^xsd:int .
    ?team :participateIn ?partecipate ;
          :name ?teamName .
	{
        select (MAX(?points) AS ?maxpoints) where {
		?raceWeekend :year "2016"^^xsd:int .
    	?partecipate a :Participate;
                :during ?raceWeekend;
        	    :cp_points_after_race ?points.
	}
}
```

##### Query 11

```sparql
PREFIX : <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX countries: <http://eulersharp.sourceforge.net/2003/03swap/countries#>

select (COUNT(?raceWeekend) AS ?totalRaces) where {
    ?circuit :hasCountry countries:us.
    ?raceWeekend :takePlaceIn ?circuit;
                 :year "2000"^^xsd:int .
}
```

##### Query 12

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver ?name ?surname ?finalPoints where {

    ?driver person:firstName ?name ;
            person:lastName ?surname . 

    ?driver f1:hasDrivenIn ?drive.
    ?drive f1:cp_position_after_race ?finalPos ;
           f1:cp_points_after_race ?finalPoints ;
           f1:during ?rwe.

    #Get the result only of the last race of the given year
    FILTER(?rwe = ?race){
        select distinct ?race where {
            ?race a f1:RaceWeekend;
                  f1:round ?round;
                  FILTER (?round = ?lastRace){
                select (MAX(?round) as ?lastRace) where {
                    ?raceWeekends f1:round ?round;
                                  f1:year "2021"^^xsd:int .
                }
            }
        }
    }

}
ORDER BY desc(?finalPoints)
```

##### Query 13

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver ?name ?surname ?finalPoints where {

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
##### Query 14

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?driver ?name ?surname ?finalPoints where {

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

##### Driver Statistics 

##### Query 1

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select (COUNT(*) as ?wins) where {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
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

}
```

##### Query 2

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons where { 
 	
    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:driveFor ?cons . 
    
} 
GROUP BY ?cons 
```

##### Query 3

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

SELECT ?cons where { 
 	
    ?driver person:firstName "Lewis" ; 
            person:lastName "Hamilton" ; 
            f1:hasDrivenIn ?drive .
    
    ?drive f1:driveFor ?cons ;
    		f1:race_position "1"^^xsd:int 
    
} 
GROUP BY ?cons 
```

##### Query 4

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(DISTINCT ?year) as ?nSeasons)  where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(*) as ?nPolePosition)  where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(*) as ?nPolePosition)  where { 
 	?driver person:firstName "Lewis" ;
            person:lastName "Hamilton" ;
			f1:hasDrivenIn ?drive .
	?drive f1:race_position "1"^^xsd:int
}

```

##### Query 8

```sparql
SELECT ?year (COUNT(*) as ?top5Finishes) where { 
 	
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
SELECT ?year (COUNT(*) as ?top5Finishes) where { 
 	
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(*) as ?nPolePosition)  where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (?nPolePosition / ?nRaces * 100 as ?perc) where { 
    {
        SELECT (COUNT(*) as ?nPolePosition)  where { 
            ?driver person:firstName "Lewis" ;
                    person:lastName "Hamilton" ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:quali_position "1"^^xsd:int
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
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

SELECT (?nVictories / ?nRaces * 100 as ?perc) where { 
    {
        SELECT (COUNT(*) as ?nVictories)  where { 
            ?driver person:firstName "Lewis" ;
                    person:lastName "Hamilton" ;
                    f1:hasDrivenIn ?drive .
            ?drive f1:race_position "1"^^xsd:int
        }
    } 
    {
        SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (MIN(?quali_position) as ?bestQuali) (MIN(?race_position) as ?bestRace)   where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (MAX(?quali_position) as ?bestQuali) (MAX(?race_position) as ?bestRace)   where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(DISTINCT ?drive) as ?q3_quali) where { 
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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

select ?driver (COUNT(?drive) as ?dnf) where {
    ?driver a f1:Driver;
            f1:hasDrivenIn ?drive.

    ?drive f1:status ?status.

    #Get the driver which last name is
    ?driver person:last_name "Bottas" .

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
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT(*) as ?nVictoryFromPole)  where { 
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

select ?year ?points where {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
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
```

##### Query 19

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select ?year ?cp_pos where {

    ?driver person:firstName "Lewis" ;
    	   person:lastName "Hamilton" ; 
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
ORDER BY ?year
```

##### Constructor Statistics 

##### Query 1

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#>

select (COUNT(*) as ?wins) where {

                             
    ?drive f1:cp_position_after_race "1"^^xsd:int;
           f1:during ?rwe;
    	   f1:driveFor ?cons.
    
    ?cons  f1:name "McLaren".
    


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
```

##### Query 2
```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT( DISTINCT *) as ?nRaces)  where { 
    ?cons  f1:name "McLaren".
    ?drive f1:driveFor ?cons.
     	   
}
```

##### Query 3
```sparql

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT( DISTINCT *) as ?nWinRaces)  where { 
    ?cons  f1:name "McLaren".
    ?drive f1:driveFor ?cons.
    ?drive f1:race_position ?position .
    FILTER (?position = 1)
} 
```

##### Query 4
```sparql

PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX person: <https://w3id.org/MON/person.owl#Person>

SELECT (COUNT( DISTINCT *) as ?nWinRaces)  where { 
    ?cons  f1:name "McLaren".
    ?drive f1:driveFor ?cons.
    ?drive f1:race_position ?position .
    FILTER (?position = 1 || ?position = 2 || ?position = 3)
} 
```