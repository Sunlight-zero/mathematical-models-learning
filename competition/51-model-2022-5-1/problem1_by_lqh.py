# -*- coding: utf-8 -*-
"""
Created on Sun May  1 15:08:48 2022

@author: lll
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp


r = np.array([11, 5, 4, 7, 16, 6, 5, 7])
h = cp.Variable(8, integer=True)
rh = cp.Variable(8, integer=True)
wh = cp.Variable(8, integer=True)
th = cp.Variable(8, integer=True)
nh = cp.Variable(8, integer=True)
b = cp.Variable(8, integer=True)
nb = cp.Variable(8, integer=True)
wb = cp.Variable(8, integer=True)
rb = cp.Variable(8, integer=True)
k = 10
obj = cp.Minimize(cp.sum(rh*10+(th+nh)*10+nh*100+nb*200+rb*10))
con = []
con.append(rh[0]+wh[0]+th[0] == 50)
con.append(rb[0]+wb[0] == 13)
for t in range(8):
    con.append(k*th[t] >= nh[t])
    con.append(wh[t] == 4*r[t])
    con.append(wb[t] == 1*r[t])
    con.append(h[t] == rh[t]+wh[t]+th[t]+nh[t])
    con.append(b[t] == nb[t]+wb[t]+rb[t])

    con.append(rh[t] >= 0)
    con.append(wh[t] >= 0)
    con.append(th[t] >= 0)
    con.append(nh[t] >= 0)
    con.append(wb[t] >= 0)
    con.append(rb[t] >= 0)
    con.append(nb[t] >= 0)
for t2 in range(7):
    con.append(h[t2+1] - nh[t2+1] == h[t2])
    con.append(rh[t2+1] >= wh[t2])
    con.append(b[t2+1] == wb[t2]+rb[t2]+nb[t2])
prob = cp.Problem(obj, con)
prob.solve(solver=cp.GLPK_MI, verbose=True)
print('目标函数值: %d' % prob.value)
print(wh.value)
print(wb.value)
print('买入新手数：', nh.value)
print('教学熟练工数：', th.value)
