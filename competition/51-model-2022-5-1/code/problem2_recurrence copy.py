import numpy as np
import pandas as pd
from math import ceil
requirements = pd.read_excel('data.xlsx', header=None).values.flatten()
wastes = np.array([round(x * 0.2) if 0.2 * x % 1 != 0.5 else ceil(x * 0.2) for x in requirements])
total_week = 104
bodies_work = np.array(requirements[0:total_week])
bodies_new = np.zeros(total_week)
bodies_rest = np.zeros(total_week)
bodies_rest[0] = 13 - requirements[0]
total_bodies = 13
for t in range(1, total_week):
    total_bodies_new = max(total_bodies - wastes[t], bodies_work[t])
    bodies_new[t] = total_bodies_new - total_bodies
    bodies_rest[t] = total_bodies - bodies_work[t] + wastes[t]
    total_bodies = total_bodies_new
print(bodies_new)