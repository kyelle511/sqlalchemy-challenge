# Import the dependencies.
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session=Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start/<start> <br/>"
        f"/api/v1.0/startend/<start>/<end> <br/>"
        f"<br/><br/>"
        f"enter dates: YYYYMMDD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create our session from Python to the DB
    session = Session(engine)

    #Query the last 12 months of data of precipitation data and close the session
    results=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > dt.date(2016,8,23))

    session.close()

    # Create a dictionary from the row data and append to list
    precipitation_data = []

    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict['date'] = date
        precipitation_dict['prcp'] = prcp
        precipitation_data.append(precipitation_dict)

    return precipitation_data

@app.route("/api/v1.0/stations")
def stations():
    #Create our session from Python to the DB
    session = Session(engine)

    #Query the last 12 months of data of precipitation data and close the session
    results=session.query(Measurement.station).group_by(Measurement.station).all()

    session.close()

    # Create a list of all stations
    stations= list(np.ravel(results))

    return stations

@app.route("/api/v1.0/tobs")
def tobs():
    #Create our session from Python to the DB
    session = Session(engine)

    #Query the dates and temperature observations of the most-active station for the previous year of data and close the session
    station_year=session.query(Measurement.date,Measurement.tobs).\
            filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date > dt.date(2016,8,23)).all()
    
    session.close()

    # Create a dictionary from the row data and append to list
    station_data = []

    for date, tobs in station_year:
        station_dict = {}
        station_dict['date'] = date
        station_dict['tobs'] = tobs
        station_data.append(station_dict)

    return station_data

@app.route("/api/v1.0/start/<start>")
def date_temps(start):
    """"Fetch the minimum temperature, average termpartere and maximum temperature for a specified start date"""
    #Create our session from Python to the DB
    session = Session(engine)

    #Create a format for the date string
    date_format='%Y%m%d'

    # Query based on the start date and close the session
    # I used: https://stackoverflow.com/questions/19480028/attributeerror-datetime-module-has-no-attribute-strptime
    start_date=session.query(Measurement.tobs).\
                filter(Measurement.date >= dt.datetime.strptime(start, date_format)).all()
    
    session.close()

    # Create a list of min, avg and max temps
    start_date_dict={}
    start_date_dict['min'] = np.min(start_date)
    start_date_dict['avg'] = np.mean(start_date)
    start_date_dict['max'] = np.max(start_date)

    return start_date_dict
    
@app.route("/api/v1.0/startend/<start>/<end>")
def enddate_temps(start, end):
    """"Fetch the minimum temperature, average termpartere and maximum temperature for a specified start date and end date"""
    #Create our session from Python to the DB
    session = Session(engine)

    # Create date format
    date_format='%Y%m%d'

    # Query based on the start date and end date, close the session
    
    end_date=session.query(Measurement.tobs).\
                filter(Measurement.date >= dt.datetime.strptime(start, date_format)).\
                filter(Measurement.date < dt.datetime.strptime(end, date_format)).all()
    
    session.close()

    #Create a dictionary of the min, avg, and max temperatures for the start and end date range entered
    end_date_dict={}
    end_date_dict['min'] = np.min(end_date)
    end_date_dict['avg'] = np.mean(end_date)
    end_date_dict['max'] = np.max(end_date)

    return end_date_dict
    
if __name__ == '__main__':
    app.run(debug=True)
 