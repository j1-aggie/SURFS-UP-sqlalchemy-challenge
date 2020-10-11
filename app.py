from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
#Base.classes.keys()

# Save reference to the tables
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
        f"Welcome to the Climate App API!<br>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#@app.route("/api/v1.0/date/precipitation/<date>")
@app.route("/api/v1.0/date/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation amounts"""
    # Query all precipitation amounts
    #rainfall = session.query(Measurement.date, Measurement.prcp).filter(func.strftime("%y-%m-%d", Measurement.date == date).all()
    last_measurement_data_point = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date == date).all()

    session.close()

 # Create a dictionary from the row data and append to a list of dates and precipitation
    date_precipitation = []
    for date, precipitation in rainfall:
        rainfall_dict = {}
        rainfall_dict["date"] = date
        rainfall_dict["precipitation"] = precipitation
        date_precipitation.append(rainfall_dict)

    return jsonify(date_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query stations
    station_results = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(station_results)


@app.route("/api/v1.0/temperature")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations"""
    # Query last year of temperature observations
    temp_observations = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    tobs_list = []
    for date, temperature_observation in temp_observations:
        temp_observations_dict = {}
        temp_observations_dict["date"] = date
        temp_observations_dict["temperature"] = temperature_observation
        tobs_list.append(temp_observations_dict)

    return jsonify(tobs_list)


@app.route("/api/v1.0/temperature_given_start_date/<date>")
def temperature_given_start_date(date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures"""
    # Query stations
    temperature_given_start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date).all()

    session.close()

    return jsonify(temperature_given_start_date_results)


@app.route("/api/v1.0/temperature_given_start_end/<date_start>/<date_end>")
def temperature_given_start_end(date_start, date_end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures"""
    # Query stations
    temperature_given_start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= date_start).filter(Measurement.date <= date_end).all()

    session.close()

    return jsonify(temperature_given_start_end_results)
# @app.route("/api/v1.0/<start>/<end>")


if __name__ == '__main__':
    app.run(debug=True)