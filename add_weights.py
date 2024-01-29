import random

def add_random_weights(G, min_weight, max_weight):
    """
    Ajoute un poids aléatoire à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    min_weight (int): Le poids minimum possible.
    max_weight (int): Le poids maximum possible.
    """
    for node in G.nodes():
        G.nodes[node]['weight'] = random.randint(min_weight, max_weight)


# TODO : add more strategies