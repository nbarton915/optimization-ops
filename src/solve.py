'''
This model is an advanced example of a gurobi model, following some best practices for inputs and outputs.
It demonstrates reading inputs from a file, writing outputs to a file, writing outputs to the terminal, producing a pretty table for columnar output, logging progress to a log file, importing modules with common methods, and formulating a model using the methods provided by Gurobi.
If you have any questions please reach out to Optilogic support at support@optilogic.com or submit a ticket through the modeling studio.
'''
# ---------------------------------------------
# Import needed modules
# ---------------------------------------------
import argparse
from tabnanny import check
import gurobipy as gp
from gurobipy import GRB
import datetime as dt
import logging
import common # this imports the common.py file

parser = argparse.ArgumentParser(description='Create a new Optilogic Job')
parser.add_argument('--scenario', help='Scenario to run')
parser.add_argument('--timetest', '-t', action='count', default=0, help='Add n minutes to the beginning of the solve')

args = parser.parse_args()

import time
minutes = args.timetest*60
checkpoints = int(minutes / 10) #report on 10 second intervals
for c in range(0, checkpoints):
    print(f'{c} seconds have passed')
    time.sleep(10)

if args.scenario:
    input_scenario_directory = args.scenario
else:
    input_scenario_directory = 'baseline'

# ---------------------------------------------
# Initialization
# ---------------------------------------------
modelName = 'advanced'

# Path objects
inputPath = common.ensureDirectory(f"../inputs/{input_scenario_directory}") # Relative path to input files
outputPath = common.ensureDirectory("../outputs") # Relative path to output files
logPath = common.ensureDirectory("../logs") # Relative path to log file

# Filename variables
logFilename = logPath / f"{dt.datetime.now()}.log"
outputFilename = outputPath / 'flow_table.csv'

# Logging
logger = common.getLogger(logFilename)

# ---------------------------------------------
# Main
#
# Wrap in a try/except block for error handling
# ---------------------------------------------
try:
    logger.info('Running ' + __file__)

    # ---------------------------------------------
    #  Get inputs
    # ---------------------------------------------
    logger.info('Read and process input files')

    inputDictionaries = common.parseInputFiles(inputPath)
    facilities = inputDictionaries['facilities']
    customers = inputDictionaries['customers']
    transportation_costs = inputDictionaries['transportation_costs']
    demand_values = inputDictionaries['demand_values']

    # ---------------------------------------------
    # Model Implementation
    # ---------------------------------------------
    logger.info('Create abstract model')

    m = gp.Model(modelName)
    # ---------------------------------------------
    # Variables
    # --------------------------------------------
    logger.info('Create variables')

    # Flow Variables between warehouses and customers
    flow = m.addVars(list(transportation_costs.keys()), name="flow")

    # ---------------------------------------------
    # Objective
    # ---------------------------------------------
    logger.info('Set the objective function')

    # Minimize the total transportation cost
    m.setObjective(sum(transportation_costs[i,j] * flow[i,j] for i in list(set(facilities)) for j in list(set((facilities + customers))) if (i,j) in list(transportation_costs.keys())), GRB.MINIMIZE)

    # ---------------------------------------------
    # Constraints
    # ---------------------------------------------
    logger.info('Set up the model contraints')

    # Demand satisfaction for each customer, product and time period
    m.addConstrs((flow.sum('*', j) == demand_values[j] for j in list(set(customers))), "demand_satisfaction")

    # ---------------------------------------------
    # Create the model lp file
    # ---------------------------------------------
    logger.info('Create the model lp file')

    # Write model as LP file
    m.write(modelName + '.lp')

    # ---------------------------------------------
    # Solve the model
    # ---------------------------------------------
    logger.info('Start the model solve')

    # Solve the model
    print(' ')
    m.optimize()
    print(' ')

    logger.info('Solve complete')

    # ---------------------------------------------
    # Write outputs to the screen
    # ---------------------------------------------

    # Printing the solution to the terminal
    if m.status == GRB.OPTIMAL:
        print(' ')
        print(' ')
        print('         ---- Solution ----')

        data = []
        solution = m.getAttr('x', flow)
        for i, j in list(transportation_costs.keys()):
            if solution[i, j] > 0:
                data.append([i,j, solution[i, j]])

        common.printPrettyTable(data)

    # ---------------------------------------------
    # Write outputs to an output file
    # ---------------------------------------------

    # Write outputs to a file
    if m.status == GRB.OPTIMAL:
        with open(outputFilename, 'w') as flowTableOutput:
            flowTableOutput.write('source,destination,flow\n')
            for i, j in list(transportation_costs.keys()):
                if solution[i, j] > 0:
                    flowTableOutput.write(f"{i},{j},{solution[i, j]}\n")
except Exception as e:
    logger.critical(f'The model encountered an exception: {e}')

# ---------------------------------------------
# Cleanup
# ---------------------------------------------

# Close the logger when done
logging.shutdown()