import os
from dotenv import load_dotenv
from SPARQLWrapper import SPARQLWrapper, JSON
from utils import driverStats 

#Read env file
load_dotenv()
SPARQL_ENDPOINT_URL = os.getenv('SPARQL_ENDPOINT_URL')
EXPOSED_PORT = int(os.getenv('EXPOSED_PORT'))

# Set up the SPARQLWrapper to perform queries in GraphDB
sparql = SPARQLWrapper(SPARQL_ENDPOINT_URL)
sparql.setMethod('POST')
sparql.setReturnFormat(JSON)

if __name__ == "__main__":
    stats = driverStats(sparql, 1)
    print(stats)