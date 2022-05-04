import pandas as pd
import numpy as np
import cvxpy as cp
df = pd.read_excel('data.xlsx', header=None)
data = df.values.flatten()
requirements = data
requirements1 = requirements[0:8]
k = 10
hand_new = cp.Variable(8, integer=True)
hand_work = cp.Variable(8, integer=True)
hand_rest = cp.Variable(8, integer=True)
hand_teach = cp.Variable(8, integer=True)
hand_skill = cp.Variable(8, integer=True)
body_new = cp.Variable(8, integer=True)
body_work = cp.Variable(8, integer=True)
body_rest = cp.Variable(8, integer=True)
body_tested = cp.Variable(8, integer=True)
cons = [
    hand_work == 4 * requirements1,
    body_work == requirements1,
    k * hand_teach >= hand_new,
    hand_skill == hand_work + hand_rest + hand_teach,
    body_tested == body_work + body_rest,
    hand_new >= 0,
    hand_rest >= 0,
    hand_work >= 0,
    hand_teach >= 0,
    body_new >= 0,
    body_rest >= 0,
    body_work >= 0,
    hand_skill[0] == 50,
    body_tested[0] == 13
]
for t in range(7):
    cons.append(hand_rest[t+1] >= hand_work[t]),
    cons.append(hand_skill[t+1] == hand_skill[t] + hand_new[t])
    cons.append(body_tested[t+1] == body_tested[t] + body_new[t])
obj = cp.Minimize(
    200 * cp.sum(body_new) + 
    100 * cp.sum(hand_new) + 
    5 * cp.sum(hand_rest) + 
    10 * cp.sum(body_rest) +
    10 * cp.sum(hand_new + hand_teach)
)
prob = cp.Problem(obj, cons)
prob.solve(verbose=True)
print('Optimal value', prob.value)