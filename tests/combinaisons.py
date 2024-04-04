import pandas as pd
import itertools

# Définition des listes
graphe_Type1 = ["graphe1", "graphe2", "graphe3","graphe4", "graphe5", "graphe6"]
strat1 = ["First-in First-Out", "Last-in First-out", "Heayweight", "Lightweight", "Heayweight V2",
          "Power of Friendship", "Mister Bigheart", " The Average Joe",  "The Debt Runner", "Back to the Richest", "Bank Busters", "Bank Wars"]
strat2 = ["The Equalizer", "The Goodman Show", "The Goodman Show V2", "Divergent", "The GodPayer"]

# Génération de toutes les combinaisons possibles
combinaisons = list(itertools.product(graphe_Type1, strat1, strat2))

# Création d'un dataframe pour stocker les combinaisons
columns = ["Graphe Type", "Stratégie 1", "Stratégie 2"] + graphe_Type1 + strat1 + strat2
df_combinaisons = pd.DataFrame(columns=columns)

# Remplissage du dataframe avec les combinaisons et les croix
for comb in combinaisons:
    # Initialisation de la ligne avec des zéros
    row = [""] * len(columns)
    # Remplissage des noms des éléments de la combinaison
    row[:3] = comb
    # Placement des croix pour chaque élément de la combinaison
    row[columns.index(comb[0])] = 'x'
    row[columns.index(comb[1])] = 'x'
    row[columns.index(comb[2])] = 'x'
    # Ajout de la ligne au dataframe en utilisant pandas.concat pour éviter le FutureWarning
    df_combinaisons = pd.concat([df_combinaisons, pd.DataFrame([row], columns=columns)], ignore_index=True)

# Sauvegarde du dataframe en fichier CSV avec ";" comme séparateur
csv_path = "combinaisons_graphe_strategies_semicolon.csv"
df_combinaisons.to_csv(csv_path, sep=';', index=False)

csv_path
