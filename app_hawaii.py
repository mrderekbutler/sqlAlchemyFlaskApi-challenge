import numpy as np
import json as json
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, request, jsonify

#--------------------------------------------------------
# Database Setup
#--------------------------------------------------------
# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

# Declare a Base using `automap_base()'
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Save references to each table 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session (link) from Python to the DB
session = Session(engine)
 
#--------------------------------------------------------
# Flask Setup
#--------------------------------------------------------
app = Flask(__name__)
#--------------------------------------------------------
# Flask Routes
#-------------------------------------------------------
@app.route("/")
def welcome():
        return (  
           f"<h1>Welcome To The Hawaii Weather App</h1>"
           f"<h2>Available Routes</h1>"
           f"<ul>"
                f"<li>/api/v1.0/precipitation</li>"
                f"<li>/api/v1.0/stations</li>"
                f"<li>/api/v1.0/tobs</li>"
                f"<li>/api/v1.0/start</li>"
                f"<li>/api/v1.0/start/end</li>"
                f"</ull>"
                )
        
@app.route("/api/v1.0/precipitation")
def precipitation():
        one_year_ago = "2016-08-23"
        prcp_results = session.query(Measurement.date, Measurement.prcp).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.date).all() 

        prcp_results_dict = []
        for prcp_loop in prcp_results:
                prcp_dict = {}                
                prcp_dict["Date"] = prcp_loop.date 
                prcp_dict["Prcp"] = prcp_loop.prcp
                prcp_results_dict.append(prcp_dict)
        return jsonify(prcp_results_dict)
 
@app.route("/api/v1.0/stations")
def stations():
        station_query = session.query(Station.station).all()
        # Convert list of tuples into normal list
        station_results = list(np.ravel(station_query))
        return jsonify(station_results)

@app.route("/api/v1.0/tobs")
def tobs():
        one_year_ago = "2016-08-23"
        tobs_results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                filter(Measurement.date >= one_year_ago).\
                order_by(Measurement.station, Measurement.date, Measurement.tobs).all()
              
        return jsonify(tobs_results)

@app.route("/api/v1.0/<start>")
def tripa(start):
        tripa_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
        return jsonify(tripa_results)

@app.route("/api/v1.0/<start>/<end>")
def tripb(start,end):
    tripb_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    return jsonify(tripb_results)

#--------------------------------------------------------
# Debug to run app for testing
#--------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)