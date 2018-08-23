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
Animals = Base.classes.animalsNew
AnimalsCount = Base.classes.animalsPivot

# base route
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# route for returning all class names
@app.route("/classes")
def classes():
    """Return a list of class names."""

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

    # sort the list
    class_names.sort()

    return jsonify(class_names)

# route for returning all species names
@app.route("/species")
def species():
    """Return a list of species names."""
    # Selection to query
    sel = [ 
        Animals.species,
        Animals.year]

    # results of the query
    results = db.session.query(*sel).all()

    # empty list to append data to
    species_names = []

    # loop to append relevant data
    for result in results:
        if result[1] != "year" and int(result[1]) > 2009 and int(result[1]) < 2018:
            species_names.append(result[0])

    # return a set of unique values in the list
    species_set = set(species_names)

    # change the set back to a list
    species_names = list(species_set)

    # remove items that are not needed
    species_names.remove("")

    # sort the list
    species_names.sort()

    return jsonify(species_names)

#route for returning animal geojson
@app.route("/metadata/<species>")
def animal_metadata(species):
    """Return the MetaData for a given species"""

    # Selection to query
    sel = [
        Animals.s_class, 
        Animals.species,
        Animals.scientificname,
        Animals.taxonkey]

    # results of the query
    results = db.session.query(*sel).filter(Animals.species==species)

    # empty list to append data to
    oneSpecies = []

    # loop to append relevant data
    for result in results:
        speciesDict = {
            "s_class": result[0],
            "species": result[1],
            "scientific name": result[2].replace('\"',""),
            "taxonkey": result[3]
        }

        oneSpecies.append(speciesDict)

    return jsonify(oneSpecies[0])

#route for returning animal geojson
@app.route("/geojsonC/<s_class>")
def class_geojson(s_class):
    """Return the MetaData for a given sample."""

    # Selection to query
    sel = [
        Animals.id,
        Animals.eventdate,
        Animals.year, 
        Animals.countrycode,
        Animals.decimalLatitude,
        Animals.decimalLongitude,
        Animals.s_class]

    # results of the query
    results = db.session.query(*sel).filter(Animals.s_class==s_class).order_by(Animals.year)

    # empty list to append data to
    FeatureCollection = {"type": "FeatureCollection",
                "metadata": {
                "title": "Class Counts"
                }}

    Features = []

    # loop to append relevant data
    for result in results:
        if result[4] != "" and result[5] != "" and int(result[2]) > 2009 and int(result[2]) < 2018:
            feature = {
                "type": "Feature",
                "properties": {
                "place": result[3],
                "date": time.mktime(datetime.datetime.strptime(result[1], "%m/%d/%Y").timetuple()),
                "start": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-01-01", "%Y-%m-%d").timetuple()),
                "end": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-12-31", "%Y-%m-%d").timetuple()),
                "s_class": result[6]
                },
                "geometry": {
                "type": "Point",
                "coordinates": [
                float(result[5]),
                float(result[4])
                ]
                },
                "id": int(result[0])
            }
            
            Features.append(feature)

    FeatureCollection["features"] = Features

    return jsonify(FeatureCollection)

#route for returning animal geojson
@app.route("/geojsonS/<species>")
def species_geojson(species):
    """Return the MetaData for a given sample."""

    # Selection to query
    sel = [
        Animals.id,
        Animals.eventdate,
        Animals.year, 
        Animals.countrycode,
        Animals.decimalLatitude,
        Animals.decimalLongitude,
        Animals.s_class,
        Animals.species,
        Animals.taxonkey,
        Animals.scientificname]

    # results of the query
    results = db.session.query(*sel).filter(Animals.species==species).order_by(Animals.year)

    # empty list to append data to
    FeatureCollection = {"type": "FeatureCollection",
                "metadata": {
                "title": "Species Counts"
                }}

    Features = []

    # loop to append relevant data
    for result in results:
        if result[4] != "" and result[5] != "" and int(result[2]) > 2009 and int(result[2]) < 2018:
            feature = {
                "type": "Feature",
                "properties": {
                "place": result[3],
                "date": time.mktime(datetime.datetime.strptime(result[1], "%m/%d/%Y").timetuple()),
                "start": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-01-01", "%Y-%m-%d").timetuple()),
                "end": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-12-31", "%Y-%m-%d").timetuple()),
                "s_class": result[6],
                "species": result[7],
                "taxonkey": result[8],
                "scientific_name": result[9].replace('\"',"")
                },
                "geometry": {
                "type": "Point",
                "coordinates": [
                float(result[5]),
                float(result[4])
                ]
                },
                "id": int(result[0])
            }
            
            Features.append(feature)

    FeatureCollection["features"] = Features

    return jsonify(FeatureCollection)


if __name__ == "__main__":
    app.run(debug=True)