import os
from datetime import datetime
import pickle

def save_graph(G):
    """
    Sauvegarde un graphe dans un fichier.

    Args:
    G (networkx.Graph): Le graphe à sauvegarder.
    """
    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"graphs/graph_n{num_nodes}_e{num_edges}_{current_time}.gpickle"

    with open(filename, 'wb') as f:
        pickle.dump(G, f)

    print("Graphe sauvegardé dans : ", filename)

def load_graph(filename):
    """
    Charge un graphe à partir d'un fichier.

    Args:
    filename (str): Le nom du fichier à partir duquel charger le graphe.

    Returns:
    networkx.Graph: Le graphe chargé.
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            G = pickle.load(f)
        print(f"Graphe chargé à partir de : {filename}")
        return G
    else:
        print(f"Aucun fichier trouvé à : {filename}")
        exit(1)

