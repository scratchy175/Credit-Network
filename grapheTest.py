from src.graph_utils import *

G = load_graph("graphs/ER_p2.0_n100_e9900_20240427_231418.gpickle")

import networkx as nx
import random

def the_godpayer_algorithm(G, budget):
    """
    Applique l'algorithme 'The GodPayer' sur un graphe G et la liste des capitaux des agents.
    
    :param G: NetworkX DiGraph - Le graphe où chaque nœud représente un agent et les arêtes représentent les créances et dettes.
    :param cap: list - Liste des capitaux initiaux des agents.
    
    :return: tuple - Tuple contenant la liste des capitaux ajustés et le dictionnaire des catégories.
    """
    # Calculer les déficits de chaque agent
    deficits = {}
    for node in G.nodes():
        creances = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
        dettes = sum(data['weight'] for _, _, data in G.in_edges(node, data=True))
        deficits[node] = creances - dettes
    
    # Trier les agents selon leur déficit croissant
    # Moi j'aurais pas trier ca 
    sorted_deficits = sorted(deficits.items(), key=lambda x: x[1])
    # Catégorisation aléatoire des agents
    categories = {1: [], 2: [], 3: [], 4: [], 5: []}
    for tuple in sorted_deficits:
        categorie = random.randint(1, 5)
        categories[categorie].append(tuple)
    for i in range(1, 6):
        for agent in categories[i]:
            if budget <= 0:
                break
            if abs(agent[1]) < budget and agent[1] < 0:
                aPreter = abs(agent[1])
                G.nodes[node]['weight'] = aPreter
                print(f"Prêt de {aPreter} à l'agent {agent[0]}")
                budget -= aPreter
    # Distribution du reste du budget si disponible
    if budget > 0 and len(categories[1]) > 0:
        for agent in categories[1]:
            G.nodes[agent[0]]['weight'] = G.nodes[agent[0]].get('weight', 0) + budget / len(categories[1])
    
    return categories


"""# Exemple d'utilisation
G = nx.DiGraph()
# Ajouter des nœuds et des arêtes (les agents et leurs transactions)
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_edge(1, 2, weight=300)  # Agent 1 doit 300 à Agent 2
G.add_edge(2, 3, weight=200)  # Agent 2 doit 200 à Agent 3
G.add_edge(3, 1, weight=150)  # Agent 3 doit 150 à Agent 1"""

budget = 500000  # Budget total disponible pour prêter
categories = the_godpayer_algorithm(G, budget)
#print("Categories:", categories)

# Afficher les capitaux ajustés des agents
for node in G.nodes():
    #print(f"Agent {node}: {G.nodes[node].get('weight', 0)}")
    pass

# Afficher les capitaux des agents de la catégorie 1
print("Catégorie 1:")
for agent in categories[1]:
    #print(f"Agent {agent[0]}: {agent[1]}")
    pass
