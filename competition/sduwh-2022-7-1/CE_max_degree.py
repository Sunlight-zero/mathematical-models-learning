import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from copy import deepcopy
from save_list import writelist

os.chdir("competition/sduwh-2022-7-1/")
EPSILON = 1E-6

def connectivity_entropy(graph: nx.graph) -> float:
    """
    定义快速连通熵算法
    """
    return -np.sum(
        len(subgraph) / graph.number_of_nodes() \
            * np.log(len(subgraph) / graph.number_of_nodes())
        for subgraph in nx.connected_components(graph))
    
def rce(graph: nx.Graph) -> float:
    return (np.log(graph.number_of_nodes()) - connectivity_entropy(graph)) / np.log(graph.number_of_nodes())

def find(node, node_fathers):
    """
    Find the father of a node.
    """
    while node_fathers[node] != node:
        node = node_fathers[node]
    
    return node

graph_to_del = nx.Graph()
edges_table = pd.read_csv("graph/附件3.txt", sep=" ", header=None).values
graph_to_del.add_edges_from(edges_table)

list_ce = []
list_rce = []
list_del_nodes = []

while np.max(graph_to_del.degree(), axis=0)[1] > 1:
    list_rce.append(rce(graph_to_del))

    num_nodes = graph_to_del.number_of_nodes()

    list_ce_before_cut = [] # 每个子图切割前的连通熵
    subgraphs = []

    for subgraph_set in nx.connected_components(graph_to_del):
        list_ce_before_cut.append(
            len(subgraph_set) / (num_nodes - 1) * \
                np.log(len(subgraph_set) / (num_nodes - 1)))
        subgraphs.append(graph_to_del.subgraph(subgraph_set))

    degrees = np.array(graph_to_del.degree)
    candidate_nodes = degrees[degrees[:, 1] >= 2][:, 0]

    node_fathers = [] # 储存每个节点的父节点
    subgraph_representations = [] # 记录每个子图的代表元

    for node_set in nx.connected_components(graph_to_del):
        for idx, node in enumerate(node_set):
            if idx == 0:
                subgraph_representations.append(node)
                father = node
            
            node_fathers.append((node, father))

    node_fathers.sort(key=lambda x: x[0])
    node_fathers = dict(node_fathers) # 以字典形式存储该结构
    representation_to_idx = dict(
        (rep, idx) for idx, rep in enumerate(subgraph_representations))

    delta_ce = []

    for node in candidate_nodes:
        subgraph_idx = representation_to_idx[find(node, node_fathers)] # 找出该节点所属的子图
        subgraph = nx.Graph(subgraphs[subgraph_idx]) # 将 frozen 的图转为正常图
        subgraph.remove_node(node)
        ce = connectivity_entropy(subgraph) # 计算子图的连通熵
        delta_ce.append((node, ce - list_ce_before_cut[subgraph_idx]))
    
    delta_ce = np.array(delta_ce)
    max_delta_ce = np.max(delta_ce[:, 1])
    nodes_to_choose = delta_ce[delta_ce[:, 1] > max_delta_ce - EPSILON][:, 0]
    dict_degrees = dict(degrees)
    nodes_to_choose_degrees = map(lambda node: dict_degrees[node], nodes_to_choose)
    node_to_del = nodes_to_choose[np.argmax(nodes_to_choose_degrees)]
    graph_to_del.remove_node(node_to_del)

    list_del_nodes.append(node_to_del)

plt.plot(range(len(list_del_nodes)), list_rce, 'r*')
plt.savefig("p4 - CE")
writelist(list_del_nodes, "pro4-ce-md.txt", "nodes_to_del")
