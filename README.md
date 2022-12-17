# Database 2 - Group project

This repository is created by the group Marideal at the University of Padua for the Database 2 course group project. 

The purpose of the project is to identify a big dataset regarding a specific topic (in our case the Formula 1 races and championships), extract the main data and model an ontology based on that data.

After that the ontology will be imported into GraphDB and some SPARQL queries will be run to obtain some usefull information about the topic. 

At the end we developed also a WebApp for showing some driver statistics. 

# Outline:
- Group Members
- Datasets
- Ontology
- Data Ingestion
- Queries
- Web Application

## Group members
| Surname      | Name          | ID            |
| ------------ | ------------- | ------------- |
| Barusco      | Manuel        | 2053083       |
| Forzan       | Riccardo      | 2057453       |
| Lotta        | Alessandro    | 2054786       |
| Mansouri     | Delaram       | 2044016       |

## Dataset

The datasets used for this project are :

- [Formula 1 World Championship (1950 - 2022) F1 race data from 1950 to 2022](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) 
- [Formula 1 Race Fan Ratings](https://www.kaggle.com/datasets/codingminds/formula-1-race-fan-ratings)

These datasets are open datasets. 

From these datasets we extracted only the data of interest and we performed only a small pre-processing phase for removing some <code>NULL</code> values and for formatting the lap times.

You can find all the datasets .csv files in the /data folder. 

The first dataset contains all the main F1 race data information from 1950 to 2022 and the second dataset contains the fans race ratings of some races (from 2008 to 2018).

## Ontology

In the <code>/ontology</code> directory you can find the final ontology that we developed for the project. 

You can find a visual file of the ontology and a <code>.owl</code> file that can be opened with Protege.

The final <code>.ttl</code> file with all the inferred triples is saved in the <code>/rdf</code> directory and is called (<code>Formula1Populated.ttl</code>). 

## Data Ingestion

The Data Ingestion phase is implemented by using a Jupyter Notebook that you can find in the main folder. 

In this file are described and commented all the data ingestion phases from the extraction and pre-processing of the data to the production of the <code>.ttl</code> files. 

All the produced <code>.ttl</code> files are saved int the <code>/rdf</code> directory. 

## Queries

All the queries that we want to perform on our Database are saved in the <code>Queries.md</code> file. 

For all the queries we present the purpose of the query and the code. 

There are 13 main queries and then other queries that we use in our WebApp for retrieving some driver statistics. 

If you want to run these queries in your GraphDB instance you can upload all the <code>.ttl</code> files contained in the <code>/rdf</code> directory.

## WebApp
You can find instructions inside the [README.md](./webapp/README.md)