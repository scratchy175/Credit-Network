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
    G.add_nodes_from(range(m + 1),weight=0)
    for i in range(m):
        G.add_edge(i, i + 1, weight= random.randint(min_weight, max_weight),date=random_date(min_date))  # Ensure initial nodes have at least one out-degree
    
    # Add the rest of the nodes, each with m edges
    for new_node in range(m + 1, N):
        G.add_node(new_node, weight=0)

        
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
        
        targets = np.random.choice(possible_targets, size=m-1, replace=True, p=probs_adjusted)
        for target in targets:
            G.add_edge(target, new_node, weight=random.randint(min_weight,max_weight), date=random_date(min_date))
    
    return G

def directed_BA_model_in_degree_with_min_out_degree2(N, m, min_weight=1, max_weight=5, seed=None):
    """
    Generates a network using a directed version of the BA model focused on in-degree,
    ensuring each node has an out-degree of at least 1 and potentially multiple edges 
    between the same pair of nodes in the same direction.

    Parameters:
    - N: Final number of nodes
    - m: Number of edges to attach from existing nodes to each new node
    - min_weight, max_weight: The range for the weights of the edges
    - min_date, random_date: Functions or values to set random date attributes for the edges
    - seed: Seed for the random number generator
    """
    if m < 1 or m >= N:
        raise ValueError("m must be in range 1 <= m < N")

    np.random.seed(seed)
    random.seed(seed)

    # Start with an initial directed graph of m + 1 nodes
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(m + 1))
    for i in range(m):
        G.add_edge(i, i + 1, weight=random.randint(min_weight, max_weight), date=random_date(min_date))
    
    # Add the rest of the nodes, each with m edges
    for new_node in range(m + 1, N):
        G.add_node(new_node)

        # Calculate probabilities for each node based on in-degree
        probs = np.array([G.in_degree(node) + 1 for node in G.nodes()])  # +1 to ensure non-zero probability
        total_in_degree = probs.sum()
        probs = probs / total_in_degree

        # Choose m nodes to connect to (allowing repeats explicitly)
        targets = np.random.choice(G.nodes(), size=m, replace=True, p=probs)
        for target in targets:
            G.add_edge(new_node, target, weight=random.randint(min_weight, max_weight), date=random_date(min_date))
    
    return G

def erdos_renyi_multigraph2(n, p, seed=None):
    """
    Generate an Erdős-Rényi directed multigraph where multiple edges are possible
    between any pair of nodes.

    Args:
    n (int): Number of nodes.
    p (float): Probability of adding each possible edge.
    seed (int, optional): Random seed for reproducibility.
    min_weight (int): Minimum weight of edges.
    max_weight (int): Maximum weight of edges.
    min_date (datetime): Minimum date for random date generation.

    Returns:
    nx.MultiDiGraph: The generated directed multigraph.
    """
    # Ensure reproducibility
    if seed is not None:
        random.seed(seed)

    G = nx.MultiDiGraph()

    # Add nodes
    for node in range(n):
        G.add_node(node, weight=0)

    # Add edges with probability p and allow multiple edges
    for i in range(n):
        for j in range(n):
            if i != j:
                num_edges = random.choices([0, 1, 2, 3], [1-p, p*0.6, p*0.3, p*0.1])[0]
                for _ in range(num_edges):
                    date = random_date(min_date)
                    weight = random.randint(min_weight, max_weight)
                    G.add_edge(i, j, date=date, weight=weight)

    return G

