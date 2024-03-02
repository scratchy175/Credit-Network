import random

#a tester 
def random_weights(G, multiplier, tot_weight):
    """
    Ajoute un poids aléatoire à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    min_weight (int): Le poids minimum possible.
    max_weight (int): Le poids maximum possible.
    """
    total_weight:int = tot_weight * multiplier

    # Calculate the number of nodes in the graph
    num_nodes = G.number_of_nodes()

    # Ensure the total_weight is distributed among the nodes
    # Generate a list of random weights that sum up to total_weight
    weights = [random.random() for _ in range(num_nodes)]
    total_random_weight = sum(weights)
    normalized_weights = [weight / total_random_weight * total_weight for weight in weights]

    # Distribute the weights among the nodes
    for node, weight in zip(G.nodes(), normalized_weights):
        G.nodes[node]['weight'] = weight


# que faire si la division n'est pas exacte ? que faire de l'argent qui reste ?
def same_weight(G, multiplier, tot_weight):
    """
    Ajoute un poids identique à chaque noeud du graphe G.

    Parameters:
    G (NetworkX graph): Le graphe à modifier.
    weight (int): Le poids à ajouter.
    """
    total_weight:int = tot_weight * multiplier
    # Calculate the number of nodes in the graph
    num_nodes = G.number_of_nodes()

    # Calculate the weight each node should receive
    weight_per_node = total_weight / num_nodes if num_nodes > 0 else 0

    # Distribute the weight among the nodes
    for node in G.nodes():
        G.nodes[node]['weight'] = int(weight_per_node)



# TODO : add more strategies here