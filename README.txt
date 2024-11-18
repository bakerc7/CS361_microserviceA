README

Communication Contract

A. How to programmatically REQUEST data from the microservice. Example call included.

This microservice, weather.py, reads the specified location from the second row of a csv file and then outputs the predefined weather data for that location for the following week from the current date. the predefined weather data can be in any combination of the following, but the format must match exactly: max_temp, min_temp, rain_sum, and prec_prob. This is in addition to the location and date headers, which are automatically introduced in the example program.

It is expected the main program will provide a location via a csv file to the weather microservice.

Here is an example of how the main program can programmatically request data from the microservice, resulting in the output of the csv with the weather data.

subprocess.run(['python', 'weather.py'])




B. How to programmatically RECEIVE data from the microservice. Example call included.

To receive data from the microservice, it is expected that the weather data has been output to the csv file. Then the data can be read from the csv file to receive it. Here is an example call:

subprocess.run(['python', programToReadData.py', 'specify file location here'])

The weather data points that are written into the csv file are the same as those that have been provided initially. Therefore, the main program can be selective about which weather data is written into the csv file. Data points such as max temperature can be accessed on its own or with other specified points.
The output will contain the weather data for each upcoming day of the week from the current date.

![UML Diagram](UML1.PNG)
