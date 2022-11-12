4) Which is the team with the biggest number of victories of the constructor championship?

##### Final query

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
```

___

##### Get the last race of every year

```sparql
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
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
```

##### Get all the race week ends in which a constructor has participated

```sparql
PREFIX dbpedia_f1: <https://dbpedia.org/ontology/FormulaOneTeam#>
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

select distinct ?rwe where {
    ?team rdf:type dbpedia_f1:FormulaOneTeam.
    ?team f1:participateIn ?part.
    ?part f1:during ?rwe.
}
```

##### Get the position of the team at a given race

```sparql
PREFIX dbpedia_f1: <https://dbpedia.org/ontology/FormulaOneTeam#>
PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

select distinct ?team ?rwe ?part ?teamName ?finalPos where {
    ?team rdf:type dbpedia_f1:FormulaOneTeam;
          f1:name ?teamName.
    
    ?team f1:participateIn ?part.
    ?part f1:cp_position_after_race ?finalPos.
    
    ?part f1:during ?rwe.
    FILTER(?rwe = f1:raceWeekEnd1009)
}
order by asc(?finalPos)
```
