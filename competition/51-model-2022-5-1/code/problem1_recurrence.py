import numpy as np
import pandas as pd
requirements = pd.read_excel('data.xlsx', header=None).values.flatten()
total_week = 8
bodies_work = np.array(requirements[0:total_week])
bodies_new = np.zeros(total_week)
bodies_rest = np.zeros(total_week)
bodies_rest[0] = 13 - requirements[0]
total_bodies = 13
for t in range(1, total_week):
    if total_bodies < bodies_work[t]:
        bodies_new[t-1] = bodies_work[t] - total_bodies
        total_bodies = bodies_work[t]
    bodies_rest[t] = total_bodies - bodies_work[t]
print(np.concatenate([bodies_work.reshape(1, -1), bodies_new.reshape(1, -1), bodies_rest.reshape(1, -1)], axis=0))