def erdos_renyi_multigraph(n, p, seed=None, max_edges=3):
    """
    Generate an Erdős-Rényi directed multigraph where the number of edges between any pair of nodes
    is randomly determined up to a maximum number.

    Args:
    n (int): Number of nodes.
    p (float): Base probability of adding an edge set.
    seed (int, optional): Random seed for reproducibility.
    max_edges (int): Maximum number of edges that can exist between any two nodes.
    min_weight (int): Minimum weight of edges.
    max_weight (int): Maximum weight of edges.
    min_date (datetime): Minimum date for random date generation.

    Returns:
    nx.MultiDiGraph: The generated directed multigraph.
    """
    # Ensure reproducibility
    if seed is not None:
        random.seed(seed)

    G = nx.MultiDiGraph()

    # Add nodes
    for node in range(n):
        G.add_node(node, weight=0)

    # Add edges with randomized edge counts up to max_edges
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < p:
                # Random number of edges from 0 to max_edges
                num_edges = random.randint(0, max_edges)
                for _ in range(num_edges):
                    date = random_date(min_date)
                    weight = random.randint(min_weight, max_weight)
                    G.add_edge(i, j, date=date, weight=weight)

    return G

def create_erdos_renyi_multidigraph(n, p, max_edges=3):
    """
    Create an Erdős–Rényi directed multigraph where each pair of nodes might have multiple directed edges.

    Parameters:
        n (int): Number of nodes in the graph.
        p (float): Probability of creating an edge between any two nodes.
        max_edges (int): Maximum number of edges allowed between two nodes in the same direction.

    Returns:
        nx.MultiDiGraph: The generated directed multigraph.
    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(n))  # Add nodes

    for i in range(n):
        for j in range(n):
            if i != j:  # No loops in this graph setup
                num_edges = random.choices(range(max_edges + 1), [p] + [(1-p)/max_edges] * max_edges)[0]
                for _ in range(num_edges):
                    G.add_edge(i, j)

    return G


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
        G = erdos_renyi_multigraph2(num_nodes, p, seed=None)
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



def has_multiple_directed_edges(G):
    """
    Check if the graph has multiple directed edges between any pair of nodes.

    Args:
    G (nx.DiGraph or nx.MultiDiGraph): The graph to check.

    Returns:
    bool: True if there are multiple directed edges between any pair of nodes, False otherwise.
    """
    for u in G.nodes():
        visited = {}
        for v in G.neighbors(u):
            if v in visited:
                # If the target node is already in the visited dict, it means there's more than one edge to this node
                return True
            visited[v] = True

            # In case of MultiDiGraph, explicitly check for multiple edges
            if isinstance(G, nx.MultiDiGraph) and G.number_of_edges(u, v) > 1:
                return True
    return False

def max_edges_in_same_direction(graph):
    max_edges = 0
    for u in graph.nodes():
        for v in graph.nodes():
            # The number of edges from u to v
            num_edges = graph.number_of_edges(u, v)
            if num_edges > max_edges:
                max_edges = num_edges
    return max_edges

if __name__ == "__main__":
    G,_ = create_new_graph()
    #friends_dict = generate_friends_for_each_node(G)
    #print(friends_dict)
    #print(len(friends_dict))
    out_degrees = [G.out_degree(node) for node in G.nodes()]
    out_degrees.sort()
    plt.plot(out_degrees)
    plt.xlabel("Node Index")
    plt.ylabel("Out-Degree")
    plt.title("Out-Degree Distribution")
    plt.show()

    print(f"Diameter of the graph: {nx.diameter(G)}")

    # FAIRE UN TRUC AVEC LA SEED


    #from graph_utils import load_graph
    #G = load_graph("graphs/ER_p0.02_n100_e201_20240503_230337.gpickle")
    # print(G.edges())
    # print out degrees
    # for node in G.nodes():
    #     print(f"Node {node} has out-degree {G.out_degree(node)}")

    """for node in G.nodes():
        print(f"Node {node} has out-degree {G.in_degree(node)}")"""
    
    # check if the graph is a multi graph
    
    # Check if the graph is a multigraph
    if has_multiple_directed_edges(G):
        print("The graph has multiple directed edges.")
        print(f"The maximum number of edges in the same direction is {max_edges_in_same_direction(G)}.")
    else:
        print("The graph does not have multiple directed edges.")
