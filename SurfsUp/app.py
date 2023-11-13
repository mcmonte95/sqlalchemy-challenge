# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation Query: /api/v1.0/precipitation<br/>"
        f"Stations Query: /api/v1.0/stations<br/>"
        f"Temperature Query (most active station): /api/v1.0/tobs<br/>"
        f"Temperature from Start Date Query (yyyy-mm-dd): /api/v1.0/start<br/>"
        f"Temperature for Date Range Query (yyyy-mm-dd/yyyy-mm-dd): /api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Initialize the session
    session = Session(engine)
    
    # Get the most recent date as well as the date 12 months ago
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).distinct().first()
    most_recent_date = datetime.strptime(most_recent_date[0], "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    twelve_months_ago = most_recent_date - timedelta(days=365)
    
    # Convert back to strings
    most_recent_date = most_recent_date.strftime("%Y-%m-%d")
    twelve_months_ago = twelve_months_ago.strftime("%Y-%m-%d")
    
    # Query the last 12 months of data. 
    # Since we are going straight to a dict, adding Measurement.prcp.isnot(None) filter to query to account for any Null values for precipitation
    last_yr_precip_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= twelve_months_ago).\
        filter(Measurement.prcp.isnot(None)).all()

    # Place results in a dictionary using a dictionary comprehension
    precip_data_dict = {row.date: row.prcp for row in  last_yr_precip_data}
    
    # Close the session
    session.close()
    
    # return the jsonified version of the dictionary
    return jsonify(precip_data_dict)  
            
@app.route("/api/v1.0/stations")
def stations():
    # Initialize the session
    session = Session(engine)
    
    
    # Query for station and then put resi
    station_result = session.query(Station.station).all()
    station_list = [station[0] for station in station_result]  
    
    # Close the session
    session.close()  

    # return the jsonified station list
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_most_active_station():

    # Initialize the session
    session = Session(engine)
    json_list = []
    
    # Retrieve the most active station by
    most_active_station_count = session.query(Measurement.station, func.count(Measurement.id)).\
        join(Station, Station.station == Measurement.station).group_by(Measurement.station).\
        order_by(func.count(Measurement.id).desc()).all() 
    
    most_active_station = most_active_station_count[0][0]

    # Get the most recent date as well as the date 12 months ago
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).distinct().first()
    most_recent_date = datetime.strptime(most_recent_date[0], "%Y-%m-%d")

    # Calculate the date one year from the last date in data set.
    twelve_months_ago = most_recent_date - timedelta(days=365)
    
    # Convert back to strings
    most_recent_date = most_recent_date.strftime("%Y-%m-%d")
    twelve_months_ago = twelve_months_ago.strftime("%Y-%m-%d")
    
    # Query the last 12 months of temp data for the most active station. 
    temp_data_most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= twelve_months_ago).\
        filter(Measurement.station == most_active_station).all()
        
    # put in a list per the challenge question
    temp_data_dict = {row.date: row.tobs for row in  temp_data_most_active_station}   
    json_list.append(temp_data_dict)
    
    # Close the session
    session.close()
    
    # return the jsonified version of the dictionary
    return jsonify(json_list) 

    # Close the session
    session.close() 

    return most_active_station


@app.route("/api/v1.0/<start>")
def temp_start_summary(start):

    # Initialize the engine
    session = Session(engine)
    
    start_date_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    # We need to put in a check to see if the selected date has no data
    if start_date_results and all(value is None for value in start_date_results[0]):
        return jsonify({"Error": "No temperature data found for the given start date"})

    temp_dict = {
        'Min Temp': start_date_results[0][0],
        'Max Temp': start_date_results[0][1],
        'Avg Temp': start_date_results[0][2]
    }
    
    # Close the session
    session.close() 
    
    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def temp_range_summary(start, end):   
    
    # Initialize the engine
    session = Session(engine)
    
    start_date_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # We need to put in a check to see if the selected date has no data
    if start_date_results and all(value is None for value in start_date_results[0]):
        return jsonify({"Error": "No temperature data found for the given start date"})

    temp_dict = {
        'Min Temp': start_date_results[0][0],
        'Max Temp': start_date_results[0][1],
        'Avg Temp': start_date_results[0][2]
    }
    
    # Close the session
    session.close()  
    
    return jsonify(temp_dict)
    
if __name__ == "__main__":
    app.run(debug=True)







