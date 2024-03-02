import os
import json

def list_graph_files():
    directory = "graphs"
    # List all files in the specified directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return [f for f in files if f.endswith('.gpickle')]


def save_parameters(simulation_dir, graph_filename, strategy_choice, weights_choice, num_simulations, weight_multiplier, total_weight):
    parameters = {
        "filename": graph_filename,
        "strategy_choice": strategy_choice,
        "weights_choice": weights_choice,
        "num_simulations": num_simulations,
        "weight_multiplier": weight_multiplier,
        "total_weight": total_weight
    }
    with open(f"{simulation_dir}/parameters.json", 'w') as f:
        json.dump(parameters, f)
