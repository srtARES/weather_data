from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os  # Import the os module

app = Flask(__name__)
CORS(app)


def fetch_weather_data():
    try:
        conn = psycopg2.connect("dbname=Assignment user=postgres password=SrtAres1904")
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM open_weather ORDER BY ID DESC")
        data = cursor.fetchall()
        weather_data = [dict(row) for row in data]
        cursor.close()
        conn.close()
        return weather_data
    except psycopg2.Error as e:
        print("Error fetching data:", e)
        return []

@app.route('/weather', methods=['GET'])
def get_weather_data():
    weather_data = fetch_weather_data()
    # Return the list of dictionaries as JSON
    return jsonify(weather_data)
