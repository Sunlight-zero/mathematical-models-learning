import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import cvxpy as cp
from math import ceil
import pickle

requirements = pd.read_excel('data.xlsx', header=None).values.flatten()

total_week = 104
requirements = requirements[0:total_week]
K = 20
waste_rate = 0.1

working_hands = cp.Parameter(total_week)
waste_hands = cp.Parameter(total_week)
working_hands.value = 4 * requirements
waste_hands.value = np.array([
    round(4 * x * waste_rate) if x % 1 != 0.5 else ceil(4 * x * waste_rate) 
    for x in requirements
])

teaching_hands = cp.Variable(total_week, integer=True)
resting_hands = cp.Variable(total_week, integer=True)
new_hands = cp.Variable((3, total_week), integer=True)

# 机械手购买的分段点
hand_price = cp.Parameter((3, 1))
hand_price.value = np.array([100, 90, 80]).reshape(3, 1)
hand_y = cp.Variable((3, total_week), boolean=True)

cons = [
    resting_hands[0] + teaching_hands[0] + working_hands[0] == 50,
    K * teaching_hands >= cp.sum(new_hands, axis=0),

    teaching_hands >= 0,
    resting_hands >= 0,
    new_hands >= 0,

    # 分段函数引入的约束
    20 * hand_y[1] <= new_hands[0],
    new_hands[0] <= 20 * hand_y[0],
    20 * hand_y[2] <= new_hands[1],
    new_hands[1]  <= 20 * hand_y[1],
    new_hands[2] <= 10000 * hand_y[2]
]

for t in range(total_week - 1):
    cons.append(resting_hands[t + 1] >= resting_hands[t] - waste_hands[t]),
    cons.append(resting_hands[t + 1] + working_hands[t + 1] + teaching_hands[t + 1] == \
        resting_hands[t] + working_hands[t] + teaching_hands[t] + new_hands[t] - waste_hands[t]
    )

obj = cp.Minimize(
    cp.sum(cp.multiply(new_hands, hand_price))\
    + 5 * cp.sum(resting_hands)\
    + 10 * cp.sum(teaching_hands)\
    + 10 * cp.sum(new_hands)
)

prob = cp.Problem(obj, cons)
prob.solve(solver=cp.CPLEX, verbose=True)
