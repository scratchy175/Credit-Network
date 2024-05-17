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

        # Chemin du dossier parent fixe
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
        ax.set_xlabel('Poids total')
        ax.set_ylabel('Nombre de faillites')

        for folder in selected_folders:
            file_path = os.path.join(self.directory_path, folder, "bankruptcy_data_all_simulations.csv")
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)

                # Tracer une courbe par fichier, utilisant 'Poids total' comme abscisse
                ax.plot(data['Poids total'], data['Nombre de faillites'], label=f'Faillites - {folder}')

        ax.legend()
        plt.title('Nombre de faillites par poids total')
        plt.tight_layout()
        plt.ylim((0, 11000))

        # Générer un nom de fichier unique pour sauvegarder le graphique
        if not os.path.exists('plots'):
            os.makedirs('plots')
        filename = self.filename_entry.get()
        if not filename:
            filename = 'analyse_simulations'
        unique_filename = self.generate_unique_filename(f"plots/{filename}", '.png')
        plt.savefig(unique_filename)
        #plt.show()

        print(f"Le graphique a été sauvegardé sous '{unique_filename}'.")

root = tk.Tk()
app = FolderApp(root)
root.mainloop()
