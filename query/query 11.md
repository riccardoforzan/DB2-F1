
11) Driver statistics: For a given driver:  
	- How many DNF in his career
	- how many pole positions and victories
	- percentage of podiums with respect to the total number of races
	- number of times that the driver started first and arrived first in a race
	- average number of points for every race
	- number of championship that he has won 
	- number of season that he has done


##### 11.1
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