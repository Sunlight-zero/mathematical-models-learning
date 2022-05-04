# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:21:52 2022

@author: lll
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import pandas as pd

T = 104

os.chdir('competition/51-model-2022-5-1')
r = pd.read_excel('data.xlsx', header=None).values.flatten()
h = cp.Variable(T,integer = True)
rh = cp.Variable(T,integer = True)
wh = cp.Variable(T,integer = True)
th = cp.Variable(T,integer = True)
nh = cp.Variable(T,integer = True)
b = cp.Variable(T,integer = True)
nb = cp.Variable(T,integer = True)
wb = cp.Variable(T,integer = True)
rb = cp.Variable(T,integer = True)
#新变量 每周损耗
u = cp.Variable(T,integer = True)

k = 10
obj = cp.Minimize(cp.sum(rh*5+(th+nh)*10+nh*100+nb*200+rb*10))
con =[]
con.append(rh[0]+wh[0]+th[0]==50)
con.append(rb[0]+wb[0]==13)
for t in range(T):
    con.append(k*th[t]>= nh[t])
    con.append(wh[t]== 4*r[t])
    con.append(wb[t]== 1*r[t])
    con.append(h[t] == rh[t]+wh[t]+th[t]+nh[t])
    con.append(b[t] == nb[t]+wb[t]+rb[t])
    
    con.append(rh[t]>=0)
    con.append(wh[t]>=0)
    con.append(th[t]>=0)
    con.append(nh[t]>=0)
    con.append(wb[t]>=0)
    con.append(rb[t]>=0)
    con.append(nb[t]>=0)
    
    con.append(u[t]<=wh[t]*0.2)
    con.append(wh[t]*0.2<=u[t]+0.9999999999)
for t2 in range(T - 1):
    con.append(h[t2+1] -nh[t2+1]== h[t2]-u[t2])
    con.append(rh[t2+1]>=wh[t2])
    con.append(b[t2+1] == wb[t2]+rb[t2]+nb[t2]+nb[t2+1])
prob =cp.Problem(obj,con)
prob.solve(solver = cp.MOSEK, verbose = True)
print('目标函数值: %d' % prob.value)
print(th.value)
