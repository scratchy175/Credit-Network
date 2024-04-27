#!/opt/homebrew/Caskroom/miniconda/base/envs/graph/bin/python

import sys
import networkx as nx
import random
from datetime import date,timedelta
from graph_utils import save_graph
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt



min_weight = 100
max_weight = 1000000
min_date = 2000


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
            G.add_edge(target, new_node, weight=random.randint(min_weight,max_weight), date=random_date(min_date))
    
    return G

import random
from datetime import datetime, timedelta

def erdos_renyi_graph(n, p, seed=None):
    # Create an Erdős–Rényi graph (not a multigraph)
    G = nx.erdos_renyi_graph(n, p, directed=True, seed=seed)

    # Add date and weight attributes to edges
    for u, v in G.edges():
        # Generate random date

        # Add date and weight attributes to edge
        G[u][v]['date'] = random_date(min_date)
        G[u][v]['weight'] = random.randint(min_weight, max_weight)

    return nx.MultiDiGraph(G)

def create_new_graph():
    """
    Demande à l'utilisateur de choisir un type de graphe.
    """
    print("Choisissez un type de graphe :")
    print("1. Modèle de Barabási-Albert")
    print("2. Modèle Erdős-Rényi")
    choice = input("Votre choix : ")

    if choice == "1":
        num_nodes = int(input("Nombre de noeuds : "))
        m = int(input("Nombre d'arêtes à attacher à chaque nouveau noeud : "))
        G = directed_BA_model_in_degree_with_min_out_degree(num_nodes, m)
        type_graph = f"BA_m{m}"
    elif choice == "2":
        num_nodes = int(input("Nombre de noeuds : "))
        p = float(input("Probabilité d'ajouter une arête : "))
        G = erdos_renyi_graph(num_nodes, p)
        type_graph = f"ER_p{p}"
    else:
        print("Choix invalide.")
        sys.exit(1)

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graphs/{type_graph}_n{num_nodes}_e{num_edges}_{current_time}.gpickle"
    save_graph(G, filename)
    print("Graphe sauvegardé dans : ", filename)
    return G, filename

if __name__ == "__main__":
    G,_ = create_new_graph()
    """out_degrees = [G.out_degree(node) for node in G.nodes()]
    out_degrees.sort()
    plt.plot(out_degrees)
    plt.xlabel("Node Index")
    plt.ylabel("Out-Degree")
    plt.title("Out-Degree Distribution")
    plt.show()"""

    #print(f"Diameter of the graph: {nx.diameter(G)}")

    # FAIRE UN TRUC AVEC LA SEED