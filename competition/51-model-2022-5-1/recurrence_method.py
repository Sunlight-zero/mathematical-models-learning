import numpy as np
import pandas as pd
import os

os.chdir('./competition/51-model-2022-5-1')
requirements = pd.read_excel('data.xlsx', header=None).values.flatten()
total_week = 16

# 工作容器艇数量一定等于当周的机器人需求数量
bodies_work = np.array(requirements[0:total_week])
bodies_new = np.zeros(total_week)
bodies_rest = np.zeros(total_week)
bodies_rest[0] = 13 - requirements[0]
total_bodies = 13
for t in range(1, total_week):
    # 当某一周的潜艇数量不足时，只需要在上一周先买上即可
    if total_bodies < bodies_work[t]:
        bodies_new[t-1] = bodies_work[t] - total_bodies
        total_bodies = bodies_work[t]
    # 保养容器艇数量 = 当前的容器艇总数 - 当前工作的容器艇数量
    bodies_rest[t] = total_bodies - bodies_work[t]

print(np.concatenate([bodies_work.reshape(1, -1), bodies_new.reshape(1, -1), bodies_rest.reshape(1, -1)], axis=0))