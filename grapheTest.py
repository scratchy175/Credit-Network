import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import datetime
import random
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
    
    #np.random.seed(seed)
    
    # Start with an initial directed graph of m + 1 nodes, ensuring each has at least one out-degree
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(m + 1))
    for i in range(m):
        G.add_edge(i, i + 1, weight= random.randint(10,1000),date=random_date(2000))  # Ensure initial nodes have at least one out-degree
    
    # Add the rest of the nodes, each with m edges
    for new_node in range(m + 1, N):
        G.add_node(new_node)
        
        # Ensure at least one out-degree by selecting a random target for an outgoing link
        random_target = np.random.choice(list(G.nodes()))
        G.add_edge(new_node, random_target, weight= random.randint(10,1000),date=random_date(2000))
        
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
            G.add_edge(target, new_node, weight= random.randint(10,1000),date=random_date(2000))
    
    return G

# Parameters
N = 1000  # Final number of nodes
m = 20    # Number of edges from existing nodes to each new node, ensuring at least one out-degree

start_time = datetime.datetime.now()
# Generate the graph
G = directed_BA_model_in_degree_with_min_out_degree(N, m, seed=42)

end_time = datetime.datetime.now()
print(f"Time taken: {end_time - start_time}")


# print out_degree and in_degree of the graph
"""for node in G.nodes():
    print(f"Node {node} has out_degree {G.out_degree(node)} and in_degree {G.in_degree(node)}")
"""
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

out_degrees = [G.out_degree(node) for node in G.nodes()]
out_degrees.sort()
plt.plot(out_degrees)
plt.xlabel("Node Index")
plt.ylabel("Out-Degree")
plt.title("Out-Degree Distribution")
plt.show()

# Plot the graph
"""plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=False, node_size=50, arrowstyle='->', arrowsize=10, node_color='skyblue')
plt.title("Directed Barabási-Albert Model (In-Degree Focus with Min Out-Degree)")
plt.show()"""

import networkx as nx
import random
import matplotlib.pyplot as plt

def create_uniform_directed_multigraph(num_nodes, num_edges_per_node):
    """
    Create a uniform directed multigraph.

    Parameters:
    - num_nodes: Number of nodes in the graph.
    - num_edges_per_node: Number of edges per node.
    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(num_nodes))

    for _ in range(num_edges_per_node):
        for n in G.nodes():
            # Select a target node different from n
            possible_targets = list(G.nodes())
            possible_targets.remove(n)  # Avoid self-loops
            target = random.choice(possible_targets)
            
            # Add one directed edge from n to target
            G.add_edge(n, target)
            
            # Add another directed edge in the opposite direction to maintain uniformity
            G.add_edge(target, n)

    return G

# Parameters
num_nodes = 1000
num_edges_per_node = 20

# Create graph
G = create_uniform_directed_multigraph(num_nodes, num_edges_per_node)

# Draw the graph
"""pos = nx.spring_layout(G)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_size=700, arrowsize=20, node_color='lightblue', arrowstyle='->')
plt.title('Uniform Directed Multigraph')
plt.show()"""

# print out_degree and in_degree of the graph
"""for node in G.nodes():
    print(f"Node {node} has out_degree {G.out_degree(node)} and in_degree {G.in_degree(node)}")
"""
#print(f"Number of nodes: {G.number_of_nodes()}")
##print(f"Number of edges: {G.number_of_edges()}")



def create_directed_multigraph_with_edge_factor(num_nodes, edge_factor=20):
    """
    Create a directed multigraph where the total number of edges is
    the number of nodes multiplied by a specified edge factor.

    Parameters:
    - num_nodes: Number of nodes in the graph.
    - edge_factor: Factor to determine the number of edges based on the number of nodes.
    """
    G = nx.MultiDiGraph()
    G.add_nodes_from(range(num_nodes))
    
    total_edges = num_nodes * edge_factor
    for _ in range(total_edges):
        # Select a source and a target node, ensuring no self-loops
        source = random.choice(list(G.nodes()))
        possible_targets = list(G.nodes())
        possible_targets.remove(source)  # Avoid self-loops
        target = random.choice(possible_targets)
        
        # Add one directed edge from source to target
        G.add_edge(source, target)

    return G

# Parameters for your specific example
num_nodes = 1000
edge_factor = 20  # You want the total number of edges to be 20 times the number of nodes

# Create the graph
G = create_directed_multigraph_with_edge_factor(num_nodes, edge_factor)

"""for node in G.nodes():
    print(f"Node {node} has out_degree {G.out_degree(node)} and in_degree {G.in_degree(node)}")

print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")
"""
"""nx.draw(G, with_labels=False, node_size=50, arrowstyle='->', arrowsize=10, node_color='skyblue')
plt.show()"""


import networkx as nx
import matplotlib.pyplot as plt
import random

# Parameters
n = 10000  # Number of nodes
p = 0.002  # Probability of edge creation

# Create an Erdős–Rényi graph (not a multigraph)
G = nx.erdos_renyi_graph(n, p, directed=True, seed=42)

# To convert it into a MultiDiGraph (if needed)
MG = nx.MultiDiGraph(G)

# If you need to add multiple edges manually, you can do something like:
# for _ in range(100):  # Example: Attempt to add 100 edges randomly
#     u, v = random.sample(range(n), 2)
#     if random.random() < p:  # Use the same probability as before
#         MG.add_edge(u, v)


print(f"Number of nodes: {MG.number_of_nodes()}")
print(f"Number of edges: {MG.number_of_edges()}")
# sort by out degree and draw a plot of out_degree to see the distribution
out_degrees = [MG.out_degree(node) for node in MG.nodes()]
out_degrees.sort()
plt.plot(out_degrees)
plt.xlabel("Node Index")
plt.ylabel("Out-Degree")
plt.title("Out-Degree Distribution")
#plt.show()

# diameter of a graph
print(f"Diameter of the graph: {nx.diameter(MG)}")
# Draw the graph
pos = nx.spring_layout(MG)  # positions for all nodes
#nx.draw(MG, pos, with_labels=True, node_size=700, node_color="lightblue", arrows=True)
#plt.show()
