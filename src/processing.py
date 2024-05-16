import random
import pickle

import networkx as nx
import matplotlib.pyplot as plt

global beginningCapital
beginningCapital = {}

global friends, CapitalPrevisionnel
friends = []

global capital
capital = {}

global detteMoy
detteMoy = {}


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

def oldestFirst(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('date'))

def newestFirst(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('date'), reverse=True)

def highestWeightFirst(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('weight'), reverse=True)

def lowestWeightFirst(G, node):
    return sorted(G.out_edges(node, data=True), key=lambda x: x[2].get('weight'))


def bankWars(G, node):
    # Créer un ensemble des successeurs du nœud
    successors = set(G.successors(node))

    # Trier les successeurs selon le capital initial reçu de la banque
    sorted_successors = sorted(successors, key=lambda x: beginningCapital.get(x, 0))

    # Utiliser un générateur pour parcourir les arêtes sortantes du nœud
    outgoing_edges = (edge for edge in G.out_edges(node, data=True) if edge[1] in successors)

    return [edge for edge in outgoing_edges if edge[1] in sorted_successors]

def bankBuster(G, node):
    # Créer un ensemble des successeurs du nœud
    successors = set(G.successors(node))

    # Trier les successeurs selon le capital initial reçu de la banque
    sorted_successors = sorted(successors, key=lambda x: beginningCapital.get(x, 0), reverse=True)

    # Utiliser un générateur pour parcourir les arêtes sortantes du nœud
    outgoing_edges = (edge for edge in G.out_edges(node, data=True) if edge[1] in successors)

    return [edge for edge in outgoing_edges if edge[1] in sorted_successors]



def misterBigHeart(G, node):
    capitalPrevisionnel = capital

    créanciers = sorted(
        ((succ, capitalPrevisionnel[succ]) for succ in G.successors(node) if succ in capitalPrevisionnel),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        edge
        for edge in G.out_edges(node, data=True)
        if edge[1] in {cr[0] for cr in créanciers}
    ]



def debtRunner(G, node):
    # Initialisation des variables
    aPayer = []
    # Trier les noeuds selon le nombre de dettes décroissant
    prio = sorted(G.successors(node), key=lambda x: G.out_degree(x), reverse=True)

    for creancier in prio:
        aPayer.extend(
            edge
            for edge in G.out_edges(node, data=True)
            if edge[1] == creancier
        )
    return aPayer

def theAverageJoe(G, node):
   
    CapitalPrevisionnel = detteMoy


    créanciers = sorted(
        [(succ, CapitalPrevisionnel[succ]) for succ in G.successors(node) if succ in CapitalPrevisionnel],
        key=lambda x: x[1] if x[1] is not None else float('-inf'),
        reverse=True
    )
    return [
        edge
        for elt in créanciers
        for edge in G.out_edges(node, data=True)
        if edge[1] == elt[0]
    ]


def backToTheRichest(G, n):
    # Calculer la "richesse" de chaque nœud en tant que créancier
    # La richesse est définie comme la somme des dettes qu'ils possèdent, soit le poids total des arêtes entrantes
    creditor_wealth = capital
    # Obtenir toutes les arêtes sortantes du nœud 'n'
    # Chaque arête est un tuple (n, creditor, data) où 'data' contient les détails de l'arête, y compris le montant de la dette
    outgoing_edges = list(G.out_edges(n, data=True))
    return sorted(
        outgoing_edges, key=lambda edge: creditor_wealth[edge[1]], reverse=True
    )


def heivyWeightv2(G,node):
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
    aVoir = [(friends[i], out_edges[i]) for i in range(len(out_edges))]
    aVoir = sorted(aVoir, key= lambda x : x[0])
    return [i[1] for i in aVoir]