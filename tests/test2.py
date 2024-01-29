import datetime
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from networkx.drawing.nx_agraph import to_agraph
from PIL import Image
import io

def graph_to_image(G, pos):
    A = to_agraph(G)

    # Set node positions in AGraph
    for node in G.nodes():
        n = A.get_node(node)
        n.attr['pos'] = f"{pos[node][0]*72},{pos[node][1]*72}"  # Multiply by 72 to convert to points

    # Adjust graph attributes for better rendering
    """A.graph_attr['dpi'] = '300'
    A.graph_attr['splines'] = 'curved'
    A.node_attr['shape'] = 'circle'
    A.edge_attr['len'] = '0.1'  # Adjust this value as needed
    A.edge_attr['overlap'] = 'true'
    A.edge_attr['labeldistance'] = '2.5'
    A.edge_attr['labelangle'] = '90'
    A.edge_attr['labelfloat'] = 'true'"""
    A.edge_attr['overlap'] = 'false'
    A.graph_attr['splines'] = 'curved'

    A.layout('neato',args='-n')  # '-n' tells Graphviz to use the node positions provided


    png_str = A.draw(format='png')
    sio = io.BytesIO(png_str)
    return Image.open(sio)

def update(num, G, edges, ax, pos):
    if num > 0 and num <= len(edges):
        remove_edge(G, edges[num - 1])
    ax.clear()
    ax.set_axis_off()
    ax.imshow(graph_to_image(G, pos))

def remove_edge(G, edge):
    if G.has_edge(*edge):
        keys = list(G[edge[0]][edge[1]].keys())
        G.remove_edge(*edge, keys[0])

# Initialize graph
G = nx.MultiDiGraph()
# Add edges with attributes
G.add_edge('A', 'B', weight=100, date=datetime.date(2022, 1, 1))
G.add_edge('A', 'B', weight=200, date=datetime.date(2023, 1, 1))
G.add_edge('B', 'C', weight=150, date=datetime.date(2024, 1, 1))



edges = [(u, v) for u, v, k in G.edges(keys=True)]

# Precompute positions of the nodes
pos = nx.spring_layout(G)  # You can use other layout algorithms as well

# Create a matplotlib figure
fig, ax = plt.subplots(figsize=(6, 4))
ax.set_axis_off()

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=range(len(edges) + 1), fargs=(G, edges, ax, pos), repeat=False, interval=2000, blit=False)

plt.show()
