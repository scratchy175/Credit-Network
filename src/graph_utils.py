import os
import pickle

def save_graph(G, filename):
    """
    Sauvegarde un graphe dans un fichier.

    Args:
    G (networkx.Graph): Le graphe à sauvegarder.
    """
    with open(filename, 'wb') as f:
        pickle.dump(G, f)



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

