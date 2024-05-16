import os
from processing import process_node_edges
from file_utils import save_parameters
from input_utils import *
import copy
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from processing import beginningCapital
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv

from process_algo import calculDeficit, detteMoyenne, generate_friends_for_each_node

def manage_pre_algo(filename):
    with open(filename, 'rb') as f:
        G = pickle.load(f)
    print(f"Graphe chargé à partir de : {filename}")
    # Check for related files
    graph_name = os.path.splitext(filename)[0]
    related_files = [f'{graph_name}_genereFriends.pickle', f'{graph_name}_calculDeficit.pickle', f'{graph_name}_calculDetteMoyenne.pickle']
    for related_file in related_files:
        if os.path.exists(related_file):
                with open(related_file, 'rb') as f:
                    processing.friends = pickle.load(f)
            
        else:
            print(f"No related file found for {related_file}.")
            processing.friends = generate_friends_for_each_node(G)
            with open(related_file, 'wb') as f:
                pickle.dump(processing.friends, f)
            
    return G


def save_bankruptcy_data(simulation_dir, simulation_num, SG, total_weight):
    """Append the number of bankruptcies and total weight in a CSV file."""
    
    filename = os.path.join(simulation_dir, "bankruptcy_data_all_simulations.csv")
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Simulation', 'Nombre de faillites', 'Poids total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header only if the file does not exist
        if not file_exists:
            writer.writeheader()
        
        bankruptcies = sum(SG.out_degree(node) > 0 for node in SG.nodes())
        writer.writerow({'Simulation': simulation_num, 'Nombre de faillites': bankruptcies, 'Poids total': total_weight})
    
    return bankruptcies

def plot_graph_(data, simulation_dir):
    """Plot a graph with number of bankruptcies on the x-axis and total_weight on the y-axis."""
    # Unpack the data
    total_weights, bankruptcies = zip(*data)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(bankruptcies, total_weights)

    # Label the axes
    plt.xlabel('Somme totale')
    plt.ylabel('Nombre de faillites')

    plt.ylim((0, 11000))

    # Save the plot
    plt.savefig(f"{simulation_dir}/plot.png")
    plt.close()


def setup_simulation():
    strategy_func = strategy_var.get()
    weights_func = weights_var.get()

    selection = graph_var.get()
    filename = selection
    G = load_graph(os.path.join("graphs", filename))
    # These functions are now selected from the combo boxes instead of via command line
    strategy_function = getattr(processing, strategy_func)
    weights_function = getattr(weights, weights_func)

    run_simulation(G, filename, strategy_function, weights_function)


def run_simulation(G, filename, strategy_func, weights_func):
    
        # Get inputs from GUI
        num_simulations = int(num_simulations_entry.get())
        weight_multiplier = float(weight_multiplier_entry.get())
        total_weight = float(total_weight_entry.get())
        timestamp = int(time.time())
        # Formatted directory name using graph name and strategy names
        graph_name = Path(filename).stem.split("_")
        strategies_name = f"{strategy_func.__name__}_{weights_func.__name__}"
        simulation_dir = f"simulations/{graph_name[0]}_{graph_name[3]}_{strategies_name}"
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)
        save_parameters(simulation_dir, Path(str(filename)).stem, strategy_func.__name__, weights_func.__name__, num_simulations, weight_multiplier, total_weight)

        list_of_bankruptcies = []
        if strategy_func.__name__ == "powerOfFriendship":
            manage_pre_algo(os.path.join("graphs", filename))
        progress_bar['maximum'] = num_simulations
        for i in range(num_simulations):
            SG = copy.deepcopy(G)

            # Distribution de l'argent
            weights_func(SG, total_weight)
            edges_removed = True
            for node in SG.nodes(data=True):
                beginningCapital[node[0]] = node[1]['weight']
            processing.capital = calculDeficit(SG)
            processing.detteMoy = detteMoyenne(SG)
            # for edge in SG.out_edges(data = True):
            #     print(edge)

            # Traitement des dettes
            # Tant que des dettes sont remboursées, on continue
            # un tour de boucle = un paiement de dettes = 1 top
            while edges_removed:
                edges_removed = False
                accumulated_weights = {}

                # On traite les dettes de chaque noeud
                for node in SG.nodes():
                    if process_node_edges(SG, node, accumulated_weights, strategy_func):
                        edges_removed = True

                # On ajoute les montants remboursés aux noeuds
                for node, weight in accumulated_weights.items():
                    SG.nodes[node]['weight'] += weight
            
            progress_bar['value'] = i + 1
            root.update_idletasks()
            beginningCapital.clear()
            print(f"Simulation {i+1} terminée.")
            list_of_bankruptcies.append((save_bankruptcy_data(simulation_dir, i+1, SG, total_weight),total_weight))
            total_weight = total_weight * weight_multiplier
        print("Toutes les simulations sont terminées.")
        print(list_of_bankruptcies)
        plot_graph_(list_of_bankruptcies, simulation_dir)
        messagebox.showinfo("Simulation terminées", f"Les résultats des simulations ont été enregistrés dans le dossier {simulation_dir}.")
    



if __name__ == "__main__":
    

    # Main window setup
    root = tk.Tk()
    root.title("Configuration de la simulation")

    # Widgets for inputs
    tk.Label(root, text="Nombre de simulations:").grid(row=0, column=0)
    num_simulations_entry = tk.Entry(root)
    num_simulations_entry.insert(0, "20")  # Default value set here
    num_simulations_entry.grid(row=0, column=1)

    tk.Label(root, text="Multiplicateur:").grid(row=1, column=0)
    weight_multiplier_entry = tk.Entry(root)
    weight_multiplier_entry.insert(0, "1.5")  # Default value set here
    weight_multiplier_entry.grid(row=1, column=1)

    tk.Label(root, text="Somme totale:").grid(row=2, column=0)
    total_weight_entry = tk.Entry(root)
    # il faudrait que la somme totale soit égale à la somme des poids des arêtes ou des noeuds ? ou une partie
    total_weight_entry.insert(0, "50000000")  # Default value set here
    total_weight_entry.grid(row=2, column=1)

    # Graph selection setup
    graph_options = list_graph_files()
    graph_var = ttk.Combobox(root, values=graph_options)
    graph_var.grid(row=3, column=1)
    tk.Label(root, text="Graphe:").grid(row=3, column=0)


    # Strategy selection
    strategy_var = ttk.Combobox(root, values=get_function_names(processing))
    strategy_var.grid(row=4, column=1)
    tk.Label(root, text="Stratégie de paiement:").grid(row=4, column=0)

    # Weights strategy selection
    weights_var = ttk.Combobox(root, values=get_function_names(weights))
    weights_var.grid(row=5, column=1)
    tk.Label(root, text="Stratégie de prêt:").grid(row=5, column=0)


    # Progress Bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.grid(row=6, columnspan=2, pady=10)

    # Run button
    run_button = tk.Button(root, text="Lancer la simulation", command=setup_simulation)
    run_button.grid(row=7, columnspan=2)

    # Start the GUI event loop
    root.mainloop()