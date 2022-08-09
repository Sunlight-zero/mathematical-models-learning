import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy
import os

os.chdir('competition/sduwh-2022-7-1/')

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

# 建图，并导入边
graph = nx.Graph()
edges_table = pd.read_csv("graph/附件3.txt", sep=" ", header=None).values
graph.add_edges_from(edges_table)
num_nodes = graph.number_of_nodes()

# 拷贝一份子图，并用列表存储各种指标的变化
graph_to_del = deepcopy(graph)
list_del_nodes_1 = []
list_cut_degree = []
list_rce_1 = []

while np.max(graph_to_del.degree(), axis=0)[1] > 1:
    degrees = np.array(graph_to_del.degree)
    # 计算指标
    list_rce_1.append(rce(graph_to_del))
    max_degree = np.max(degrees[:, 1])
    max_degree_nodes = degrees[degrees[:, 1] == max_degree]
    
    if max_degree <= 1:
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
    list_del_nodes_1.append(node_to_del)
    list_cut_degree.append(max_degree)

graph_to_del = deepcopy(graph)
graph_to_del.add_edges_from(edges_table)

list_rce_2 = []
list_del_nodes_2 = []

while np.max(graph_to_del.degree(), axis=0)[1] > 1:
    list_rce_2.append(rce(graph_to_del))

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
        delta_ce.append(ce - list_ce_before_cut[subgraph_idx])
    
    node_to_cut_idx = np.argmax(delta_ce)
    node_to_del = candidate_nodes[node_to_cut_idx]
    graph_to_del.remove_node(node_to_del)

    list_del_nodes_2.append(node_to_del)

plt.plot(range(len(list_del_nodes_1)), list_rce_1, 'r*')
plt.plot(range(len(list_del_nodes_2)), list_rce_2, 'b*')
plt.savefig("p4 - CMP - MD & CE")
