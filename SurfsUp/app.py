# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt




#################################################
# Database Setup
#################################################

# Create our session (link) from Python to the DB
engine = create_engine("sqlite:////Users/tomwildun/Documents/UTA-VIRT-DATA-PT-06-2023-U-LOLC/02-Homework/10-Advanced-SQL/Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
#Base.prepare(autoload_with=engine)


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
#   Define Routes for homepage
@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#   Define Route for Precipitation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()
    prcp_dict = {date: prcp for date, prcp in prcp_data}
    return jsonify(prcp_dict)

#   Define route for Stations Data
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    return jsonify(stations)

#   Define route for Tempurature Data
@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    start_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).\
        order_by(func.count().desc()).first()[0]
    
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= start_date).all()
        
    return jsonify(temperature_data)

# Define route for result
@app.route("/api/v1.0/<start>")
def start_date(start):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    return jsonify(result)

#   Define route start end 
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start, end)).all()
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)