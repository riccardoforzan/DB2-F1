from typing import Union
from fastapi import FastAPI, HTTPException, Form
from SPARQLWrapper import SPARQLWrapper, JSON

app = FastAPI()

sparql = SPARQLWrapper("http://localhost:7200/repositories/formula1")
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
        PREFIX person: <https://w3id.org/MON/person.owl#Person>

        select ?driver (CONCAT(?fn, ' ', ?ln) as ?name) where {
            ?driver a f1:Driver ;
                    person:last_name ?ln ;
                    person:first_name ?fn .
        }
    """

    sparql.setQuery(query)

    try:
        ret = sparql.queryAndConvert()
        return ret["results"]["bindings"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
