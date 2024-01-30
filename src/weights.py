import random
import json

def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

config = load_config("config.json")

def random_weights(G, multiplier):
    """
    Ajoute un poids aléatoire à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    min_weight (int): Le poids minimum possible.
    max_weight (int): Le poids maximum possible.
    """
    min_weight = config['weights_strategies'][0]['parameters']['min_weight']
    max_weight = config['weights_strategies'][0]['parameters']['max_weight']
    for node in G.nodes():
        G.nodes[node]['weight'] = random.randint(min_weight, max_weight) * multiplier

def same_weight(G, multiplier):
    """
    Ajoute un poids identique à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    weight (int): Le poids à ajouter.
    """
    weight = config['weights_strategies'][1]['parameters']['weight']
    for node in G.nodes():
        G.nodes[node]['weight'] = weight * multiplier



# TODO : add more strategies