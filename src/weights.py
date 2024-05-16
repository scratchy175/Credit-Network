import random


def equalizer(G, tot_weight):
    """
    Ajoute un poids identique à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    weight (int): Le poids à ajouter.
    """
    # Calculate the number of nodes in the graph
    num_nodes = G.number_of_nodes()

    # Calculate the weight each node should receive
    weight_per_node = tot_weight / num_nodes if num_nodes > 0 else 0

    # Distribute the weight among the nodes
    for node in G.nodes():
        G.nodes[node]['weight'] = weight_per_node


def goodmanShow(G, tot_weight):
    """
    Applique la stratégie de The Goodman Show sur un MultiDiGraph G où chaque
    arête représente une dette d'un agent vers un autre.
    
    :param G: MultiDiGraph - Le graphe des dettes où les nœuds sont les agents
              et les arêtes contiennent les attributs des dettes.
    :param total_sum: int ou float - La somme totale que la banque peut prêter.
    """
    # Calculer la dette totale 
    # il existe peut etre deja un algo qui fait ca 
    dette_totale = sum(data['weight'] for node in G.nodes() for _, _, data in G.edges(node, data=True))
    
    # Calculer la contribution de chaque agent à la dette totale et ajuster leurs capitaux
    for node in G.nodes():
        dette_agent = sum(data['weight'] for _, _, data in G.edges(node, data=True))
        percentage_of_total = (dette_agent / dette_totale) if dette_totale > 0 else 0
        G.nodes[node]['weight'] = tot_weight * percentage_of_total


def goodmanShowV2(G, tot_weight):
    """
    Applique la version V2 de The Goodman Show sur un MultiDiGraph G où chaque
    arête représente une dette et le focus est mis sur le nombre de dettes.
    
    :param G: MultiDiGraph - Le graphe des dettes où les nœuds sont les agents
              et les arêtes indiquent les dettes.
    :param total_sum: int ou float - La somme totale que la banque peut prêter.
    
    :return: dict - Un dictionnaire avec les capitaux ajustés des agents.
    """
    # Compter le nombre total de dettes
    nombre_total_dettes = sum(G.out_degree(node) for node in G.nodes())
    # Calculer la contribution de chaque agent au nombre total de dettes et ajuster leurs capitaux
    for node in G.nodes():
        nombre_dettes_agent = G.out_degree(node)
        percentage_of_total = (nombre_dettes_agent / nombre_total_dettes) if nombre_total_dettes > 0 else 0
        G.nodes[node]['weight'] = tot_weight * percentage_of_total


def divergent(G, tot_weight):
    """
    Applique la méthode de prêt "Divergent" sur un graphe G où chaque nœud contient le capital de l'agent à zéro initialement.
    Le graphe utilise les arêtes pour représenter les transactions (déficits et gains).

    :param G: NetworkX DiGraph - Le graphe où les nœuds représentent les agents
               et les arêtes indiquent les montants des créances et dettes.
    :param initial_amount: int - Le montant total disponible pour équilibrer les déficits.

    :return: None - Modifie directement les capitaux dans le graphe.
    """
    # Calcul des déficits pour chaque agent
    deficits = {node: 0 for node in G.nodes()}
    for node in G.nodes():
        dettes = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
        creances = sum(data['weight'] for _, _, data in G.in_edges(node, data=True))
        deficit = creances - dettes
        deficits[node] = deficit
    # Couvrir les déficits si négatifs
    for node, deficit in deficits.items():
        if deficit < 0 and abs(deficit) < tot_weight:
            amount_needed = abs(deficit)
            G.nodes[node]['weight'] = G.nodes[node].get('weight', 0) + amount_needed
            tot_weight -= amount_needed

    # Redistribuer le montant restant équitablement si de l'argent reste
    if tot_weight > 0:
        number_of_agents = len(G.nodes())
        equal_share = tot_weight / number_of_agents
        for node in G.nodes():
            G.nodes[node]['weight'] = G.nodes[node].get('weight', 0) + equal_share


def theGodpayer(G, tot_weight):
    """
    Applique l'algorithme 'The GodPayer' sur un graphe G et la liste des capitaux des agents.
    
    :param G: NetworkX DiGraph - Le graphe où chaque nœud représente un agent et les arêtes représentent les créances et dettes.
    :param cap: list - Liste des capitaux initiaux des agents.
    
    :return: tuple - Tuple contenant la liste des capitaux ajustés et le dictionnaire des catégories.
    """
    random.seed(42)
    # Calculer les déficits de chaque agent
    deficits = {}
    for node in G.nodes():
        dettes = sum(data['weight'] for _, _, data in G.out_edges(node, data=True))
        creances = sum(data['weight'] for _, _, data in G.in_edges(node, data=True))
        deficits[node] = creances - dettes
    
    # Trier les agents selon leur déficit croissant
    # Moi j'aurais pas trier ca 
    sorted_deficits = sorted(deficits.items(), key=lambda x: x[1])
    # Catégorisation aléatoire des agents
    categories = {1: [], 2: [], 3: [], 4: [], 5: []}
    for tuple in sorted_deficits:
        categorie = random.randint(1, 5)
        categories[categorie].append(tuple)
    for i in range(1, 4):
        for agent in categories[i]:
            if tot_weight <= 0:
                break
            if abs(agent[1]) < tot_weight and agent[1] < 0:
                aPreter = abs(agent[1])
                G.nodes[node]['weight'] = aPreter
                print(f"Prêt de {aPreter} à l'agent {agent[0]}")
                tot_weight -= aPreter
    # Distribution du reste du budget si disponible
    if tot_weight > 0 and len(categories[1]) > 0:
        for agent in categories[1]:
            G.nodes[agent[0]]['weight'] = G.nodes[agent[0]].get('weight', 0) + tot_weight / len(categories[1])
    