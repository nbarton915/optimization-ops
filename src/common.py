'''
This module contains methods common to both versions (gurobi & python) of the template model.
'''
import pandas as pd
import logging
import sys
import os
from pathlib import Path
from tabulate import tabulate

# ---------------------------------------------
# Print a nicely formatted grid
# ---------------------------------------------
def printPrettyTable(data):
    header = ['SOURCE', 'DESTINATION', 'FLOW']
    print(tabulate(data, headers=header, tablefmt='fancy_grid'))

# ---------------------------------------------
# Ensure a directory exists
#
# Returns a Path object for the directory
# ---------------------------------------------

def ensureDirectory(folderName):
    folderPath = Path(folderName)
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    return folderPath

# ---------------------------------------------
# Read and parse input files
#
# Returns a dictionary of objects with the parsed fields
# ---------------------------------------------

def parseInputFiles(inputPath):
    logger = logging.getLogger('main.common') # create a 'child' logger that logs to the same outputs as main.

    facilities = []
    customers = []
    transportation_costs = {}
    demand_values = {}

    try:
        # Read and process lane data
        logger.info('Read and process lane data')
        lane_data = pd.read_csv(inputPath / 'lane.csv')
        for index, rows in lane_data.iterrows():
            facilities.append(rows.warehouse_name)
            customers.append(rows.customer_name)
            transportation_costs[(rows.warehouse_name, rows.customer_name)] = rows.transport_cost

        # Read and process demand data
        logger.info('Read and process demand data')
        demand_data = pd.read_csv(inputPath / 'demand.csv')
        for index, rows in demand_data.iterrows():
            demand_values[(rows.customer_name)] = rows.demand_value
    except Exception as e:
        logger.critical(f'parseInputFiles encounted an exception: {e}')
        raise # rethrow the exception

    return {
        'facilities': facilities,
        'customers': customers,
        'transportation_costs': transportation_costs,
        'demand_values': demand_values
    }

# ---------------------------------------------
# Logger Usage
#
# logger.debug('a debug log entry')
# logger.info('an info log entry')
# logger.warning('a warning log entry')
# logger.error('an error log entry')
# logger.critical('a critical log entry')
#
# for more on logging, see https://docs.python.org/3/howto/logging-cookbook.html
# ---------------------------------------------

def getLogger(logFilename):
    logger = logging.getLogger('main') # create the parent logger.
    logger.setLevel(logging.DEBUG)

    # Log to file
    fileFormatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler(logFilename, mode='w')
    file_handler.setFormatter(fileFormatter)
    logger.addHandler(file_handler)

    # log to terminal
    screenFormatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(screenFormatter)
    logger.addHandler(screen_handler) # Comment out this line to not log to the screen

    return logger