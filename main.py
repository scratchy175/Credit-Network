from processing import *
from add_weights import *
from gen_graph import *
from graph_utils import *


if __name__ == "__main__":
    filename = 'graph.pkl'
    min_weight = 1
    max_weight = 10
    # maybe ask the user if he want to load a graph or generate a new one
    G = load_graph(filename)

    add_random_weights(G, min_weight, max_weight) # later choose strategy to add weights

    strategy_func = oldest_first

    edges_removed = True
    while edges_removed:
        edges_removed = False
        accumulated_weights = {}

        for node in G.nodes():
            if process_node_edges(G, node, accumulated_weights, strategy_func):
                edges_removed = True

        for node, weight in accumulated_weights.items():
            G.nodes[node]['weight'] += weight

# choose where to display the graph. each step? at the end ? or both?

