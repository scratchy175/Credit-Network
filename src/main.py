import os
from processing import process_node_edges
from graph_utils import save_graph
from file_utils import save_parameters
from disp_graph import save_png
from input_utils import *
import copy
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

def plot_graph(data):
    """Plot a graph with number of bankruptcies on the x-axis and total_weight on the y-axis."""
    # Unpack the data
    total_weights, bankruptcies = zip(*data)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(bankruptcies, total_weights, marker='o')

    # Label the axes
    plt.xlabel('Poids total')
    plt.ylabel('Nombre de faillites')

    # Show the plot
    plt.show()


def save_bankruptcy_data(simulation_dir, simulation_num, SG, total_weight):


    """Append the number of bankruptcies and total weight in a text file."""
    
    filename = os.path.join(simulation_dir, "bankruptcy_data_all_simulations.txt")

    with open(filename, 'a') as txtfile:
        bankruptcies = sum(SG.out_degree(node) > 0 for node in SG.nodes())
        txtfile.write(f"Simulation {simulation_num} : (Nombre de faillites : {bankruptcies}, Poids total : {total_weight})\n")
    return bankruptcies

def plot_graph_2(data):
    """Plot a smooth graph with number of bankruptcies on the x-axis and total_weight on the y-axis."""
    # Unpack the data
    total_weights, bankruptcies = zip(*data)

    # Create an interpolation function
    x = np.array(bankruptcies)
    y = np.array(total_weights)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='')

    # Label the axes
    plt.xlabel('Nombre de faillites')
    plt.ylabel('Poids total')

    # Show the plot
    plt.show()




# def save_detailed_node_data(simulation_dir, simulation_num, SG):
#     """Save detailed node data including the sum of all node weights and each outgoing edge's weight."""
#     filename = os.path.join(simulation_dir, f"detailed_node_data_simulation_{simulation_num}.csv")

#     with open(filename, 'w', newline='') as csvfile:
#         fieldnames = ['node', 'node_weight', 'outgoing_edges', 'sum_out_edge_weights', 'out_edge_weights']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
#         writer.writeheader()
#         for node in SG.nodes():
#             node_weight = SG.nodes[node].get('weight', 0)
#             out_edges = SG.out_edges(node, data=True)
#             sum_out_edge_weights = sum(data['weight'] for _, _, data in out_edges)
#             outgoing_edges = SG.out_degree(node)
#             out_edge_weights = [data['weight'] for _, _, data in out_edges]
#             writer.writerow({
#                 'node': node, 
#                 'node_weight': node_weight, 
#                 'outgoing_edges': outgoing_edges, 
#                 'sum_out_edge_weights': sum_out_edge_weights,
#                 'out_edge_weights': out_edge_weights
#             })


if __name__ == "__main__":
    timestamp = int(time.time())
    simulation_dir = f"simulations/{timestamp}"
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)
    G, filename = choose_graph()
    friends = genereFriends(G)
    random_strat, strat_dict = random_strategies(G, simulation_dir)
    if not random_strat:
        strategy_func = choose_strategy()
    weights_func = choose_weights_strategy()
    total_weight = input_total_weight(G)
    num_simulations, weight_multiplier = input_simulation_parameters()

    save_parameters(simulation_dir, Path(str(filename)).stem, "all_random" if random_strat else strategy_func.__name__, weights_func.__name__, num_simulations, weight_multiplier, total_weight)
    list_of_bankruptcies = []
    for i in range(num_simulations):
        SG = copy.deepcopy(G)
        weights_func(SG, weight_multiplier*i if i > 0 else 1, total_weight)

        edges_removed = True
        while edges_removed:
            edges_removed = False
            accumulated_weights = {}

            for node in SG.nodes():
                if random_strat and strat_dict is not None:
                    strategy_func = strat_dict[node]
                if process_node_edges(SG, node, accumulated_weights, strategy_func):
                    edges_removed = True

            for node, weight in accumulated_weights.items():
                SG.nodes[node]['weight'] += weight

        true_Total_Weight = total_weight * (weight_multiplier * i if i > 0 else 1)
       
        print(f"Simulation {i+1} done.")
        list_of_bankruptcies.append((save_bankruptcy_data(simulation_dir, i+1, SG, true_Total_Weight),true_Total_Weight))
    print("All simulations done.")
    print(list_of_bankruptcies)
    plot_graph_2(list_of_bankruptcies)