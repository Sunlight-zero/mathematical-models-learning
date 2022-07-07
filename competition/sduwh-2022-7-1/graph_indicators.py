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
    num_nodes = graph.number_of_nodes()
    for subgraph in nx.connected_components(graph):
        num_subgraph_nodes = len(subgraph)
        importance = num_subgraph_nodes / num_nodes # importance degree of a subgraph
        entropy -= importance * np.log(importance)
    return entropy


def normalized_connectivity_entropy(graph: nx.graph) -> float:
    """
    Calculate the normalized connectivity entropy.
    The max connecivity entropy of a graph is ln(n),
    where n is the number of the nodes.
    Thus the normalized connectivity entropy is calculated by
    R = [ln(n) - CE] / ln(n).
    """
    log_num_nodes = np.log(graph.number_of_nodes())
    entropy = connectivity_entropy(graph)
    return (log_num_nodes - entropy) / log_num_nodes


def RS(graph: nx.graph) -> float:
    """
    Calculate the relative maximum connected component size,
    which is defined as the ratio of number of nodes of the
    maximum connected commonent and the number of total nodes:
    RS(G) = max(V(g), g is a connected graph) / V(G).
    """
    subgraph_sizes = [
        len(subgraph)
        for subgraph in nx.connected_components(graph)]
    return np.max(subgraph_sizes) / graph.number_of_nodes()


def graph_features(graph: nx.graph) -> tuple:
    """
    Calculate the CE, RCE and RS at the same time.
    """
    num_nodes = graph.number_of_nodes()
    log_num_nodes = np.log(num_nodes)
    subgraph_sizes = list(map(
        lambda subgraph: len(subgraph),
        nx.connected_components(graph))
    )
    RS = np.max(subgraph_sizes) / num_nodes
    CE = -sum(map(
        lambda size: size / num_nodes * np.log(size / num_nodes),
        subgraph_sizes
    ))
    RCE = (log_num_nodes - CE) / log_num_nodes
    return (CE, RCE, RS)


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
