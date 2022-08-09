import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

os.chdir('competition/sduwh-2022-7-1/')

from graph_indicators import graph_features


def connectivity_entropy(graph: nx.graph) -> float:
    """
    定义快速连通熵算法
    """
    return - np.sum(
        len(subgraph) / graph.number_of_nodes() \
            * np.log(len(subgraph) / graph.number_of_nodes())
        for subgraph in nx.connected_components(graph))


graph_table = pd.read_csv("graph1.txt", sep=" ", header=None).values
graph = nx.Graph()
graph.add_edges_from(graph_table)

num_node_list = [len(graph.nodes())] # 节点数
num_connected_branches = [len(list(nx.connected_components(graph)))] # 连通分支数
# connectivity_entropy_list = [connectivity_entropy(graph)]
# node_connectivity_list = [node_connectivity(graph)]


flag = True
for _ in range(100):
    degrees = np.array(graph.degree)
    # 寻找最大的度节点
    max_degree_id = np.argmax(degrees[:, 1])
    max_degree_node = degrees[max_degree_id, 0]
    graph.remove_node(max_degree_node)

    # 在此计算各种指标
    num_node_list.append(len(graph.nodes()))
    num_connected_branches.append(len(list(nx.connected_components(graph))))
    # connectivity_entropy_list.append(connectivity_entropy(graph))
    # node_connectivity_list.append(node_connectivity(graph))
    
plt.rc('font',size=50)
nx.draw(graph, node_size=1)
plt.show()
print('return 0')
