import os
import uvicorn
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, Form
from SPARQLWrapper import SPARQLWrapper, JSON
from fastapi.middleware.cors import CORSMiddleware
from utils import driver_stats

#Read env file
load_dotenv()
SPARQL_ENDPOINT_URL = os.getenv('SPARQL_ENDPOINT_URL')
EXPOSED_PORT = int(os.getenv('EXPOSED_PORT'))

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
sparql = SPARQLWrapper(SPARQL_ENDPOINT_URL)
sparql.setMethod('POST')
sparql.setReturnFormat(JSON)

@app.post("/query")
def execute_raw_query(query):
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
def get_driver_stat(driverURI):    
    stats = driver_stats(sparql, driverURI)
    return jsonable_encoder(stats)
 
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=EXPOSED_PORT)