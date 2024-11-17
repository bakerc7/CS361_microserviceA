import subprocess

import sys

# This program issues a test call to show how the microservice can be called by the main program
# and then receive data from the microservice

# Request data (run microservice)
# subprocess.run([sys.executable, 'weather.py'])

# Receive data (read microservice data output csv)
subprocess.run(['python', 'weatherReader.py'])

