"""
先按最大度割点，当出现最大度相同时，计算连通熵，按连通熵最大割点
"""

import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
import os

os.chdir('competition/sduwh-2022-7-1/')

from graph_indicators import graph_features

def connectivity_entropy(graph: nx.graph) -> float:
    """
    定义快速连通熵算法
    """
    return -np.sum(
        len(subgraph) / graph.number_of_nodes() \
            * np.log(len(subgraph) / graph.number_of_nodes())
        for subgraph in nx.connected_components(graph))

THRESHOLD = 3 # 当最大点的度数小于等于这个阈值时，不再按最大度进行切割。
EPSILON = 1e-6 # 浮点数比较的允差

# 建图，并导入边
graph = nx.Graph()
edges_table = pd.read_csv("graph/附件3.txt", sep=" ", header=None).values
graph.add_edges_from(edges_table)
num_nodes = graph.number_of_nodes()

# 拷贝一份子图，并用列表存储各种指标的变化
graph_to_del = deepcopy(graph)
list_del_nodes = []
list_RCE = []

while graph_to_del.nodes():
    degrees = np.array(graph_to_del.degree)
    # 计算指标
    ce, rce, rs = graph_features(graph_to_del)
    list_RCE.append(rce)
    
    # 定义割点后连通熵的计算函数
    def ce_after_cut(node, graph):
        subgraph = deepcopy(graph)
        subgraph.remove_node(node)
        return connectivity_entropy(subgraph)
    
    # 寻找割后具有最大连通熵的点
    nodes = list(graph_to_del.nodes())
    array_ce_after_cut = np.array(
        [(node, ce_after_cut(node, graph_to_del)) for node in nodes])
    max_ce_pos = np.argmax(array_ce_after_cut[:, 1])
    node_to_del = nodes[max_ce_pos]
    # max_ce = np.max(array_ce_after_cut[:, 1])
    # max_ce_nodes = array_ce_after_cut[array_ce_after_cut[:, 1] > max_ce - EPSILON]

    # # 在最大连通熵的点中寻找最大度
    # max_degree_node_pos = np.argmax(graph_to_del.degree[node] for node in max_ce_nodes)
    # node_to_del = max_ce_nodes[0, max_degree_node_pos]

    graph_to_del.remove_node(node_to_del)
    list_del_nodes.append(node_to_del)


# 作图
plt.plot(range(len(list_del_nodes)), list_RCE, 'r*')
plt.xlabel("step")
plt.ylabel("rce")
plt.show()
