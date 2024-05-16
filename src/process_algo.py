import random
import pickle
from random import shuffle


def generate_friends_for_each_node(G):
    """
    Generates a randomized list of friends for each node in the graph.
    This assumes that all nodes can potentially be friends with any other node.
    Excludes the node itself from its list of friends.
    
    Parameters:
    - G: The graph object

    Returns:
    A dictionary where keys are nodes and values are lists of friends (other nodes).
    """
    friends_dict = {}
    nodes_list = list(G.nodes())
    
    for node in nodes_list:
        # Create a copy of the node list and remove the current node to avoid self-friendship
        possible_friends = nodes_list.copy()
        possible_friends.remove(node)
        
        # Shuffle the list to randomize friend connections
        random.shuffle(possible_friends)
        
        # You can also limit the number of friends each node can have by slicing the list
        # For example, `[:10]` would give each node 10 friends at most
        friends_dict[node] = possible_friends

    return friends_dict


def calculDeficit(G):
    deficits = {}
    in_edges_sum = {node: sum(data['weight'] for _, _, data in G.in_edges(node, data=True)) for node in G.nodes()}
    out_edges_sum = {node: sum(data['weight'] for _, _, data in G.out_edges(node, data=True)) for node in G.nodes()}
    for node in G.nodes():
        capital = G.nodes[node]['weight']
        deficit = in_edges_sum.get(node, 0) + capital - out_edges_sum.get(node, 0)
        deficits[node] = deficit
    return deficits



def detteMoyenne(G):
    average_debts = {}
    for node in G.nodes():
        if out_edges := list(G.out_edges(node, data=True)):
            out_edges_sum = sum(data['weight'] for _, _, data in out_edges)
            num_out_edges = len(out_edges)
            average_debt = out_edges_sum / num_out_edges
            average_debts[node] = average_debt
        else:
            average_debts[node] = None
    return average_debts

def nbDettes(G):
    return {node: G.out_degree(node) for node in G.nodes()}

def trierDecroissant(G):
    return sorted(nbDettes(G).items(), key=lambda x: x[1], reverse=True)

def sommeDettes(G):
    outgoing_weights = {}
    for node in G.nodes():
        out_edges = list(G.out_edges(node, data=True))
        if out_edges:
            out_edges_sum = sum(data['weight'] for _, _, data in out_edges)
            outgoing_weights[node] = out_edges_sum
        else:
            outgoing_weights[node] = 0
    return outgoing_weights



def poidTotal(G):
    total_weight = sum(data['weight'] for _, _, data in G.edges(data=True))
    return total_weight

def porportionMontantDettes(G):
    dettes_totales = {}
    total_poids = poidTotal(G)
    dettes_noeuds = sommeDettes(G)
    for node in G.nodes():
        dettes_totales[node] = {}
        if node in dettes_noeuds:
            total_sortant = dettes_noeuds[node]
            for agent, poids_sortant in dettes_noeuds[node].items():
                proportion = poids_sortant / total_poids
                dettes_totales[node][agent] = proportion        
    return dettes_totales

def proportionNbDettes(G):
    proportions = {}
    total_edges = G.number_of_edges()
    nb_arcs_sortants = nbDettes(G)
    for node in G.nodes():
        proportions[node] = nb_arcs_sortants[node] / total_edges if total_edges > 0 else 0
    return proportions

def sommePoidsEntrants(G):
    incoming_weights = {}
    for node in G.nodes():
        in_edges = list(G.in_edges(node, data=True))
        if in_edges:
            in_edges_sum = sum(data['weight'] for _, _, data in in_edges)
            incoming_weights[node] = in_edges_sum
        else:
            incoming_weights[node] = 0
    return incoming_weights

def calculDeficitPur(G):
    incoming_weights = sommePoidsEntrants(G)  
    outgoing_weights = sommeDettes(G)  
    difference_weights = {}
    for node in G.nodes():
        difference_weights[node] = incoming_weights[node] - outgoing_weights[node]
    return difference_weights

def definitionPayeurs(G):
    random_assignment = {1:[], 2:[], 3:[], 4:[], 5:[]}
    for node in G.nodes():
        random_key = random.randint(1, 5)
        random_assignment[random_key].append(node)
    return random_assignment