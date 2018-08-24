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

from flask_mysqldb import MySQL

## mysql://bb43e756cddd2f:5e6891d5@us-cdbr-iron-east-01.cleardb.net/heroku_724a6776f62a58d?reconnect=true

app = Flask(__name__)

# to run locally uncomment
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'jkennedy'
# app.config['MYSQL_DB'] = 'animal'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config['MYSQL_USER'] = 'bb43e756cddd2f'
app.config['MYSQL_PASSWORD'] = '5e6891d5'
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-01.cleardb.net'
app.config['MYSQL_DB'] = 'heroku_724a6776f62a58d'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/test')
def animals():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM heroku_724a6776f62a58d.animals''')
    rv = cur.fetchall()
    return jsonify(rv)

##################################
# base route


@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")

# route for returning all class names
@app.route("/classes")
def classes():
    """Return a list of class names."""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT s_class FROM heroku_724a6776f62a58d.animals''')
    results = cur.fetchall()

    # empty list to append data to
    class_names = []

    # loop to append relevant data
    for result in results:
        class_names.append(result["s_class"])

    # return a set of unique values in the list
    class_set = set(class_names)

    # change the set back to a list
    class_names = list(class_set)

    # remove items that are not needed
    # class_names.remove("s_class")

    # sort the list
    class_names.sort()

    return jsonify(class_names)

    

# route for returning all species names
@app.route("/species")
def species():
    """Return a list of species and years."""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT species, year FROM heroku_724a6776f62a58d.animals''')
    results = cur.fetchall()

    # empty list to append data to
    species_names = []

    # loop to append relevant data
    for result in results:
        if result["year"] != "year" and int(result["year"]) > 2009 and int(result["year"]) < 2018:
            species_names.append(result["species"])

    # return a set of unique values in the list
    species_set = set(species_names)

    # change the set back to a list
    species_names = list(species_set)

    # remove items that are not needed
    species_names.remove("")

    # sort the list
    species_names.sort()

    return jsonify(species_names)

#route for returning class geojson
@app.route("/geojsonC/<s_class>")
def class_geojson(s_class):
    """Return the MetaData for a given sample."""
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, eventdate, year, countrycode, decimallatitude, decimallongitude, s_class FROM heroku_724a6776f62a58d.animals''')
    results = cur.fetchall()
    # empty list to append data to
    FeatureCollection = {"type": "FeatureCollection",
                         "metadata": {
                             "title": "Class Counts"
                         }}

    Features = []

    # loop to append relevant data
    for result in results:
        if result["decimallatitude"] != "" and result["decimallongitude"] != "" and int(result["year"]) > 2009 and int(result["year"]) < 2018:
            feature = {
                "type": "Feature",
                "properties": {
                    "place": result["countrycode"],
                    "date": time.mktime(datetime.datetime.strptime(result["eventdate"], "%m/%d/%Y").timetuple()),
                    "start": time.mktime(datetime.datetime.strptime(f"{int(result['year'])}-01-01", "%Y-%m-%d").timetuple()),
                    "end": time.mktime(datetime.datetime.strptime(f"{int(result['year'])}-12-31", "%Y-%m-%d").timetuple()),
                    "s_class": result["s_class"]
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(result["decimallongitude"]),
                        float(result["decimallatitude"])
                    ]
                },
                "id": int(result["id"])
            }

            Features.append(feature)

    FeatureCollection["features"] = Features

    return jsonify(FeatureCollection)

#route for returning species geojson
@app.route("/geojsonS/<species>")
def species_geojson(species):
    """Return the MetaData for a given sample."""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, eventdate, year, countrycode, decimalLatitude, decimalLongitude, s_class, species, scientificname, taxonkey FROM heroku_724a6776f62a58d.animals''')
    results = cur.fetchall()

    # empty list to append data to
    FeatureCollection = {"type": "FeatureCollection",
                "metadata": {
                "title": "Species Counts"
                }}

    Features = []

    # loop to append relevant data
    for result in results:
        if result["decimalLatitude"] != "" and result["decimalLongitude"] != "" and int(result["year"]) > 2009 and int(result["year"]) < 2018:
            feature = {
                "type": "Feature",
                "properties": {
                "place": result["countrycode"],
                "date": time.mktime(datetime.datetime.strptime(result["eventdate"], "%m/%d/%Y").timetuple()),
                "start": time.mktime(datetime.datetime.strptime(f"{int(result['year'])}-01-01", "%Y-%m-%d").timetuple()),
                "end": time.mktime(datetime.datetime.strptime(f"{int(result['year'])}-12-31", "%Y-%m-%d").timetuple()),
                "s_class": result["s_class"],
                "species": result["species"],
                "taxonkey": result["taxonkey"],
                "scientific_name": result["scientificname"].replace('\"',"")
                },
                "geometry": {
                "type": "Point",
                "coordinates": [
                float(result["decimalLongitude"]),
                float(result["decimalLatitude"])
                ]
                },
                "id": int(result["id"])
            }
            
            Features.append(feature)

    FeatureCollection["features"] = Features

    return jsonify(FeatureCollection)
    

if __name__ == '__main__':
    app.run(debug=True)