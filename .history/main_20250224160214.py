import tkinter as tk
import platform
import pandas as pd
from tkinter import ttk,filedialog, messagebox



fichier_charger = False
df = None

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
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

def open_windows_choise():
    global df
    def update_name_entry(event, column_cb, name_entry):
        """Met à jour name_entry avec column_cb + '_' par défaut."""
        selected_column = column_cb.get()
        if selected_column:
            name_entry.delete(0, tk.END)
            name_entry.insert(0, selected_column + "_T")

    def add_condition():
        """Ajoute une nouvelle ligne de critères."""
        row_frame = tk.Frame(frame_conditions)
        row_frame.pack(fill="x", pady=2)

        column_cb = ttk.Combobox(row_frame, values=numeric_columns, state="readonly")
        column_cb.pack(side="left", padx=5)
        column_cb.set(numeric_columns[0] if numeric_columns else "")

        name_entry = tk.Entry(row_frame)
        name_entry.pack(side="left", padx=5)
        
        # Mettre à jour name_entry lorsqu'on sélectionne une colonne
        column_cb.bind("<<ComboboxSelected>>", lambda event, cb=column_cb, ne=name_entry: update_name_entry(event, cb, ne))

        operator_cb = ttk.Combobox(row_frame, values=operators, state="readonly")
        operator_cb.pack(side="left", padx=5)
        operator_cb.set(operators[0])

        value_entry = tk.Entry(row_frame)
        value_entry.pack(side="left", padx=5)

        conditions.append((column_cb, name_entry, operator_cb, value_entry))

    def send_conditions():
        """Récupère les conditions et appelle make_calcul."""
        selected_conditions = []
        for col_cb,name_col, op_cb, val_entry in conditions:
            col = col_cb.get()
            op = op_cb.get()
            try:
                val = float(val_entry.get().replace(",", "."))
                selected_conditions.append((col, op, val))
                
            except ValueError:
                print(f"Valeur incorrecte pour {col}: {val_entry.get()}")
        
        if selected_conditions:
            make_calcul(df, selected_conditions)

    # Fenêtre principale
    window = tk.Toplevel()
    window.title("Choisir les conditions")
    if platform.system() == "Windows":
        window.state("zoomed")

    # Détection des colonnes numériques
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
    operators = ["=", "<", ">", "⩽", "⩾", "≠"]
    conditions = []

    # Cadre pour les conditions
    frame_conditions = tk.Frame(window)
    frame_conditions.pack(fill="both", expand=True, padx=10, pady=10)

    add_condition()  # Ajoute une première ligne par défaut

    # Bouton Ajouter
    add_button = tk.Button(window, text="Ajouter", command=add_condition)
    add_button.pack(pady=5)

    # Bouton Envoyer
    send_button = tk.Button(window, text="Envoyer", command=send_conditions)
    send_button.pack(pady=5)

def make_calcul(df, selected_conditions):
    for col_cb, op_cb, val_entry in selected_conditions:
        col = col_cb
        op = op_cb
        val = val_entry
        print(f"Calcul pour {col} {op} {val}")

root = tk.Tk()
root.title("Recode")

if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Crétation de Recode").pack(pady=20)

tk.Button(root, text="Charger un fichier Excel", command=load_file).pack(pady=10)


bouton_suivant = tk.Button(
    root, text="Suivant", command=open_windows_choise, state=tk.DISABLED, )
bouton_suivant.pack()

root.mainloop()