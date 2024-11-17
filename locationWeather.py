import csv
import os

import sys

# This is an example program of how the main program can interact with the microservice
# Its purpose is to get user input and write it to csv file, in preparation for microservice to run
# The microservice needs a location and headers of the requested data to run
def main():
    # use same csv file for location and weather data
    file_path = "weather_data.csv"
    # getting location data and weather variables from user
    location = input("Enter the weather location: ")
    headers_input = input(
        "Enter the data you would like to receive in CSV format: \n"
        "('max_temp', 'min_temp', 'rain_sum', 'prec_prob'): "
    )
    # Split input by commas, strip spaces, and remove quotes if they exist
    headers_format = [header.strip().replace('"', '') for header in headers_input.split(",")]

    write_location_to_csv(file_path, location, headers_format)
    print("Arguments:", sys.argv)


def write_location_to_csv(file_path, location, headers_format ):
    try:
        # Open the CSV file in write mode
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Check if the file is empty
            if os.stat(file_path).st_size == 0:
                # File is empty, write headers
                writer.writerow(["location", "dates"] + headers_format)

                print("Headers written to locations CSV.")

            # Write the specified location to the CSV file
            writer.writerow([location])
            # Only the location
            print(f"Location '{location}' written to weather_data CSV.")

    except Exception as e:
        print(f"An error occurred writing the locations to CSV: {e}")


if __name__ == "__main__":
    main()
