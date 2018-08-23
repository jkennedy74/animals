# dependencies
from flask import (
    Flask, 
    jsonify, 
    render_template, 
    redirect)

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, load_only
from sqlalchemy import create_engine, func
from flask_sqlalchemy import SQLAlchemy

import numpy as np
import pandas as pd
import time
import datetime

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data/animalData.sqlite"
db = SQLAlchemy(app)

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(db.engine, reflect=True)

# Assign the demographics class to a variable called `Demographics`
Animals = Base.classes.animals

# base route
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# route for returning all class names
@app.route("/classes")
def classes():
    """Return a list of sample names."""

    # results of the query
    results = db.session.query(Animals.s_class).all()

    # empty list to append data to
    class_names = []

    # loop to append relevant data
    for result in results:
        class_names.append(result[0])

    # return a set of unique values in the list
    class_set = set(class_names)

    # change the set back to a list
    class_names = list(class_set)

    # remove items that are not needed
    class_names.remove("s_class")
    class_names.remove("")
    class_names.remove("Hutter_Madagascar_2016_2016-11-21_12:33")

    # sort the list
    class_names.sort()

    return jsonify(class_names)

# route for returning animal geojson
@app.route("/geojson/<s_class>")
def animal_geojson(s_class):
    """Return the MetaData for a given sample."""

    # Selection to query
    sel = [
        Animals.id,
        Animals.eventDate, 
        Animals.country,
        Animals.decimalLatitude,
        Animals.decimalLongitude,
        Animals.s_class]

    # results of the query
    results = db.session.query(*sel).filter(Animals.s_class==s_class).order_by(Animals.eventDate)

    # empty list to append data to
    FeatureCollection = {"type": "FeatureCollection",
                "metadata": {
                "title": "Animal Counts"
                }}

    Features = []

    # loop to append relevant data
    for result in results:
        if result[3] != "" and result[4] != "" and int(result[1][0:4]) > 1999 and int(result[1][0:4]) < 2013:
            feature = {
                "type": "Feature",
                "properties": {
                "place": result[2],
                "year": result[1][0:4],
                "start": time.mktime(datetime.datetime.strptime(f"{int(result[1][0:4])}-01-01", "%Y-%m-%d").timetuple()),
                "end": time.mktime(datetime.datetime.strptime(f"{int(result[1][0:4])}-12-31", "%Y-%m-%d").timetuple()),
                "type": result[5]
                },
                "geometry": {
                "type": "Point",
                "coordinates": [
                float(result[4]),
                float(result[3])
                ]
                },
                "id": int(result[0])
            }
            
            Features.append(feature)

    FeatureCollection["features"] = Features

    return jsonify(FeatureCollection)

# route for returning sample metadata
@app.route("/year/<s_class>")
def animal_year(s_class):
    """Return the MetaData for a given sample."""

    # Selection to query
    sel = [
        Animals.eventDate]

    # results of the query
    results = db.session.query(*sel).filter(Animals.s_class==s_class)

    # empty list to append data to
    years = []

     # loop to append relevant data
    for result in results:
        years.append(result[0][0:4])

    # return a set of unique values in the list
    year_set = set(years)

    # change the set back to a list
    years = list(year_set)

    # sort the list
    years.sort()

    return jsonify(years)


if __name__ == "__main__":
    app.run(debug=True)