import os
import inspect
import random
import json
import processing as processing
import weights as weights
import networkx as nx
from processing import *
from weights import *
from gen_graph import create_new_graph
from graph_utils import load_graph
from file_utils import list_graph_files

def get_function_names(module, exclude_function=None):
    if exclude_function is None:
        exclude_function = ["process_node_edges","load_config"]
    functions = inspect.getmembers(module, inspect.isfunction)
    return [func_name for func_name, _ in functions if func_name not in exclude_function]

def function_choice(module, display_message, input_message, error_message):
    function_names = get_function_names(module)
    function_map = {name: getattr(module, name) for name in function_names}
    
    print(display_message)
    numbered_options = {str(i+1): name for i, name in enumerate(function_names)}
    for number, name in numbered_options.items():
        print(f"{number}. {name}")

    choice = input(input_message)
    while choice not in numbered_options:
        print(error_message)
        choice = input(input_message)

    # Use the selected number to get the function name, then get the function from the map
    selected_function_name = numbered_options[choice]
    return function_map[selected_function_name]

def choose_graph():
    load_or_create = input("Do you want to load a graph (load) or create a new one (create)? ")
    filename = None
    G = nx.MultiDiGraph()
    if load_or_create.lower() == 'load':
        print("Available graph files:")
        available_graphs = list_graph_files()
        for index, file in enumerate(available_graphs, start=1):
            print(f"{index}. {file}")
        
        choice = input("Enter the number of the graph to load: ")
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(available_graphs):
            print("Invalid selection. Please enter a valid number.")
            choice = input("Enter the number of the graph to load: ")
        filename = available_graphs[int(choice)-1]
        G = load_graph(os.path.join("graphs", filename))
    elif load_or_create.lower() == 'create':
        G, filename = create_new_graph()

    return G, filename

def choose_strategy():
    return function_choice(
        processing,
        "Available strategies:",
        "Choose a strategy by number: ",
        "Invalid strategy. Please choose a valid strategy by number.",
    )

def choose_weights_strategy():
    return function_choice(
        weights,
        "Available weights strategies:",
        "Choose a weights strategy by number: ",
        "Invalid weights strategy. Please choose a valid weights strategy by number.",
    )

def input_simulation_parameters():
    num_simulations = int(input("How many times should the simulation run? "))
    weight_multiplier = float(input("Enter the weight multiplication factor: "))
    return num_simulations, weight_multiplier


def input_total_weight(G):
    total_weight = int(input("Enter the total weight: "))
    while total_weight < G.number_of_nodes():
        print("The total weight must be greater than or equal to the number of nodes.")
        total_weight = int(input("Enter the total weight: "))
    return total_weight

def random_strategies(G, simulation_dir):
    if (
        random_strategies := input(
            "Do you want random strategies for the graph? (yes/no): "
        )
        .lower()
        .startswith('y')
    ):
        strats_list = get_function_names(processing)
        strat_dict = {node: random.choice(strats_list) for node in G.nodes()}
        with open(f"{simulation_dir}/strategies.json", 'w') as f:
            json.dump(strat_dict, f)
        return random_strategies, strat_dict
    else:
        return random_strategies, None
