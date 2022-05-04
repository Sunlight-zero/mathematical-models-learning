import numpy as np
import pandas as pd
import cvxpy as cp
from math import ceil
requirements = pd.read_excel('data.xlsx', header=None).values.flatten()
TOTAL_WEEK = 104
WASTE_RATE = 0.1
K = 20
wasted_robots = np.array([round(x * WASTE_RATE) if x * WASTE_RATE % 1 != 0.5 else ceil(x * WASTE_RATE) for x in requirements])
working_hands = cp.Parameter(TOTAL_WEEK)
working_hands.value = 4 * requirements
wasted_hands = cp.Parameter(TOTAL_WEEK)
wasted_hands.value = 4 * wasted_robots
working_bodies = cp.Parameter(TOTAL_WEEK)
working_bodies.value = requirements
wasted_bodies = cp.Parameter(TOTAL_WEEK)
wasted_bodies.value = wasted_robots
new_hands = cp.Variable(TOTAL_WEEK, integer=True)
teaching_hands = cp.Variable(TOTAL_WEEK, integer=True)
resting_hands = cp.Variable(TOTAL_WEEK, integer=True)
new_bodies = cp.Variable(TOTAL_WEEK, integer=True)
resting_bodies = cp.Variable(TOTAL_WEEK, integer=True)
cons = [
    resting_hands[0] + teaching_hands[0] + working_hands[0] == 50,
    resting_bodies[0] + working_bodies[0] == 13,
    K * teaching_hands >= new_hands,
    teaching_hands >= 0,
    resting_hands >= 0,
    new_hands >= 0,
    resting_bodies >= 0,
    new_bodies >= 0
]
for t in range(TOTAL_WEEK - 1):
    cons.append(resting_hands[t + 1] >= working_hands[t] - wasted_hands[t]),
    cons.append(resting_hands[t + 1] + working_hands[t + 1] + teaching_hands[t + 1] == \
        resting_hands[t] + working_hands[t] + teaching_hands[t] + new_hands[t] - wasted_hands[t]
        )
    cons.append(resting_bodies[t + 1] + working_bodies[t + 1] == \
        resting_bodies[t] + working_bodies[t] + new_bodies[t] - wasted_bodies[t]    
    )
obj = cp.Minimize(100 * cp.sum(new_hands) + 200 * cp.sum(new_bodies) + 5 * cp.sum(resting_hands) + 10 * cp.sum(resting_bodies) + 10 * cp.sum(teaching_hands + new_hands))
prob = cp.Problem(obj, cons)
prob.solve(solver=cp.CPLEX)
print(prob.value)
