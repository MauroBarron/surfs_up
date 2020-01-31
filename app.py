# %%
# 9.5.1: Set Up the Database and Flask

## Dependencies
# Standard
import datetime as dt
import numpy as np
import pandas as pd

#SqlAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#FLASK
from flask import Flask, jsonify

## Set up Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base=automap_base()
Base.prepare(engine, reflect=True)

## Save Reflected References as Clasees for further use
Measurement = Base.classes.measurement
Station = Base.classes.station

## Create a session link from Python to the SQLite database
session=Session(engine)

# %%
#  Set Up Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#localhost:5000/

@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
    
    #localhost:5000/api/v1.0/precipitation

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

    #localhost:5000/api/v1.0/stations

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    temps = list(np.ravel(results))
	
    return jsonify(temps)

    #localhost:5000/api/v1.0/tobs

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#def stats(start=None, end=None):
#def stats(start, end):    
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
	    results = session.query(*sel).filter(Measurement.date <= start).all()
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)

     #localhost:5000/api/v1.0/start/end
    #http://127.0.0.1:5000/api/v1.0/temp/2017-06-01/2017-06-30
