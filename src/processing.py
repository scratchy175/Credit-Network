import random
import pickle

import networkx as nx
import matplotlib.pyplot as plt
from process_algo import *
global beginningCapital
beginningCapital = {}

global friends
friends = []

"""
Permet de traiter(payer les dettes) un noeud selon une stratégie donnée
:param G: le graphe
:param node: le noeud à traiter
:param accumulated_weights: les poids accumulés
:param strategy_func: liste/ordre des arêtes à traiter pour le noeud donné selon une stratégie donnée

:return: False si aucun paiement n'a été effectué durant le tour, True sinon
"""
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


def bankBuster (G,node):
    # print('Traitement du noeud : ',node)
    aPayer = []
    capitalv2 = []
    # print('capital : ',capital)
    for ele in G.successors(node):
        # print(node, ele)
        for tup in beginningCapital:
            if tup[0] == ele:
                capitalv2.append(tup)
    sortedCapital = sorted(capitalv2, key=lambda x: x[1], reverse=True)
    # print("capitalv2 : ", capitalv2)
    # print("sortedCapital : ",sortedCapital, node)
    for elt in sortedCapital:
        for edge in G.out_edges(node,data=True):
            # print(edge ,node, "arrete", elt)
            if edge[1] == elt[0]:
                # print(edge , node, "arrete validée")
                aPayer.append(edge)

    # Afficher les arêtes trouvées
    return aPayer

# def bankWars (G,node):
#     # print('Traitement du noeud : ',node)
#     aPayer = []
#     capital = beginningCapital.copy()
#     capitalv2 = []
#     # print('capital : ',capital)
#     for ele in G.successors(node):
#         # print(node, ele)
#         for tup in capital:
#             if tup[0] == ele:
#                 capitalv2.append(tup)
#     sortedCapital = sorted(capitalv2, key=lambda x: x[1])
#     # print("capitalv2 : ", capitalv2)
#     # print("sortedCapital : ",sortedCapital)
#     for elt in sortedCapital:
#         for edge in G.out_edges(node,data=True):
#             if edge[1] == elt[0]:
#                 aPayer.append(edge)

#     # Afficher les arêtes trouvées
#     return aPayer  

def bankBuster(G, node):
    # Créer un ensemble des successeurs du nœud
    successors = set(G.successors(node))

    # Trier les successeurs selon le capital initial reçu de la banque
    sorted_successors = sorted(successors, key=lambda x: beginningCapital.get(x, 0), reverse=True)

    # Utiliser un générateur pour parcourir les arêtes sortantes du nœud
    outgoing_edges = (edge for edge in G.out_edges(node, data=True) if edge[1] in successors)

    # Filtrer les arêtes sortantes en fonction des successeurs triés
    aPayer = [edge for edge in outgoing_edges if edge[1] in sorted_successors]

    return aPayer

def Mister_big_heart(G,node):
    aPayer = []
    créanciers = []
    capitalPrevisionnel = calculDeficit(G)
    for elt in G.successors(node):
        for key in capitalPrevisionnel.keys():
            if elt == key:
                créanciers.append((key,capitalPrevisionnel[key]))
    créanciers = sorted(créanciers, key=lambda x: x[1], reverse=True)
    for elt in créanciers:
        for edge in G.out_edges(node,data=True):
            if edge[1] == elt[0]:
                aPayer.append(edge)
    print(aPayer)
    return aPayer

def debt_runner(G, node):

   # Print the type of the successors to verify it's an iterable
    print(type(G.successors(node)))
    print(list(G.successors(node)))
    # Initialisation des variables
    aPayer = []
    # Trier les noeuds selon le nombre de dettes décroissant
    prio = sorted(G.successors(node), key=lambda x: G.out_degree(x), reverse=True)

    for creancier in prio:
        for edge in G.out_edges(node,data=True):
            if edge[1] == creancier:
                aPayer.append(edge)


    return aPayer

def The_Average_Joe(G, node):
    aPayer = []
    créanciers = []
    CapitalPrevisionnel = detteMoyenne(G)
    
    
    for elt in G.successors(node):
        for key in CapitalPrevisionnel.keys():
            if elt == key:
                créanciers.append((key, CapitalPrevisionnel[key]))
               # print(f"Ajout du créancier {key} avec une dette moyenne de {CapitalPrevisionnel[key]}")
    
    créanciers = sorted(créanciers, key=lambda x: x[1] if x[1] is not None else float('-inf'), reverse=True)
    
    for elt in créanciers:
        for edge in G.out_edges(node, data=True):
            if edge[1] == elt[0]:
                aPayer.append(edge)
                #print(f"Ajout de paiement: {node} paie {edge[1]} avec les détails {edge[2]}")
    
    print("Paiements à effectuer:", aPayer)
    return aPayer

def back_to_the_richest(G, node):
    #print('Traitement du noeud : ',node)
    # Initialisation de la liste des paiements
    aPayer = []
    creanciers = []
    capital = calculDeficit(G)

    for el in G.successors(node):
        for keys in capital.keys():
            if el ==keys :
                creanciers.append((keys,capital[keys]))

        creanciers = sorted(creanciers, key=lambda x: x[1])
    for elt in creanciers:
        aPayer.extend(
            edge for edge in G.out_edges(node, data=True) if edge[1] == elt[0]
        )
    #print(aPayer)
    return aPayer


def heivyweightv2(G,node):
    out_edges = sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('weight'), reverse=True)
    aPayer = []
    capital = G.nodes[node]['weight']
    for i in out_edges:
        if float(i[2]['weight']) < capital:
            aPayer.append(i)
            capital -= i[2]['weight']
        else: break 
    return aPayer
    
def powerOfFriendship(G, node):
    out_edges = list(G.out_edges(node,data = True))
    amis = definit_amis(G.number_of_nodes())
    aVoir = []
    aPayer = []
    for i in range(len(out_edges)):
        aVoir.append((amis[i],out_edges[i]))
    aVoir = sorted(aVoir, key= lambda x : x[0])
    for i in aVoir:
        aPayer.append(i[1])
    return aPayer