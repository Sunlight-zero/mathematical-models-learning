# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:01:31 2022

@author: lll
"""


import pandas as pd
import matplotlib.pyplot as plt
df =pd.read_excel("data.xlsx",header = None)
data = df.values
data = data.flatten()
print(data)

plt.scatter(np.arange(1,105), data)
plt.show()
