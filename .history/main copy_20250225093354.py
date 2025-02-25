import tkinter as tk
import platform
import pandas as pd
from tkinter import ttk, filedialog, messagebox

# Variables globales
fichier_charger = False
df = None
add_button = None
send_button = None
conditions = []  # Liste qui contiendra les conditions

def load_file():
    global df, fichier_charger
    file_path = filedialog.askopenfilename(
        filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
    )
    if file_path:
        try:
            df = pd.read_excel(file_path)
            fichier_charger = True
            bouton_suivant.config(state=tk.NORMAL)
            messagebox.showinfo("Succès", "Fichier Excel chargé avec succès !")
        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible de charger le fichier : {e}")

def open_windows_choise():
    global df, add_button, send_button, conditions

    # Fenêtre principale
    window = tk.Toplevel()
    window.title("Choisir les conditions")
    window.geometry("450x350")

    # Détection des colonnes numériques
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    print(f"Colonnes numériques détectées: {numeric_columns}")  # Débogage
    if not numeric_columns:
        print("Aucune colonne numérique trouvée.")  # Débogage
        messagebox.showerror("Erreur", "Aucune colonne numérique trouvée dans le fichier.")
        window.destroy()
        return

    operators = ["=", "<", ">", "<=", ">=", "!="]
    
    # Cadre pour les conditions
    frame_conditions = tk.Frame(window)
    frame_conditions.pack(fill="both", expand=True, padx=10, pady=10)

    # Définition des boutons AVANT validate_condition()
    add_button = tk.Button(window, text="Ajouter", command=lambda: add_condition(), state=tk.DISABLED)
    add_button.pack(pady=5)

    send_button = tk.Button(window, text="Envoyer", command=lambda: make_calcul(), state=tk.DISABLED)
    send_button.pack(pady=5)

    def validate_condition(event=None):
        """Active ou désactive les boutons en fonction de la validité de la dernière condition."""
        if not conditions:
            add_button.config(state=tk.DISABLED)
            send_button.config(state=tk.DISABLED)
            return
        
        column, name, operator, value = conditions[-1]  # Dernière ligne ajoutée
        
        is_valid = (
            column.get() in numeric_columns and  # Colonne doit être valide
            name.get().strip() != "" and         # Nom ne doit pas être vide
            operator.get() in operators and      # Opérateur valide
            value.get().strip() != "" and value.get().replace(".", "", 1).isdigit()  # Valeur numérique
        )
        
        state = tk.NORMAL if is_valid else tk.DISABLED
        add_button.config(state=state)
        send_button.config(state=state)
    def delete_condition(index):
        """Supprimer la condition à l'index donné."""
        # Supprimer le cadre de la condition
        conditions[index][0].destroy()  # Combobox colonne
        conditions[index][1].destroy()  # Entry nom
        conditions[index][2].destroy()  # Combobox opérateur
        conditions[index][3].destroy()  # Entry valeur
        conditions[index][4].destroy()  # Bouton supprimer
        del conditions[index]  # Supprimer de la liste
        validate_condition()  # Vérifier si les boutons doivent être activés ou non



    def update_name_entry(column_cb, name_entry):
        """Met à jour name_entry avec column_cb + '_' par défaut."""
        selected_column = column_cb.get()
        print(f"update_name_entry: Sélection de la colonne: {selected_column}")  # Débogage
        if selected_column:
            name_entry.delete(0, tk.END)  # Effacer le contenu précédent
            name_entry.insert(0, selected_column + "_T")  # Ajouter le nom de la colonne avec "_"
            print(f"Nom mis à jour dans name_entry: {name_entry.get()}")  # Débogage

    def add_condition():
        """Ajoute une nouvelle ligne de critères."""
        row_frame = tk.Frame(frame_conditions)
        row_frame.pack(fill="x", pady=2)

        column_cb = ttk.Combobox(row_frame, values=numeric_columns, state="readonly")
        column_cb.pack(side="left", padx=5)
        column_cb.set(numeric_columns[0] if numeric_columns else "")

        print("Combobox 'column_cb' créée.")  # Débogage
        
        name_entry = tk.Entry(row_frame)
        name_entry.pack(side="left", padx=5)

        operator_cb = ttk.Combobox(row_frame, values=operators, state="readonly")
        operator_cb.pack(side="left", padx=5)
        operator_cb.set(operators[0])

        value_entry = tk.Entry(row_frame)
        value_entry.pack(side="left", padx=5)

                # Bouton pour supprimer cette ligne
        delete_button = tk.Button(row_frame, text="Supprimer", command=lambda: delete_condition(len(conditions)))
        delete_button.pack(side="left", padx=5)
        # Initialisation du champ 'name_entry' en fonction de la colonne sélectionnée
        update_name_entry(column_cb, name_entry)

        # Liaison de l'événement de sélection dans column_cb pour que name_entry soit mis à jour
        def on_combobox_selected(event):
            update_name_entry(column_cb, name_entry)
            validate_condition()

        column_cb.bind("<<ComboboxSelected>>", on_combobox_selected)
        name_entry.bind("<KeyRelease>", validate_condition)
        operator_cb.bind("<<ComboboxSelected>>", validate_condition)
        value_entry.bind("<KeyRelease>", validate_condition)

        # Ajouter la condition à la liste
        conditions.append((column_cb, name_entry, operator_cb, value_entry))
        validate_condition()  # Vérifier après l'ajout d'une nouvelle ligne

    add_condition()  # Ajoute une première ligne par défaut


    window.mainloop()

def make_calcul():
    """Effectue les calculs sur les conditions sélectionnées."""
    selected_conditions = []
    
    # Récupère les conditions sélectionnées (sélectionnées dans les cases)
    for col_cb, name_entry, op_cb, val_entry in conditions:
        column = col_cb.get()
        name = name_entry.get()
        operator = op_cb.get()
        value = val_entry.get()
        
        # Si tout est valide, ajouter à la liste des conditions sélectionnées
        if column and name and operator and value:
            selected_conditions.append((column, operator, value, name))
    
    # Appeler la fonction de calcul avec les conditions sélectionnées
    for col, op, val, name in selected_conditions:
        print(f"Calcul pour {name}: {col} {op} {val}")
    
    # Ici tu peux ajouter le calcul réel avec le DataFrame
    # Par exemple, filtrer les données selon les conditions sélectionnées

# Fenêtre principale
root = tk.Tk()
root.title("Recode")

if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Création de Recode").pack(pady=20)

tk.Button(root, text="Charger un fichier Excel", command=load_file).pack(pady=10)

# Bouton suivant qui ouvre la fenêtre des conditions
bouton_suivant = tk.Button(
    root, text="Suivant", command=open_windows_choise, state=tk.DISABLED, )
bouton_suivant.pack()

root.mainloop()
