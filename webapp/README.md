# WebApp

The web application we developed is composed by two parts:

* Backend
* Frontend

# Backend

Our backend has been developed in Python using FastAPI. 

The code is contained in the `backend` sub directory. 

In order to run the backend successfully you have to:
1) Copy the file `.env.example` and rename it to `.env`
2) Set the `SPARQL_ENDPOINT_URL` variable inside the file
3) Run the backend app `python main.py` (you may need to install missing requirements)

In details, we used as database GraphDB. 
We loaded our ontology, then we used the URL provided by GraphDB to query the database: `http://localhost:7200/repositories/formula1`

At the URL `127.0.0.1:PORT/docs` you can find the documentation of our REST endpoint, documented using [Swagger](https://swagger.io/) that implements the [OpenAPI specification](https://swagger.io/specification/)

# Frontend

When the backend is up and running you can start the frontend.

Our frontend has been developed using HTML, Bootstrap 5 and Javascript.

The `index.html` page queries the backend endpoint asking for all drivers in our database.

Then you can select a specific driver in the select (you can also search by starting typing).

When you select a driver two queries are issued to the backend:
* A first one to retrieve some basic data about driver
* A second one to retrieve data that are used to populate charts
