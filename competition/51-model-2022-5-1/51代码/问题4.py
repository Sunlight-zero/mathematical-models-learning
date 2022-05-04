# -*- coding: utf-8 -*-
"""
Created on Sun May  1 17:06:51 2022

@author: lll
"""



import os
import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp

M =9999999
r =  np.array([11,5,4,7,16,6,5,7])
h = cp.Variable(8,integer = True)
rh = cp.Variable(8,integer = True)
wh = cp.Variable(8,integer = True)
th = cp.Variable(8,integer = True)
nh = cp.Variable(8,integer = True)
b = cp.Variable(8,integer = True)
nb = cp.Variable(8,integer = True)
wb = cp.Variable(8,integer = True)
rb = cp.Variable(8,integer = True)
#新变量 每周损耗
u = cp.Variable(8,integer = True)
#新手分段变量
nb1 = cp.Variable(8,integer = True)
nb2 = cp.Variable(8,integer = True)
nb3 = cp.Variable(8,integer = True)

nh1 = cp.Variable(8,integer = True)
nh2 = cp.Variable(8,integer = True)
nh3 = cp.Variable(8,integer = True)

y1 = cp.Variable(8,integer = True)
y2 = cp.Variable(8,integer = True)
y3 = cp.Variable(8,integer = True)

z1 = cp.Variable(8,boolean = True)
z2 = cp.Variable(8,boolean = True)
z3 = cp.Variable(8,boolean = True)

k = 20#不超过20
obj = cp.Minimize(cp.sum(rh*5+(th+nh)*10+nh*100+nb*200+rb*10))
con =[]
con.append(rh[0]+wh[0]+th[0]==50)
con.append(rb[0]+wb[0]==13)
for t in range(8):
    con.append(k*th[t]>= nh[t])
    con.append(wh[t]== 4*r[t])
    con.append(wb[t]== 1*r[t])
    con.append(h[t] == rh[t]+wh[t]+th[t]+nh[t])
    con.append(b[t] == nb[t]+wb[t]+rb[t])
    #分段
    con.append(nb[t] == nb1[t]+nb2[t]+nb3[t])
    con.append(5*y2[t]<=nb1[t]);con.append(nb1[t]<=5*y1[t])
    con.append(5*y3[t]<=nb2[t]);con.append(nb2[t]<=5*y2[t])
    con.append(nb3[t]<=M*y3[t])
    con.append(0<=nb3[t]);con.append(0<=nb1[t]);con.append(nb1[t]<=5);con.append(0<=nb2[t]);con.append(nb2[t]<=5)
    
    con.append(nh[t] == nh1[t]+nh2[t]+nh3[t])
    con.append(20*z2[t]<=nh1[t]);con.append(nh1[t]<=20*z1[t])
    con.append(20*z3[t]<=nh2[t]);con.append(nh2[t]<=20*z2[t])
    con.append(nh3[t]<=M*z3[t])
    con.append(0<=nh3[t]);con.append(0<=nh1[t]);con.append(nh1[t]<=20);con.append(0<=nh2[t]);con.append(nh2[t]<=20)
    
    con.append(rh[t]>=0)
    con.append(wh[t]>=0)
    con.append(th[t]>=0)
    con.append(nh[t]>=0)
    con.append(wb[t]>=0)
    con.append(rb[t]>=0)
    con.append(nb[t]>=0)
    
    con.append(u[t]<=wh[t]*0.1)#损坏0.1
    con.append(wh[t]*0.1<=u[t]+0.99999999999999)
for t2 in range(7):
    con.append(h[t2+1] -nh[t2+1]== h[t2]-u[t2])
    con.append(rh[t2+1]>=wh[t2])
    con.append(b[t2+1] == wb[t2]+rb[t2]+nb[t2]+nb[t2+1])
prob =cp.Problem(obj,con)
prob.solve(solver = cp.GLPK_MI,verbose = True)
print('目标函数值: %f' % prob.value)
print(th.value)
