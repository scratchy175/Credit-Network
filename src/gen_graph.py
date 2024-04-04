#!/opt/homebrew/Caskroom/miniconda/base/envs/graph/bin/python

import sys
import networkx as nx
import random
from datetime import date,timedelta
from graph_utils import save_graph
from datetime import datetime
import numpy as np


def random_date(start_year):
    # Generate a date between January 1 of start_year and December 31 of end_year
    start_date = date(start_year, 1, 1)
    end_date = date.today()

    # Calculate the number of days between start_date and end_date
    delta_days = (end_date - start_date).days

    # Generate a random number of days to add to start_date
    random_number_of_days = random.randint(0, delta_days)

    # Return the random date
    return start_date + timedelta(days=random_number_of_days)

def directed_BA_model_in_degree_with_min_out_degree(N, m, seed=None):
    """
    Generates a network using a directed version of the BA model focused on in-degree,
    ensuring each node has an out-degree of at least 1.
    
    Parameters:
    - N: Final number of nodes
    - m: Number of edges to attach from existing nodes to each new node
    - seed: Seed for the random number generator
    """
    min_weight = 100
    max_weight = 1000000
    min_date = 2000

    if m < 1 or m >= N:
        raise ValueError("m must be in range 1 <= m < N")
    
    np.random.seed(seed)
    
    # Start with an initial directed graph of m + 1 nodes, ensuring each has at least one out-degree
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(m + 1))
    for i in range(m):
        G.add_edge(i, i + 1, weight= random.randint(min_weight, max_weight),date=random_date(min_date))  # Ensure initial nodes have at least one out-degree
    
    # Add the rest of the nodes, each with m edges
    for new_node in range(m + 1, N):
        G.add_node(new_node)
        
        # Ensure at least one out-degree by selecting a random target for an outgoing link
        random_target = np.random.choice(list(G.nodes()))
        G.add_edge(new_node, random_target, weight= random.randint(min_weight,max_weight),date=random_date(min_date))
        
        # Calculate the probability for each node based on in-degree for the remaining m-1 links
        probs = np.array([G.in_degree(node) for node in G.nodes()])
        total_in_degree = probs.sum()
        probs = probs / total_in_degree
        
        # Choose m-1 distinct nodes to connect to, excluding the randomly selected target
        possible_targets = [node for node in G.nodes() if node != random_target]
        probs_adjusted = np.array([G.in_degree(node) for node in possible_targets])
        probs_adjusted = probs_adjusted / probs_adjusted.sum()
        
        targets = np.random.choice(possible_targets, size=m-1, replace=False, p=probs_adjusted)
        for target in targets:
            G.add_edge(target, new_node, weight= random.randint(min_weight,max_weight),date=random_date(min_date))
    
    return G

def create_new_graph(num_nodes):
    """
    Crée un nouveau graphe.
    """
    min_edges = int(input("Nombre minimum d'arêtes par noeud : "))
    max_edges = int(input("Nombre maximum d'arêtes par noeud : "))
    min_weight = int(input("Poids minimum d'une arête : "))
    max_weight = int(input("Poids maximum d'une arête : "))
    min_date = int(input("Année de début : "))

    # Create a MultiDiGraph
    G = nx.MultiDiGraph()

    # Add nodes
    for node in range(1, num_nodes + 1):
        G.add_node(node)

    # Add edges with random labels
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                for _ in range(random.randint(min_edges, max_edges)):
                    G.add_edge(node1, node2, weight=random.randint(min_weight, max_weight), date=random_date(min_date))
    
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"graphs/graph_n{num_nodes}_e{num_edges}_{current_time}.gpickle"
    save_graph(G, filename)
    print("Graphe sauvegardé dans : ", filename)
    return G, filename

if __name__ == "__main__":
    create_new_graph(int(sys.argv[1]))
