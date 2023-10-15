# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Home route to list all available routes
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a> - Precipitation data for the last year<br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a> - List of all weather observation stations<br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a> - Temperature observations for the most active station over the last year<br/>"
        f"/api/v1.0/start - Minimum, average, and maximum temperature for a given start date (format: YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end - Minimum, average, and maximum temperature for a given date range (format: YYYY-MM-DD/YYYY-MM-DD)<br/>"
)

# Route for precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    # Querying precipitation data for the last year
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Closing session
    session.close()

    # Converting the query results to a dictionary using date as the key and prcp as the value
    prcp_data_list = {date: prcp for date, prcp in prcp_data}

    # Returning the JSON representation of the dictionary
    return jsonify(prcp_data_list)

# Route for stations data
@app.route("/api/v1.0/stations")
def stations():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    # Querying all stations
    stations = session.query(Station.station).all()

    # Closing session
    session.close()

    # Unraveling station results into a one-dimensional array and converting to a list
    stations_list = list(np.ravel(stations))

    # Returning JSON list of stations
    return jsonify(stations_list)

# Route for temperature observations (tobs) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # Creating session (link) from Python to the DB
    session = Session(engine)

    # Querying the dates and temperature observations of the most active station for the last year of data
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    # Closing session
    session.close()

    # Unraveling results into a one-dimensional array and converting to a list
    tobs_list = list(np.ravel(results))

    # Returning JSON list of temperature observations (TOBS) for the previous year
    return jsonify(tobs_list)

# Route for temperature statistics from a start date
@app.route("/api/v1.0/<start>")
def start(start):
    # Creating session (link) from Python to the DB
    session = Session(engine)

    # Querying min, max, and avg temperature from a start date
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    # Closing session
    session.close()

    # Converting the query results to a list
    temp_stats_list = list(np.ravel(temp_stats))

    # Returning JSON list of min, max, and avg temperature from the start date
    return jsonify(temp_stats_list)

# Route for temperature statistics from start date to end date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Creating session (link) from Python to the DB
    session = Session(engine)

    # Querying min, max, and avg temperature from start date to end date
    temp_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    # Closing session
    session.close()

    # Converting the query results to a list
    temp_stats_list = list(np.ravel(temp_stats))

    # Returning JSON list of min, max, and avg temperature from start date to end date
    return jsonify(temp_stats_list)

#################################################
# Run the Flask App
#################################################
if __name__ == '__main__':
    app.run(debug=True)