import tkinter as tk
import platform
import pandas as pd
from tkinter import ttk, filedialog, messagebox


fichier_charger = False
df = None
add_button = None
send_button = None


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


import tkinter as tk
from tkinter import ttk

def open_windows_choise():
    global df

    # Fenêtre principale
    window = tk.Toplevel()
    window.title("Choisir les conditions")
    window.geometry("450x350")

    # Détection des colonnes numériques
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    operators = ["=", "<", ">", "<=", ">=", "!="]
    conditions = []

    # Cadre pour les conditions
    frame_conditions = tk.Frame(window)
    frame_conditions.pack(fill="both", expand=True, padx=10, pady=10)

    # Définition des boutons AVANT validate_condition()
    add_button = tk.Button(window, text="Ajouter", command=lambda: add_condition(), state=tk.DISABLED)
    add_button.pack(pady=5)

    send_button = tk.Button(window, text="Envoyer", command=lambda: make_calcul(), state=tk.DISABLED)
    send_button.pack(pady=5)

    def validate_condition():
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

    def update_name_entry(event, column_cb, name_entry):
        """Met à jour name_entry avec column_cb + '_' par défaut."""
        selected_column = column_cb.get()
        if selected_column:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, selected_column + "_T")
        validate_condition()

    def add_condition():
        """Ajoute une nouvelle ligne de critères."""
        row_frame = tk.Frame(frame_conditions)
        row_frame.pack(fill="x", pady=2)

        column_cb = ttk.Combobox(row_frame, values=numeric_columns, state="readonly")
        column_cb.pack(side="left", padx=5)
        column_cb.set(numeric_columns[0] if numeric_columns else "")
        
        name_entry = tk.Entry(row_frame)
        name_entry.pack(side="left", padx=5)
        
        operator_cb = ttk.Combobox(row_frame, values=operators, state="readonly")
        operator_cb.pack(side="left", padx=5)
        operator_cb.set(operators[0])

        value_entry = tk.Entry(row_frame)
        value_entry.pack(side="left", padx=5)

        # Associer les widgets à la vérification
        column_cb.bind("<<ComboboxSelected>>", lambda event: update_name_entry(event, column_cb, name_entry))
        column_cb.bind("<<ComboboxSelected>>", lambda event: validate_condition())
        name_entry.bind("<KeyRelease>", lambda event: validate_condition())
        operator_cb.bind("<<ComboboxSelected>>", lambda event: validate_condition())
        value_entry.bind("<KeyRelease>", lambda event: validate_condition())

        conditions.append((column_cb, name_entry, operator_cb, value_entry))
        validate_condition()  # Vérifier après l'ajout d'une nouvelle ligne

    add_condition()  # Ajoute une première ligne par défaut

    window.mainloop()




def make_calcul(df, selected_conditions):
    for col_cb, op_cb, val_entry, n in selected_conditions:
        col = col_cb
        op = op_cb
        val = val_entry
        print(f"Calcul pour {col} {op} {val}")


root = tk.Tk()
root.title("Recode")

if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Crétation de Recode").pack(pady=20)

tk.Button(root, text="Charger un fichier Excel",
          command=load_file).pack(pady=10)


bouton_suivant = tk.Button(
    root, text="Suivant", command=open_windows_choise, state=tk.DISABLED, )
bouton_suivant.pack()

root.mainloop()
