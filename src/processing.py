import random

def process_node_edges(G, node, accumulated_weights, strategy_func):
    edges_removed = False
    edges = strategy_func(G, node)

    for u, v, data in edges:
        if G.nodes[u]['weight'] > 0 and G.nodes[u]['weight'] > data['weight']:
            G.nodes[u]['weight'] -= data['weight']
            accumulated_weights[v] = accumulated_weights.get(v, 0) + data['weight']
            G.remove_edge(u, v)
            edges_removed = True
        else:
            break
    return edges_removed

def oldest_first(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('date'))

def newest_first(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('date'), reverse=True)

def highest_weight_first(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('weight'), reverse=True)

def lowest_weight_first(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('weight'))

def random_strategy(G, node):
    print("random")
    return random.shuffle(list(G.out_edges(node, data=True))) #pas bon ca 

def genereFriends(G):
    nbNoeuds = G.number_of_nodes()
    AGENTS = list(range(1, nbNoeuds + 1)) 
    list_of_lists = []
    for i in range(1, nbNoeuds + 1):
        Li = []  
        random.shuffle(AGENTS) 
        Li.extend(AGENTS) 
        list_of_lists.append(Li)  
    return list_of_lists

def calculDeficit(G):
    deficits = {}  
    in_edges_sum = {node: sum(data['weight'] for _, _, data in G.in_edges(node, data=True)) for node in G.nodes()}
    out_edges_sum = {node: sum(data['weight'] for _, _, data in G.out_edges(node, data=True)) for node in G.nodes()}
    for node in G.nodes():
        capital = 0 
        deficit = in_edges_sum.get(node, 0) + capital - out_edges_sum.get(node, 0)
        deficits[node] = deficit
    return deficits

def detteMoyenne(G):
    average_debts = {} 
    for node in G.nodes():
        out_edges = list(G.out_edges(node, data=True))
        if out_edges:
            out_edges_sum = sum(data['weight'] for _, _, data in out_edges)
            num_out_edges = len(out_edges)
            average_debt = out_edges_sum / num_out_edges
            average_debts[node] = average_debt
        else:
            average_debts[node] = None
    return average_debts

def nbDettes(G):
    outgoing_edges_count = {}
    for node in G.nodes():
        outgoing_edges_count[node] = G.out_degree(node)
    return outgoing_edges_count

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

# TODO : add more strategies