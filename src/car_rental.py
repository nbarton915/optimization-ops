# A car rental company has a fleet of 94 vehicles distributed among its 10 agencies. 
# The distance between every two agencies is given. The required number of cars needed 
# at each agency and the number of present cars each day are given. Also, a fixed cost 
# per kilometer for transporting a car is given. The problem is to determine the movements 
# of cars so as to satisfy the requirements of each agency and minimizing the 
# total cost of transportation.

from pyomo.environ import *
import math
import os

model = AbstractModel("Car rental")

#Sets and parameters

#set of agencies
model.agencies = Set()

#set of agencies with excess
model.excess_agencies = Set()

#set of agencies with need
model.need_agencies = Set()

#number of vehicles in the company
model.vehicles = Param(within = NonNegativeIntegers)

#number of cars present for each company
model.present_cars = Param(model.agencies, within = NonNegativeIntegers)

#number of cars required for each company
model.required_cars = Param(model.agencies, within = NonNegativeIntegers)

#X-coordinate of each agency
model.X = Param(model.agencies, within = NonNegativeReals)

#Y-coordinate of each agency
model.Y = Param(model.agencies, within = NonNegativeReals)

#road distance between each pair of agencies
def dist(model, i, j):
    return 1.3*math.sqrt((model.X[i] - model.X[j])**2 + (model.Y[i] - model.Y[j])**2)  
model.road_distance = Param(model.excess_agencies, model.need_agencies, within = NonNegativeReals, initialize = dist)

#cost per km of transporting a car
model.cost_car = Param(within = NonNegativeReals)

#Variable

#variable indicating the flow from agencies with excess to agencies in need
model.move_ab = Var(model.excess_agencies, model.need_agencies, within = NonNegativeIntegers)

#Objective

#minimize the total transportation cost
def min_cost(model):
    return sum(sum(model.cost_car*model.road_distance[a,b]*model.move_ab[a,b] for b in model.need_agencies) for a in model.excess_agencies)
model.min_cost = Objective(rule = min_cost)

#Constraints

#Number of cars going from each excess agency to all agencies in need
def excess_release(model, a):
    return sum(model.move_ab[a,b] for b in model.need_agencies) == (model.present_cars[a] - model.required_cars[a])
model.excess_release = Constraint(model.excess_agencies, rule = excess_release)

#Number of cars going in each agency in need from all excess agencies
def need_satisfy(model, b):
    return sum(model.move_ab[a,b] for a in model.excess_agencies) == (model.required_cars[b] - model.present_cars[b])
model.need_satisfy = Constraint(model.need_agencies, rule = need_satisfy)


solver = SolverFactory('gurobi_direct')
instance = model.create_instance(f"{os.getcwd()}/../data/car_rental.dat")
results = solver.solve(instance)

#Python Script for printing the solution in the terminal
for i in instance.excess_agencies:
    for j in instance.need_agencies:
        if value(instance.move_ab[i,j]) > 0:
            print(f'Number of cars needed to move from agency {i} to agency {j} is {value(instance.move_ab[i,j])}')
print(f'The minimum total transportation cost is {value(instance.min_cost)}')

#Python Script for writing the solution while checking the termination condition of the solver
if results.solver.termination_condition == TerminationCondition.infeasible:
    print('The model is infeasible: No solution available')
elif results.solver.termination_condition == TerminationCondition.unbounded:
    print('The model has an unbounded solution')
elif results.solver.termination_condition == TerminationCondition.optimal:
    output = open(f'{os.getcwd()}/../output/results.txt', 'w')
    for i in instance.excess_agencies:
        for j in instance.need_agencies:
            if value(instance.move_ab[i,j]) > 0:
                output.write(f'Number of cars needed to move from agency {i} to agency {j} is {value(instance.move_ab[i,j])}\n\n')
    output.write(f'The minimum total transportation cost is {value(instance.min_cost)}')
    output.close()
