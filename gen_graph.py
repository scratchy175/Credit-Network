#!/opt/homebrew/Caskroom/miniconda/base/envs/graph/bin/python

import networkx as nx
import random
from datetime import date,timedelta
from graph_utils import save_graph


# Parameters
num_nodes = 5  # Number of nodes in the graph
min_edges = 0   # Minimum number of edges between two nodes
max_edges = 2   # Maximum number of edges between two nodes
min_weight = 1  # Minimum weight of an edge
max_weight = 10 # Maximum weight of an edge
min_date = 2000  # Minimum date of an edge

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

save_graph(G)


