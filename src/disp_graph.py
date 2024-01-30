import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph


def print_graph(G):
    # Print the list of nodes and edges
    print("List of Nodes:", list(G.nodes()))
    print("List of Edges:", list(G.edges(keys=True)))

    # Print the list of edges with labels
    list_of_edges_with_labels = [(u, v, G[u][v][k]['label']) for u, v, k in G.edges(keys=True)]
    print("List of Edges with Labels:", list_of_edges_with_labels)

# to change 
def draw_graph(G, pos):
    A= to_agraph(G)
    A.layout('dot')
    A.draw('file.png')
    

def save_png(G, filename):
    # Graphviz layout options
    G.graph['edge'] = {'arrowsize': '0.6', 'splines': 'curved'}
    G.graph['graph'] = {'scale': '1'}

    # Convert to AGraph and draw
    A = to_agraph(G)
    A.layout('dot')
    A.draw(filename)