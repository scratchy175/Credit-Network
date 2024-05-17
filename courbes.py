import os
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt

class FolderApp:
    def __init__(self, master):
        self.master = master
        master.title("Analyse des simulations")

        self.label = tk.Label(master, text="Sélectionnez les dossiers à analyser:")
        self.label.pack()

        self.listbox = tk.Listbox(master, selectmode=tk.MULTIPLE, width=50, height=15)
        self.listbox.pack()

        self.filename_label = tk.Label(master, text="Nom du fichier:")
        self.filename_label.pack()

        self.filename_entry = tk.Entry(master)
        self.filename_entry.pack()

        self.plot_button = tk.Button(master, text="Analyser et afficher le graphique", command=self.read_files_and_plot)
        self.plot_button.pack()

        self.directory_path = "simulations/"
        self.populate_listbox()

    def populate_listbox(self):
        if os.path.exists(self.directory_path):
            self.listbox.delete(0, tk.END)
            for name in os.listdir(self.directory_path):
                if os.path.isdir(os.path.join(self.directory_path, name)):
                    self.listbox.insert(tk.END, name)
        else:
            print("Le chemin spécifié n'existe pas!")

    def generate_unique_filename(self, base_filename, extension):
        counter = 1
        unique_filename = base_filename
        while os.path.exists(f"{unique_filename}{extension}"):
            unique_filename = f"{base_filename}_{counter}"
            counter += 1
        return f"{unique_filename}{extension}"

    def read_files_and_plot(self):
        selected_indices = self.listbox.curselection()
        selected_folders = [self.listbox.get(i) for i in selected_indices]

        fig, ax = plt.subplots()
        ax.set_xlabel('Argent injecté par la banque')
        ax.set_ylabel('Nombre de faillites')

        # Dictionnaire des remplacements
        replacements = {
            "highestWeightFirst": "Heavy Weight",
            "heivyWeightv2": "Heavy Weight V2",
            "lowestWeightFirst": "Light Weight",
            "newestFirst": "LIFO",
            "oldestFirst": "FIFO",
            "backToTheRichest": "Back To The Richest",
            "bankBuster":"Bank Buster",
            "debtRunner":"Debt Runner",
            "misterBigHeart":"Mister Big Heart",
            "powerOfFriendship":"Power Of Friendship",
            "theAverageJoe":"The Average Joe",
            "divergent":"Divergent",
            "equalizer":"Equalizer",
            "goodmanShow":"Goodman Show",
            "goodmanShowV2":"Goodman Show V2",
            "theGodpayer":"The Godpayer"
        }

        for folder in selected_folders:
            file_path = os.path.join(self.directory_path, folder, "bankruptcy_data_all_simulations.csv")
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)

                # Extraire seulement la dernière partie du nom de dossier pour la légende
                folder_parts = folder.split('_')
                label = f'{folder_parts[-2]}_{folder_parts[-1]}'

                # Appliquer les remplacements
                for old, new in replacements.items():
                    label = label.replace(old, new)

                ax.plot(data['Poids total'], data['Nombre de faillites'], label=f'{label}')

        plt.title('Nombre de faillites en fonction de l\' argent injecté par la banque')
        plt.tight_layout()
        plt.ylim((0, 11000))
        
        # Déplacer la légende en dehors du graphique
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=2)

        if not os.path.exists('plots'):
            os.makedirs('plots')
        filename = self.filename_entry.get()
        if not filename:
            filename = 'analyse_simulations'
        unique_filename = self.generate_unique_filename(f"plots/{filename}", '.png')
        plt.savefig(unique_filename, bbox_inches='tight')
        print(f"Le graphique a été sauvegardé sous '{unique_filename}'.")

root = tk.Tk()
app = FolderApp(root)
root.mainloop()
