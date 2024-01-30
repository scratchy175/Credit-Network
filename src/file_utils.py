import os
import json

def list_graph_files():
    directory = "graphs"
    # List all files in the specified directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return [f for f in files if f.endswith('.gpickle')]  # Assuming graph files end with '.pkl'


def save_parameters(filename, strategy_choice, weights_choice, num_simulations, weight_multiplier):
    parameters = {
        "strategy_choice": strategy_choice,
        "weights_choice": weights_choice,
        "num_simulations": num_simulations,
        "weight_multiplier": weight_multiplier
    }
    with open(filename, 'w') as f:
        json.dump(parameters, f)
