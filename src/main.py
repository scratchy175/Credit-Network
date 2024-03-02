import os
from processing import process_node_edges
from graph_utils import save_graph
from file_utils import save_parameters
from disp_graph import save_png
from input_utils import *
import copy
import time
import csv
from pathlib import Path


def save_detailed_node_data(simulation_dir, simulation_num, SG):
    """Save detailed node data including the sum of all node weights and each outgoing edge's weight."""
    filename = os.path.join(simulation_dir, f"detailed_node_data_simulation_{simulation_num}.csv")

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['node', 'node_weight', 'outgoing_edges', 'sum_out_edge_weights', 'out_edge_weights']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for node in SG.nodes():
            node_weight = SG.nodes[node].get('weight', 0)
            out_edges = SG.out_edges(node, data=True)
            sum_out_edge_weights = sum(data['weight'] for _, _, data in out_edges)
            outgoing_edges = SG.out_degree(node)
            out_edge_weights = [data['weight'] for _, _, data in out_edges]
            writer.writerow({
                'node': node, 
                'node_weight': node_weight, 
                'outgoing_edges': outgoing_edges, 
                'sum_out_edge_weights': sum_out_edge_weights,
                'out_edge_weights': out_edge_weights
            })


if __name__ == "__main__":
    timestamp = int(time.time())
    simulation_dir = f"simulations/{timestamp}"
    if not os.path.exists(simulation_dir):
        os.makedirs(simulation_dir)
    G, filename = choose_graph()
    random_strat, strat_dict = random_strategies(G, simulation_dir)
    if not random_strat:
        strategy_func = choose_strategy()
    weights_func = choose_weights_strategy()
    total_weight = input_total_weight(G)
    num_simulations, weight_multiplier = input_simulation_parameters()
    save_graphs = input("Do you want to save the simulation graphs? (yes/no): ").lower().startswith('y')
    save_images =  input("Do you want to save the simulation images? (yes/no): ").lower().startswith('y')

    save_parameters(simulation_dir, Path(str(filename)).stem, "all_random" if random_strat else strategy_func.__name__, weights_func.__name__, num_simulations, weight_multiplier, total_weight)


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
        
        if save_graphs:
            os.mkdir(f"simulations/{timestamp}/graphs")
            save_graph(SG,f"simulations/{timestamp}/graphs/simulation_{i+1}.gpickle")
        if save_images:
            os.mkdir(f"simulations/{timestamp}/images")
            save_png(SG, f"simulations/{timestamp}/images/simulation_{i+1}.png")
        save_detailed_node_data(simulation_dir, i+1, SG)
        print(f"Simulation {i+1} done.")
    print("All simulations done.")

