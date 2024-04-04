import requests
import psycopg2
from datetime import datetime, timedelta

city = "Huddersfield"
api_key = "bd34abc96f52c81934a8ece631087ae2"

def fetch_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data.get('main', {}).get('humidity')

def save_to_database(city, humidity):
    try:
        conn = psycopg2.connect("dbname=assignment_o9dk host=dpg-co5pcpm3e1ms73b9logg-a.oregon-postgres.render.com user=root password=UwrZkz3gvU6cayjibCpazPpkdcA4p1VO")
        cursor = conn.cursor()
        print("Inserting data:", city, humidity, datetime.now())
        cursor.execute("INSERT INTO open_weather (city_name, humidity, date) VALUES (%s, %s, %s)", (city, humidity, datetime.now()))
        conn.commit()
    except psycopg2.Error as e:
        print("Error inserting data:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_latest_weather_timestamp(city):
    try:
        conn = psycopg2.connect("dbname=assignment_o9dk host=dpg-co5pcpm3e1ms73b9logg-a.oregon-postgres.render.com user=root password=UwrZkz3gvU6cayjibCpazPpkdcA4p1VO")
        cursor = conn.cursor()
        print("Fetching latest timestamp for city:", city)
        cursor.execute("SELECT date FROM open_weather WHERE city_name = %s ORDER BY date DESC LIMIT 1", (city,))
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error as e:
        print("Error fetching latest timestamp:", e)
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_cached_weather(city):
    try:
        conn = psycopg2.connect("dbname=assignment_o9dk host=dpg-co5pcpm3e1ms73b9logg-a.oregon-postgres.render.com user=root password=UwrZkz3gvU6cayjibCpazPpkdcA4p1VO")
        cursor = conn.cursor()
        print("Fetching cached data for city:", city)
        cursor.execute("SELECT humidity FROM open_weather WHERE city_name = %s ORDER BY date DESC LIMIT 1", (city,))
        row = cursor.fetchone()
        return row[0] if row else None
    except psycopg2.Error as e:
        print("Error fetching cached data:", e)
        return None
    finally:
        if conn:
            cursor.close()
            conn.close()

def get_weather(city, api_key):
    last_update_time = get_latest_weather_timestamp(city)
    if last_update_time and datetime.now() - last_update_time < timedelta(hours=1):
        print("Using cached data")
        return get_cached_weather(city)
    else:
        humidity = fetch_weather(city, api_key)
        if humidity is not None:
            latest_time_after_fetch = get_latest_weather_timestamp(city)
            if latest_time_after_fetch is None or (datetime.now() - latest_time_after_fetch >= timedelta(hours=1)):
                save_to_database(city, humidity)
                print("Fetched and saved new data")
            else:
                print("New data was inserted during the fetch, skipping save")
        return humidity


humidity = get_weather(city, api_key)
if humidity is not None:
    print(f"Humidity in {city}: {humidity}%")
