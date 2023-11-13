# sqlalchemy-challenge

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii. To help with your trip planning, you decide to do a climate analysis about the area. 

In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib. You will also design a Flask API based on the queries that you just developed.

### Repository Guide:
This repository contains 2 main components:
  1. A folder called 'SurfsUp' which contains 2 files:
  - A jupyter notebook file called "climate_final.ipynb" which contains the inital SQLAlchemy queries and plots for analyzing the climate data in the hawaii sqlite database
  - A python file called 'app.py' which is the code to initialize the Flask API that also queries the hawaii sqlite database and returns climate information in JSON format
  2. A 'Resources' folder which contains the hawaii.sqlite database file as well as two csv files that represent the two tables that are included in the sqlite database

### Climate API Guide:

API routes
 
Precipitation Query: /api/v1.0/precipitation
Stations Query: /api/v1.0/stations
Temperature Query (most active station): /api/v1.0/tobs
Temperature from Start Date Query (yyyy-mm-dd): /api/v1.0/start
Temperature for Date Range Query (yyyy-mm-dd/yyyy-mm-dd): /api/v1.0/start/end
