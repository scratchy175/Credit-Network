import random as r
from datetime import *
import pickle

nb_sommet = int(input("Combien voulez-vous de sommets? "))
nb_aretes_min = int(input("Combien d'arcs au minimum par sommet? "))
nb_aretes_max = int(input("Combien d'arcs au maximum par sommet? "))
poid_min = int(input("Quelle est le poid minimum d'un arc? "))
poid_max = int(input("Quelle est le poid maximum d'un arc? "))
date_deb = int(input("Quelle est l'année de début? "))

def nb_aretes(min, max):
    cpt = 0
    aug = True
    proba = 0.99999
    while True:
        if cpt == max + 1 or aug != True:
            return min + cpt
        if (r.random() < proba**cpt) == False:
            aug = False
        cpt +=1
        
def nb_aretes(min, max):
    cpt = 0
    aug = True
    proba = 0.99999
    while True:
        if cpt == max + 1 or aug != True:
            return min + cpt
        if (r.random() < proba**cpt) == False:
            aug = False
        cpt +=1

def random_date(start_year):
    # Generate a date between January 1 of start_year and December 31 of end_year
    start_date = date(start_year, 1, 1)
    end_date = date.today()

    # Calculate the number of days between start_date and end_date
    delta_days = (end_date - start_date).days

    # Generate a random number of days to add to start_date
    random_number_of_days = r.randint(0, delta_days)

    # Return the random date
    return start_date + timedelta(days=random_number_of_days)

def genere_graph():
    nb_arc = 0
    arcs = []
    for i in range(nb_sommet):  
        for _ in range(nb_aretes(nb_aretes_min,nb_aretes_max)):
            noeud1 = i
            noeud2 = r.choice([j for j in range(nb_sommet) if j != i])
            poids = r.randint(poid_min,poid_max)
            date = random_date(date_deb)
            arcs.append((noeud1, noeud2, poids, date))
            nb_arc += 1
    with open("arcs",'wb') as f:
        pickle.dump(arcs, f)
    print(nb_arc)

genere_graph()