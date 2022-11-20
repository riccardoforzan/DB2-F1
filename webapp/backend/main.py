from typing import Union
from fastapi import FastAPI, HTTPException, Form
from SPARQLWrapper import SPARQLWrapper, JSON
from fastapi.middleware.cors import CORSMiddleware
import stats 

# Create FastAPI endpoint and allow all origins
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up the SPARQLWrapper to perform queries in GraphDB
# Riccardo sparql = SPARQLWrapper("http://localhost:7200/repositories/formula1")

# Manuel sparql = SPARQLWrapper("http://manuelubuntu:7200/repositories/Formula1")
sparql = SPARQLWrapper("http://localhost:7200/repositories/DB2Project")

sparql.setMethod('POST')
sparql.setReturnFormat(JSON)

@app.post("/query")
def execute_raw_query(query: str = Form()):
    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
        return ret["results"]["bindings"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drivers")
def get_drivers():

    query = """
        PREFIX f1: <http://www.dei.unipd.it/database2/Formula1Ontology#>
        PREFIX person: <https://w3id.org/MON/person.owl#>

        select ?driver (CONCAT(?fn, ' ', ?ln) as ?name) where {
            ?driver a f1:Driver ;
                    person:lastName ?ln ;
                    person:firstName ?fn .
        }
    """

    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
        return ret["results"]["bindings"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drivers/{driverURI}/stats")
async def get_driver_stat(driverURI):
    driverStats = stats.driverStats(sparql, driverURI)
    return driverStats
 