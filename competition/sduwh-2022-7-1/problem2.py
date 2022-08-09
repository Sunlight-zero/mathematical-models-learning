import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

os.chdir('competition/sduwh-2022-7-1/')

from graph_indicators import *
from save_list import writelist


graph_table = pd.read_csv("graph1.txt", sep=" ", header=None).values
graph = nx.Graph()
graph.add_edges_from(graph_table)

num_nodes = graph.number_of_nodes() # 节点数
del_nodes = []
num_connected_branches = [] # 连通分支数
connectivity_entropy_list = [] # 连通熵
rce_list = [] # 标准化连通熵
relative_size_list = [] # 相对最大连通分支规模
max_degree_list = [] # 最大节点度


flag = True
while graph.nodes():
    degrees = np.array(graph.degree)
    # 在此计算各种指标
    num_connected_branches.append(len(list(nx.connected_components(graph))))
    ce, rce, rs = graph_features(graph)
    connectivity_entropy_list.append(ce)
    rce_list.append(rce)
    relative_size_list.append(rs)
    max_degree_list.append(max(degrees[:, 1]))
    # 寻找最大的度节点
    max_degree_id = np.argmax(degrees[:, 1])
    max_degree_node = degrees[max_degree_id, 0]
    graph.remove_node(max_degree_node)
    del_nodes.append(max_degree_node)


list_del_nodes = list(range(num_nodes))
plt.plot(list_del_nodes, connectivity_entropy_list)
plt.ylabel('ce')
plt.savefig('p2 - ce')
plt.clf()
plt.plot(list_del_nodes, rce_list)
plt.ylabel('rce')
plt.savefig('p2 - rce')
plt.clf()
plt.plot(list_del_nodes, relative_size_list)
plt.ylabel('rs')
plt.savefig('p2 - rs')
plt.clf()
plt.plot(list_del_nodes, max_degree_list)
plt.ylabel('max degree')
plt.savefig('p2 - max_degree')
writelist(del_nodes, 'problem-2-del-nodes.txt')
plt.plot(list_del_nodes, rce_list, 'r*', label="$the-best-way$")
plt.savefig('p2 - plot')
print('return 0')
