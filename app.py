# dependencies
from flask import (
    Flask,
    jsonify,
    render_template,
    redirect)
from flask_mysqldb import MySQL
import numpy as np
import pandas as pd
import time
import datetime

## mysql://bb43e756cddd2f:5e6891d5@us-cdbr-iron-east-01.cleardb.net/heroku_724a6776f62a58d?reconnect=true

app = Flask(__name__)

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
    rv = cur.fetchall()
    return jsonify(rv)

    

# route for returning all species names


@app.route("/species")
def species():
    """Return a list of species and years."""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT species, year FROM heroku_724a6776f62a58d.animals''')
    rv = cur.fetchall()
    return jsonify(rv)


@app.route("/metadata/<species>")
def animal_metadata(species):
    """Return the MetaData for a given species"""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT s_class, species, scientificname, taxonkey FROM heroku_724a6776f62a58d.animals''')
    rv = cur.fetchall()
    return jsonify(rv)

#route for returning animal geojson


@app.route("/geojsonC/<s_class>")
def class_geojson(s_class):
    """Return the MetaData for a given sample."""
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, eventdate, year, countrycode, decimallatitude, decimallongitude, s_class FROM heroku_724a6776f62a58d.animals''')
    rv = cur.fetchall()
    return jsonify(rv)

    # results = cur.fetchall()
    # # empty list to append data to
    # FeatureCollection = {"type": "FeatureCollection",
    #                      "metadata": {
    #                          "title": "Class Counts"
    #                      }}

    # Features = []

    # # loop to append relevant data
    # for result in results:
    #     if result[4] != "" and result[5] != "" and int(result[2]) > 2009 and int(result[2]) < 2018:
    #         feature = {
    #             "type": "Feature",
    #             "properties": {
    #                 "place": result[3],
    #                 "date": time.mktime(datetime.datetime.strptime(result[1], "%m/%d/%Y").timetuple()),
    #                 "start": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-01-01", "%Y-%m-%d").timetuple()),
    #                 "end": time.mktime(datetime.datetime.strptime(f"{int(result[2])}-12-31", "%Y-%m-%d").timetuple()),
    #                 "s_class": result[6]
    #             },
    #             "geometry": {
    #                 "type": "Point",
    #                 "coordinates": [
    #                     float(result[5]),
    #                     float(result[4])
    #                 ]
    #             },
    #             "id": int(result[0])
    #         }

    #         Features.append(feature)

    # FeatureCollection["features"] = Features

    # return jsonify(FeatureCollection)




@app.route("/geojsonS/<species>")
def species_geojson(species):
    """Return the MetaData for a given sample."""

    cur = mysql.connection.cursor()
    cur.execute('''SELECT id, eventdate, year, countrycode, decimalLatitude, decimalLongitude, s_class, species, scientificname, taxonkey FROM heroku_724a6776f62a58d.animals''')
    rv = cur.fetchall()
    return jsonify(rv)
    # Selection to query
    

if __name__ == '__main__':
    app.run(debug=True)

    print('is this ok?')
