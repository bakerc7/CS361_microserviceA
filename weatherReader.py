import csv
import os

# This is an example of how the main program can receive data from the microservice
# Its purpose is to read the csv weather data

def print_weather_data(csv_file_path):
    if not os.path.isfile(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    try:
        with open(csv_file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(", ".join(row))
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")


if __name__ == "__main__":
    csv_file_path = "weather_data.csv"
    print_weather_data(csv_file_path)
