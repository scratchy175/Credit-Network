#!/opt/homebrew/Caskroom/miniconda/base/envs/graph/bin/python

import sys
import networkx as nx
import random
from datetime import date,timedelta
from graph_utils import save_graph
from datetime import datetime


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
