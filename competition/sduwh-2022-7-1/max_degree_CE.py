"""
先按最大度割点，当出现最大度相同时，计算连通熵，按连通熵最大割点
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
import os
from save_list import writelist

os.chdir('competition/sduwh-2022-7-1/')

from graph_indicators import connectivity_entropy, graph_features

THRESHOLD = 1 # 当最大点的度数小于等于这个阈值时，不再按最大度进行切割。

# 建图，并导入边
graph = nx.Graph()
edges_table = pd.read_csv("graph/附件3.txt", sep=" ", header=None).values
graph.add_edges_from(edges_table)
num_nodes = graph.number_of_nodes()

# 拷贝一份子图，并用列表存储各种指标的变化
graph_to_del = deepcopy(graph)
list_del_nodes = []
list_cut_degree = []
list_RCE = []

while graph_to_del.nodes():
    degrees = np.array(graph_to_del.degree)
    # 计算指标
    ce, rce, rs = graph_features(graph_to_del)
    list_RCE.append(rce)
    max_degree = np.max(degrees[:, 1])
    max_degree_nodes = degrees[degrees[:, 1] == max_degree]
    
    if max_degree <= THRESHOLD:
        node_to_del = degrees[0, 0]
    elif len(max_degree_nodes > 1):
        # 记录所有具有最大度的点
        list_ce = []
        for node in max_degree_nodes[:, 0]:
            # 计算删去该点后的连通熵，选择最大的一个
            subgraph = deepcopy(graph_to_del)
            subgraph.remove_node(node)
            ce = connectivity_entropy(subgraph)
            list_ce.append(ce)
        max_node_id = np.argmax(list_ce)
        node_to_del = max_degree_nodes[max_node_id, 0]
    else:
        node_to_del = max_degree_nodes[0, 0]
    graph_to_del.remove_node(node_to_del)
    list_del_nodes.append(node_to_del)
    list_cut_degree.append(max_degree)

# 作图
writelist(list_del_nodes, "pro4-md-ce.txt", path="nodes_to_del")
plt.plot(range(num_nodes), list_RCE, 'r*')
plt.xlabel("step")
plt.ylabel("rce")
plt.show()
