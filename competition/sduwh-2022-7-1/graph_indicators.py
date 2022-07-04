import networkx as nx
import numpy as np
import pandas as pd


def connectivity_entropy(graph: nx.graph) -> float:
    """
    Calculate the connectivityentropy of a graph.
    The connectivity entropy is defined as:
    E = - Σ (n_k / n) ln(n_k / n),
    where n_k is the number of nodes of the k-th connectivity subgraph.
    """
    entropy = 0
    num_nodes = len(graph.nodes())
    for subgraph in nx.connected_components(graph):
        num_subgraph_nodes = len(subgraph)
        importance = num_subgraph_nodes / num_nodes # importance degree of a subgraph
        entropy -= importance * np.log(importance)
    return entropy

def node_connectivity(graph: nx.graph) -> float:
    """
    Calculate the connectivity.
    The connectivity of a unconnect graph is defined 
    as the maximum of its connective branches.
    The connectivity of null graph is defined as zero.
    """
    if graph.nodes():
        return min(nx.node_connectivity(graph.subgraph(subgraph_nodes)) 
            for subgraph_nodes in nx.connected_components(graph))
    else:
        return 0
