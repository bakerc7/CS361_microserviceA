import csv
import os
import requests
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# precip_prob is in percent chance
# temperature is in fahrenheit
# rain_sum is in mm for the day

# Setup the OpenMeteo API client for weather data, where the weather data comes from
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


# Function to convert to coordinates from a location using a geocoding API
# OpenMateo needs coordinates to work
def get_coordinates(location):
    # My provided API key, can get new one from opencagedata
    geocoding_api_key = "27708e3c5142438babf9fe4e1ba67dff"
    geocoding_url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={geocoding_api_key}"

    response = requests.get(geocoding_url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            latitude = data['results'][0]['geometry']['lat']
            longitude = data['results'][0]['geometry']['lng']
            return latitude, longitude
        else:
            print(f"No results found for location: {location}")
            return None
    else:
        print(f"Error fetching coordinates for {location}: {response.status_code}")
        return None


# Function to get weather data from OpenMateo using the coordinates
def get_weather_data(latitude, longitude):
    # API url
    url = "https://api.open-meteo.com/v1/forecast"
    # The weather data parameters being received
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "temperature_2m_min", "rain_sum", "precipitation_probability_max"],
        "temperature_unit": "fahrenheit"
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0] if responses else None

    if not response:
        print("No weather data found.")
        return None

    # Extract daily data from openmateo data, it is given a week out from the current date
    # weather variable names can be adjusted as needed
    daily_data = {
        "dates": pd.date_range(
            start=pd.to_datetime(response.Daily().Time(), unit="s", utc=True),
            end=pd.to_datetime(response.Daily().TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=response.Daily().Interval()),
            inclusive="left"
        ),
        "max_temp": response.Daily().Variables(0).ValuesAsNumpy(),
        "min_temp": response.Daily().Variables(1).ValuesAsNumpy(),
        "rain_sum": response.Daily().Variables(2).ValuesAsNumpy(),
        "prec_prob": response.Daily().Variables(3).ValuesAsNumpy()
    }

    return {
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "daily": daily_data
    }


# Function to write the retrieved weather data to the csv file
def write_weather_to_csv(file_path, weather_data):
    try:
        # Check if the file exists
        file_exists = os.path.isfile(file_path)
        existing_headers = []

        if file_exists:
            # Read the headers of the existing file
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                # Read first row as headers
                existing_headers = next(reader)

        # Open the file to overwrite it
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Rewrite the existing headers first
            writer.writerow(existing_headers)

            # Write data for each relevant header
            # weather variable names can be adjusted as needed
            for dates, max_temp, min_temp, rain_sum, prec_prob in zip(
                    weather_data['daily']['dates'],
                    weather_data['daily']['max_temp'],
                    weather_data['daily']['min_temp'],
                    weather_data['daily']['rain_sum'],
                    weather_data['daily']['prec_prob']
            ):
                row = []

                # Add Location first, assuming it's in the headers
                if 'location' in existing_headers:
                    row.append(weather_data['location'])

                # Add Date second, assuming it's in the headers
                if 'dates' in existing_headers:
                    row.append(dates.date())

                # Adds weather data based on the existing headers provided
                if 'max_temp' in existing_headers:
                    row.append(max_temp)
                if 'min_temp' in existing_headers:
                    row.append(min_temp)
                if 'rain_sum' in existing_headers:
                    row.append(rain_sum)
                if 'prec_prob' in existing_headers:
                    row.append(prec_prob)

                # Write the row with all relevant columns
                writer.writerow(row)

    except Exception as e:
        print(f"An error occurred writing the weather data CSV: {e}")


# Processing the received weather data
def process_weather_data(locations_file_path, weather_data_file_path):
    try:
        # read the csv file
        with open(locations_file_path, mode='r') as file:
            reader = csv.reader(file)
            # ignores the header row, as location is assumed in second row
            headers = next(reader)

            # Ensure there's at least one row of data
            first_data_row = next(reader, None)
            if first_data_row:
                # Retrieve location from the first column
                location = first_data_row[0]

                # Get coordinates for the location
                coordinates = get_coordinates(location)
                if coordinates:
                    latitude, longitude = coordinates
                    # Retrieve weather data using coordinates
                    weather_data = get_weather_data(latitude, longitude)
                    if weather_data:
                        # Adds the location to the weather_data
                        weather_data['location'] = location
                        # Write weather data to csv
                        write_weather_to_csv(weather_data_file_path, weather_data)

            else:
                print("No locations found in the CSV file.")

    except Exception as e:
        print(f"An error occurred reading the locations CSV: {e}")


if __name__ == "__main__":
    # Specify the paths to the CSV files, update as needed
    locations_file_path = "weather_data.csv"
    weather_data_file_path = "weather_data.csv"

    # Call the function to process weather data
    process_weather_data(locations_file_path, weather_data_file_path)
