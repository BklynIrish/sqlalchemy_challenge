# Dependencies
import numpy as np
import datetime as dt


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, text, desc

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<br/>"
        f"/api/v1.0/"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query Precipitation data
    annual_rainfall = session.query(Measurement.date,  Measurement.prcp).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_rain = dict(annual_rainfall)

    return jsonify(all_rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations data"""
    # Query a list of all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    max_date = session.query(func.max(Measurement.date)).all()[0][0]
    min_date = dt.datetime.strptime(max_date,'%Y-%m-%d') - dt.timedelta(days = 365)
    Active_Stations = session.query(Station.station ,func.count(Measurement.tobs)).filter(Station.station == Measurement.station).\
    group_by(Station.station).order_by(func.count(Measurement.tobs).desc()).all()


    #Query the dates and temperature observations of the most active station for the last year of data.
    
    
    results_WAHIAWA = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > min_date).\
    filter(Station.station == Active_Stations[0][0]).all()

    session.close()

    # Return a JSON list of temperature observations (TOBS) for the previous year.
    temp_list = list(np.ravel(results_WAHIAWA))
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)