import argparse
import requests
import simplejson as json
import sqlite3
from sqlite3 import Error

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Retrieve weather information and store it in a SQLite database.")
    parser.add_argument("api_key", help="OpenWeatherMap API key")
    parser.add_argument("location", help="Location for weather information (e.g., city name)")

    return parser.parse_args()

# Function to retrieve weather information and store it in the database
def retrieve_and_store_weather(api_key, location):
    # SQLite database file path
    db_path = '/data/weather_data.db'

    # SQL statements for creating the database and tables
    createdb = "CREATE TABLE IF NOT EXISTS weather_data (id INTEGER PRIMARY KEY AUTOINCREMENT, epoch TIMESTAMP DEFAULT CURRENT_TIMESTAMP, " \
               "mintemp REAL, maxtemp REAL, currenttemp REAL, windspeed REAL, winddir TEXT, text1 TEXT, text2 TEXT, humidity REAL, pressure REAL);"

    url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=imperial'
    response = requests.get(url, verify=True)
    weatherjson = response.content
    j = json.loads(response.content)

    # Check if 'main' key is present in the response
    if 'main' in j:
        pressure = j['main'].get('pressure', None)
        humidity = j['main'].get('humidity', None)

        max_temp = j['main'].get('temp_max', None)
        min_temp = j['main'].get('temp_min', None)
        current_temp = j['main'].get('temp', None)
    else:
        print("Error: 'main' key not present in the response.")
        return  # Exit the function if 'main' key is not present

    wind_speed = j['wind'].get('speed', None)
    wind_dir = j['wind'].get('deg', None)
    description = j['weather'][0].get('description', None)
    main_weather = j['weather'][0].get('main', None)

    # SQL statement for inserting weather data into the database
    insert_query = "INSERT INTO weather_data (mintemp, maxtemp, currenttemp, windspeed, winddir, text1, text2, humidity, pressure) " \
                   "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"

    try:
        # Use a context manager for SQLite connection and cursor
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()

            # Create the table if it doesn't exist
            cursor.execute(createdb)

            # Insert data into the table
            cursor.execute(insert_query, (min_temp, max_temp, current_temp, wind_speed, wind_dir, description, main_weather, humidity, pressure))

            # Commit the changes to the database
            connection.commit()

    except Error as e:
        print(f"Error: {e}")

    print('Received JSON:')
    print(weatherjson)

def main():
    args = parse_arguments()
    retrieve_and_store_weather(args.api_key, args.location)

if __name__ == "__main__":
    main()
