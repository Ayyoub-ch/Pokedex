import sqlite3
import tkinter as tk
from PIL import Image, ImageTk
import io

# Fonction pour afficher les informations d'un Pokémon
def afficher_infos_pokemon(event):
    selection = liste_pokemons.curselection()
    if selection:
        index = selection[0]
        pokemon = resultat[index]

        # Effacer le contenu actuel
        for widget in frame_infos.winfo_children():
            widget.destroy()

        # Afficher les informations du Pokémon
        labels = [
            f"Nom: {pokemon[0]}",
            f"Type 1: {pokemon[1]}",
            f"Type 2: {pokemon[2] if pokemon[2] else 'N/A'}",
            f"Gen: {pokemon[3]}",
            f"Lignée Evolutive: {pokemon[4] if pokemon[4] else 'N/A'}",
            f"Méga Evolution: {pokemon[5] if pokemon[5] else 'N/A'}",
            f"Région d'Origine: {pokemon[6]}",
            f"Légendaire: {pokemon[7]}",
            f"Primo Résurgence: {pokemon[8] if pokemon[8] else 'N/A'}",
            f"Fabuleux: {pokemon[9] if pokemon[9] else 'N/A'}"
        ]

        for label in labels:
            tk.Label(frame_infos, text=label).pack(anchor='w')

        # Afficher l'image du Pokémon
        image_data = pokemon[10]
        if image_data:
            try:
                # Convertir les données binaires de l'image en format image
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(image)

                label_image = tk.Label(frame_infos, image=photo)
                label_image.image = photo  # Garder une référence pour éviter que l'image soit garbage collected
                label_image.pack()
            except Exception as e:
                print(f"Erreur de chargement de l'image: {e}")
                label_error = tk.Label(frame_infos, text="Erreur de chargement de l'image : Cannot identify image file")
                label_error.pack()

# Connexion à la base de données
connexion = sqlite3.connect('C:\\Users\\Ayyoub\\Documents\\Projets persos\\Projet bdd sqlite\\pokemon\\pokemon.sqlite3')
connexion.text_factory = lambda x: x.decode('utf-8', 'ignore') if isinstance(x, bytes) else x
curseur = connexion.cursor()

# Requête SQL pour récupérer les informations et les images des Pokémon
requete = """
SELECT f.nom, f.type1, f.type2, f.gen, f.lignée_evo, f.mega, f.regionale ,f.legendaire, f.primo, f.fabuleux, f.image FROM Formes f;
"""
curseur.execute(requete)
resultat = curseur.fetchall()
connexion.close()

# Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Informations des Pokémon")
fenetre.geometry("800x600")

# Créer un cadre pour afficher la liste des Pokémon
frame_liste = tk.Frame(fenetre)
frame_liste.pack(side='left', fill='y')

# Créer un cadre pour afficher les informations du Pokémon sélectionné
frame_infos = tk.Frame(fenetre)
frame_infos.pack(side='right', fill='both', expand=True)

# Ajouter une barre de défilement pour la liste des Pokémon
scrollbar = tk.Scrollbar(frame_liste)
scrollbar.pack(side='right', fill='y')

# Créer une liste des noms des Pokémon
liste_pokemons = tk.Listbox(frame_liste, yscrollcommand=scrollbar.set, width=40)
for pokemon in resultat:
    liste_pokemons.insert(tk.END, pokemon[0])
liste_pokemons.pack(side='left', fill='both')

# Configurer la barre de défilement
scrollbar.config(command=liste_pokemons.yview)

# Afficher les informations du Pokémon sélectionné lorsque l'utilisateur clique sur un nom dans la liste
liste_pokemons.bind('<<ListboxSelect>>', afficher_infos_pokemon)

# Démarrer la boucle principale de la fenêtre
fenetre.mainloop()
