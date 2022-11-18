from SPARQLWrapper import SPARQLWrapper, JSON
import queries as qrs

sparql = SPARQLWrapper(
     "http://manuelubuntu:7200/repositories/Formula1"
     )
sparql.setReturnFormat(JSON)

#set driver name and surname in the queries

driverName = "Lewis"
driverSurname = "Hamilton"

for i in range(0, len(qrs.queries)) :
    query = qrs.queries[i]
    query = query.replace(" NAME ", driverName)
    query = query.replace(" SURNAME ", driverSurname)
    qrs.queries[i] = query

sparql.setQuery(qrs.queries[0])

#add query 1: number of driver championship win

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats = {'cp_win' : r["wins"]["value"]} 
except Exception as e:
    print(e)

#add query 2: number constructors for which the driver has driven

sparql.setQuery(qrs.queries[1])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    cons = [] 
    for row in r: 
        cons.append(row["name"]["value"])
    stats["constructor"] = cons 

except Exception as e:
    print(e)

#add query 3: constructors for which the driver has won a race

sparql.setQuery(qrs.queries[2])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    cons = [] 
    for row in r: 
        cons.append(row["name"]["value"])
    stats["constructor_win"] = cons 

except Exception as e:
    print(e)

#add query 4: how many seasons

sparql.setQuery(qrs.queries[3])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['season_number'] = r["nSeasons"]["value"]

except Exception as e:
    print(e)

#add query 5: how many races

sparql.setQuery(qrs.queries[4])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['races_number'] = r["nRaces"]["value"]

except Exception as e:
    print(e)

#add query 6: how many pole positions

sparql.setQuery(qrs.queries[5])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['pole_number'] = r["nPolePosition"]["value"]

except Exception as e:
    print(e)

#add query 7: how many victories

sparql.setQuery(qrs.queries[6])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['victories_number'] = r["nRaceVictories"]["value"]

except Exception as e:
    print(e)

#add query 8: How many times finishes in the first 10 position every year

sparql.setQuery(qrs.queries[7])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    first_10 = {} 
    for row in r: 
        first_10[row["year"]["value"]] = row["top10Finishes"]["value"] 
    stats["top_10_year"] = first_10

except Exception as e:
    print(e)

#add query 9: How many times finishes in the first 5 position every year

sparql.setQuery(qrs.queries[8])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    first_5 = {} 
    for row in r: 
        first_5[row["year"]["value"]] = row["top5Finishes"]["value"] 
    stats["top_5_year"] = first_5

except Exception as e:
    print(e)

#add query 10: How many podiums

sparql.setQuery(qrs.queries[9])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['podiums'] = r["nPodiums"]["value"]

except Exception as e:
    print(e)

#add query 11: Percentage of podiums to total number of races

sparql.setQuery(qrs.queries[10])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['perc_pod_races'] = r["perc"]["value"]

except Exception as e:
    print(e)

#add query 12: How many times finishes in the first 10 position every year

sparql.setQuery(qrs.queries[11])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['perc_vic_races'] = r["perc"]["value"]

except Exception as e:
    print(e)

#add query 13: Best finish in qualifying and race

sparql.setQuery(qrs.queries[12])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['best_quali'] = r["bestQuali"]["value"]
    stats['best_race'] = r["bestRace"]["value"]

except Exception as e:
    print(e)

#add query 14: Worst finish in qualifying and race

sparql.setQuery(qrs.queries[13])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['worst_quali'] = r["worstQuali"]["value"]
    stats['worst_race'] = r["worstRace"]["value"]

except Exception as e:
    print(e)

#add query 15: Number of times it reached Q3

sparql.setQuery(qrs.queries[14])


try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['q3_quali'] = r["q3_quali"]["value"]

except Exception as e:
    print(e)

#add query 16: Number of DNF

sparql.setQuery(qrs.queries[15])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['dnf'] = r["dnf"]["value"]

except Exception as e:
    print(e)

#add query 17: number of times that the driver started first and arrived first in a race

sparql.setQuery(qrs.queries[16])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"][0] 
    stats['victory_from_pole'] = r["nVictoryFromPole"]["value"]

except Exception as e:
    print(e)

#add query 18: How many points year per year in the championship

sparql.setQuery(qrs.queries[17])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    points_year = {} 
    for row in r: 
        points_year[row["year"]["value"]] = row["points"]["value"] 
    stats["points_year"] = points_year

except Exception as e:
    print(e)


#add query 19: Position year per year in the championship

sparql.setQuery(qrs.queries[18])

try:
    ret = sparql.queryAndConvert()
    
    r = ret["results"]["bindings"]
    position_year = {} 
    for row in r: 
        position_year[row["year"]["value"]] = row["cp_pos"]["value"] 
    stats["position_year"] = position_year

except Exception as e:
    print(e)

print(stats)
