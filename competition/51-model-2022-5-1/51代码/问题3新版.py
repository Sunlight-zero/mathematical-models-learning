# -*- coding: utf-8 -*-
"""
Created on Mon May  2 17:03:00 2022

@author: lll
"""


import numpy as np
import matplotlib.pyplot as plt
import cvxpy as cp
import pandas as pd
df =pd.read_excel("data.xlsx",header = None);data = df.values;data = data.flatten()
r = data[0:104];n = 104;k = 20
h = cp.Variable(n,integer = True);rh = cp.Variable(n,integer = True);wh = cp.Variable(n,integer = True);th = cp.Variable(n,integer = True);nh = cp.Variable(n,integer = True)
b = cp.Variable(n,integer = True);nb = cp.Variable(n,integer = True);wb = cp.Variable(n,integer = True);rb = cp.Variable(n,integer = True)
weekly_cost = cp.Variable(n,integer = True)
u = cp.Variable(n,integer = True)#新变量 每周损耗
#obj = cp.Minimize(cp.sum(weekly_cost))
obj = cp.Minimize(cp.sum((rh*5+rb*10)+(th+nh)*10+(nh*100+nb*200)))
con =[]
con.append(rh[0]+wh[0]+th[0]==50)
con.append(rb[0]+wb[0]==13)
for t in range(n):
    #con.append(weekly_cost[t]==(rh[t]*5+rb[t]*10)+(th[t]+nh[t])*10+(nh[t]*100+nb[t]*200))
    con.append(k*th[t]>= nh[t])
    con.append(wh[t]== 4*r[t])
    con.append(wb[t]== 1*r[t])
    con.append(h[t] == rh[t]+wh[t]+th[t]+nh[t])
    con.append(b[t] == nb[t]+wb[t]+rb[t])
    con.append(rh[t]>=0);con.append(wh[t]>=0);con.append(th[t]>=0);con.append(nh[t]>=0);con.append(wb[t]>=0);con.append(rb[t]>=0);con.append(nb[t]>=0) 
    con.append(u[t]<=wb[t]*0.1+0.5);con.append(wb[t]*0.1+0.5<=u[t]+0.9999999999)#四舍五入
for t2 in range(n-1):
    con.append(h[t2+1] -nh[t2+1]== h[t2]-4*u[t2])
    con.append(rh[t2+1]>=wh[t2]-4*u[t2])
    con.append(b[t2+1] == wb[t2]+rb[t2]+nb[t2]+nb[t2+1]-u[t2])
prob =cp.Problem(obj,con)
prob.solve(solver = cp.SCIP, verbose = True)
print('目标函数值: %f' % prob.value)
print('每周购买新手数量:',nh.value,cp.sum(nh).value)
print('每周购买新艇数量:',nb.value)
print('每周保养手数量:',rh.value)
print('每周保养艇数量:',rb.value)
print('每周教学手总数:',nh.value+th.value)
print('每周花费:',weekly_cost.value)
nh1 = pd.DataFrame(nh.value)
nb1 = pd.DataFrame(nb.value)
rh1 = pd.DataFrame(rh.value)
rb1 = pd.DataFrame(rb.value)
th1 = pd.DataFrame(nh.value+th.value)
wc1 = pd.DataFrame(weekly_cost.value)
print('awa')
# writer = pd.ExcelWriter("d://问题3结果.xlsx")
# nh1.to_excel(excel_writer=writer, sheet_name='sheet_1')
# nb1.to_excel(excel_writer=writer, sheet_name='sheet_2')
# rh1.to_excel(excel_writer=writer, sheet_name='sheet_3')
# rb1.to_excel(excel_writer=writer, sheet_name='sheet_4')
# th1.to_excel(excel_writer=writer, sheet_name='sheet_5')
# wc1.to_excel(excel_writer=writer, sheet_name='sheet_6')
# writer.save()
# writer.close()