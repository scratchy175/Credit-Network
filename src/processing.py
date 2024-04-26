import random
import pickle

import networkx as nx
import matplotlib.pyplot as plt

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



def debt_runner(G, node):

  
    # dessin du graphe 
    #with open("./graphs/graph_n5_e21_20240129_091000.gpickle", "rb") as f:
        #G = pickle.load(f)

        # Dessiner le graphe
        #pos = nx.spring_layout(G)  # Calculer les positions des noeuds pour une belle visualisation
        #nx.draw(G, pos, with_labels=True)

        # Dessiner les poids des arcs
        #edge_labels = nx.get_edge_attributes(G, 'weight')
        #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Dessiner le graphe
        #plt.show()

        
    # Initialisation des variables
    montantTotal = 0
    aPayer = []
    Liste_dette = []

    # Trier les noeuds selon le nombre de dettes décroissant
    prio = sorted(G.successors(node), key=lambda x: G.out_degree(x), reverse=True)
    print(prio)
   

    # Parcourir la liste triée
    for x in prio:
        if x in G.successors(node) :
            pass    
           

    # Mettre à jour le capital de l'agent node
    "G.nodes[node]['weight'] -= montantTotal"

    # Ajouter les dettes à payer de l'agent node au résultat
    return aPayer





















def back_to_the_richest(G):
    result = {}
    for x in G.nodes():
        # Initialisation des variables
        montantTotal = 0
        aPayer = []

        # Trier les noeuds selon le montant total des dettes croissant
        prio = sorted(G.nodes(), key=lambda node: G.nodes[node]['mtDettes'])

        # Parcourir la liste triée
        for node in prio:
            if node in G.nodes[x]:  # Vérifier si l'agent x doit de l'argent à l'agent node
                dette = G[x][node]['montant']  # Obtenir le montant de la dette
                if montantTotal + dette < G.nodes[x]['capital']:
                    montantTotal += dette
                    aPayer.append((node, dette))  # Ajouter à la liste des dettes à payer
                    G.remove_edge(x, node)  # Retirer la dette du graphe

        # Mettre à jour le capital de l'agent x
        G.nodes[x]['capital'] -= montantTotal

        # Ajouter les dettes à payer de l'agent x au résultat
        result[x] = aPayer

    return result
