import pandas as pd
import numpy as np
import cvxpy as cp
from math import ceil
requirements = pd.read_excel('data.xlsx', header=None).values.flatten()
total_week = 104
K = 20
waste_rate = 0.1
working_hands = cp.Parameter(total_week)
waste_hands = cp.Parameter(total_week)
working_hands.value = 4 * requirements
waste_hands.value = np.round(4 * waste_rate * requirements)
teaching_hands = cp.Variable(total_week, integer=True)
resting_hands = cp.Variable(total_week, integer=True)
new_hands = cp.Variable((3, total_week), integer=True)
hand_price = cp.Parameter((3, 1))
hand_price.value = np.array([100, 90, 80]).reshape(3, 1)
hand_y = cp.Variable((3, total_week), boolean=True)
cons = [
    resting_hands[0] + teaching_hands[0] + working_hands[0] == 50,
    K * teaching_hands >= cp.sum(new_hands, axis=0),
    teaching_hands >= 0,
    resting_hands >= 0,
    new_hands >= 0,
    20 * hand_y[1] <= new_hands[0],
    new_hands[0] <= 20 * hand_y[0],
    20 * hand_y[2] <= new_hands[1],
    new_hands[1]  <= 20 * hand_y[1],
    new_hands[2] <= 10000 * hand_y[2]
]
for t in range(total_week - 1):
    cons.append(resting_hands[t + 1] >= working_hands[t] - waste_hands[t]),
    cons.append(resting_hands[t + 1] + working_hands[t + 1] + teaching_hands[t + 1] == \
        resting_hands[t] + working_hands[t] + teaching_hands[t] + cp.sum(new_hands, axis=0)[t] - waste_hands[t]
        )
obj = cp.Minimize(
    cp.sum(cp.multiply(new_hands, hand_price))\
    + 5 * cp.sum(resting_hands)\
    + 10 * cp.sum(teaching_hands)\
    + 10 * cp.sum(new_hands)
)
prob = cp.Problem(obj, cons)
prob.solve(solver=cp.CPLEX, verbose=True)
print(prob.value)
working_bodies = cp.Parameter(total_week)
waste_bodies = cp.Parameter(total_week)
working_bodies.value = requirements
waste_bodies.value = np.round(requirements * waste_rate)
resting_bodies = cp.Variable(total_week, integer=True)
new_bodies = cp.Variable((3, total_week), integer=True)
body_price = cp.Parameter((3, 1))
body_price.value = np.array([200, 180, 160]).reshape(3, 1)
body_y = cp.Variable((3, total_week), boolean=True)
cons2 = [
    resting_bodies[0] + working_bodies[0] == 13,
    resting_bodies >= 0,
    new_bodies >= 0,
    5 * body_y[1] <= new_bodies[0],
    new_bodies[0] <= 5 * body_y[0],
    5 * body_y[2] <= new_bodies[1],
    new_bodies[1]  <= 5 * body_y[1],
    new_bodies[2] <= 10000 * body_y[2]
]
for t in range(total_week - 1):
    cons2.append(resting_bodies[t + 1] + working_bodies[t + 1]== \
        resting_bodies[t] + working_bodies[t] + cp.sum(new_bodies, axis=0)[t] - waste_bodies[t]
        )
obj2 = cp.Minimize(
    cp.sum(cp.multiply(new_bodies, body_price))\
    + 10 * cp.sum(resting_bodies)
)
prob2 = cp.Problem(obj2, cons2)
prob2.solve(solver=cp.CPLEX, verbose=True)
print(prob2.value)
print(prob.value + prob2.value)
