import os
import inspect
import src.processing as processing
import src.weights as weights
import networkx as nx
from src.processing import *
from src.weights import *
from src.gen_graph import create_new_graph
from src.graph_utils import load_graph
from src.file_utils import list_graph_files


def get_function_names(module, exclude_function="process_node_edges"):
    functions = inspect.getmembers(module, inspect.isfunction)
    return [func_name for func_name, _ in functions if func_name != exclude_function]

def function_choice(module, display_message, input_message, error_message):
    function_names = get_function_names(module)
    function_map = {name: getattr(module, name) for name in function_names}
    
    print(display_message)
    for name in function_names:
        print(name)

    choice = input(input_message)
    while choice not in function_map:
        print(error_message)
        choice = input(input_message)

    return function_map[choice]

def choose_graph():
    load_or_create = input("Do you want to load a graph (load) or create a new one (create)? ")
    filename = None
    G = nx.MultiDiGraph()
    if load_or_create == 'load':
        print("Available graph files:")
        available_graphs = list_graph_files()
        for file in available_graphs:
            print(file)
        filename = input("Enter the filename of the graph to load: ")
        while filename not in available_graphs:
            print("File not found. Please enter a valid filename.")
            filename = input("Enter the filename of the graph to load: ")
            G = load_graph(os.path.join("graphs", filename))
    elif load_or_create == 'create':
        nb_nodes = int(input("How many nodes should the graph have? "))
        G, filename = create_new_graph(nb_nodes)

    return G, filename


def choose_strategy():
    return function_choice(
        processing,
        "Available strategies:",
        "Choose a strategy: ",
        "Invalid strategy. Please choose a valid strategy.",
    )

def choose_weights_strategy():
    return function_choice(
        weights,
        "Available weights strategies:",
        "Choose a weights strategy: ",
        "Invalid weights strategy. Please choose a valid weights strategy.",
    )

def input_simulation_parameters():
    num_simulations = int(input("How many times should the simulation run? "))
    weight_multiplier = float(input("Enter the weight multiplication factor: "))
    return num_simulations, weight_multiplier


