import tkinter as tk
import platform
import pandas as pd
import numpy as np
from tkinter import ttk, filedialog, messagebox

# Variables globales
df = None
conditions = {"num": [], "order": [], "bi": []}
selection_list = []  # Stocke les lignes de sélection de colonnes/opérations

def load_file():
    global df
    file_path = filedialog.askopenfilename(
        filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
    )
    if file_path:
        try:
            df = pd.read_excel(file_path)
            messagebox.showinfo("Succès", "Fichier Excel chargé avec succès !")
            bouton_suivant.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")

def open_windows_choise():
    global df, selection_list

    if df is None:
        messagebox.showerror("Erreur", "Aucun fichier chargé.")
        return
    root.withdraw()
    # Détection des types de colonnes
    numeric_columns = [col for col in df.select_dtypes(include=['number']).columns]

    cali_multiple = [col for col in df.columns if df[col].astype(str).str.contains('/').any()]
    labels_columns = [col for col in df.columns if col not in numeric_columns + cali_multiple]

    if not (numeric_columns or cali_multiple or labels_columns):
        messagebox.showerror("Erreur", "Aucune colonne valide détectée.")
        return

    window = tk.Toplevel()
    window.title("Choisir les conditions")
    if platform.system() == "Windows":
        window.state("zoomed")

    frame_selections = tk.Frame(window)
    frame_selections.pack(pady=10)

    def add_selection_row():
        """Ajoute une nouvelle ligne de sélection pour colonne et type d'opération."""
        if selection_list:
            last_col, last_op = selection_list[-1]
            open_selected_window(last_col.get(), last_op.get(), last_col, last_op)
        
        row_frame = tk.Frame(frame_selections)
        row_frame.pack(fill="x", pady=2)
        max_length = max((len(col) for col in numeric_columns), default=10) + 2
        # Zone d'affichage des statistiques
        stat_label = tk.Label(row_frame, text="", justify="left", anchor="w")
        stat_label.pack(side="left", padx=10)
        # Liste déroulante pour choisir une colonne
        all_columns = numeric_columns + cali_multiple + labels_columns
        all_columns = [col for col in df.columns if col in all_columns]
        column_cb = ttk.Combobox(row_frame, values=all_columns, state="readonly", width=max_length)
        column_cb.pack(side="left", padx=5)
        column_cb.stat_label = stat_label
        stat_label.pack(side="left", padx=10)
        column_cb.stat_label = stat_label

        # Liste déroulante pour choisir le type d'opération
        operation_cb = ttk.Combobox(row_frame, state="readonly")
        operation_cb.pack(side="left", padx=5)
        

        def update_operations(event):
            """Met à jour les opérations possibles selon la colonne sélectionnée."""
            selected_col = column_cb.get()
            text = ""
            if selected_col in numeric_columns:
                col_data = df[selected_col].dropna()
                total = len(df[selected_col])
                nan_count = df[selected_col].isna().sum()
                nan_pct = round(nan_count / total * 100, 2)

                text += f"M: {col_data.mean():.1f},  mi: {col_data.min():.1f}, ma: {col_data.max():.1f}\n"
                text += f"Q1: {col_data.quantile(0.25):.1f}, Q2: {col_data.median():.1f}, Q3: {col_data.quantile(0.75):.1f}\n"
                text += f"Vide: {nan_count} ({nan_pct}%) BT: {total}"
                
                operation_cb["values"] = ["Numérique"]
                
            elif selected_col in cali_multiple:
                liste = pd.unique(df[selected_col])
                liste = [x for x in liste if str(x) != 'nan']
                features = set()
                for path in liste:
                    features.update(path.strip('/').split('/'))
                total = len(df)
                counts = {feat: df[selected_col].astype(str).apply(lambda x: feat in x.split('/')).sum() for feat in features}
                #sort counts
                counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
                text = "\n".join([f"{k}: {v} ({v/total*100:.1f}%)" for k, v in counts.items()])

                operation_cb["values"] = ["Binarisation"]
                
            elif selected_col in labels_columns:
                counts = df[selected_col].value_counts(dropna=False)
                total = len(df)
                text = "\n".join([f"{k}: {v} ({v/total*100:.1f}%)" for k, v in counts.items()])
                
                operation_cb["values"] = ["Binarisation", "Order"]
            
            
            operation_cb.current(0)
            stat_label.config(text=text)
        column_cb.bind("<<ComboboxSelected>>", update_operations)
            # Bouton de suppression
        # Ajouter la ligne aux sélections
        selection_list.append((column_cb, operation_cb))

    # Bouton pour ajouter une ligne
    tk.Button(window, text="Ajouter", command=add_selection_row).pack(pady=5)

    def send_conditions():
        """Ouvre la dernière condition et exécute make_calcul après la fermeture de la fenêtre."""
        if selection_list:
            last_col, last_op = selection_list[-1]
            window = open_selected_window(last_col.get(), last_op.get())
            
            if window:  # Vérifier si la fenêtre a bien été créée
                window.wait_window()  # Attendre que la fenêtre soit fermée
            
            make_calcul() 
    # Bouton pour envoyer et calculer
    tk.Button(window, text="Envoyer", command=send_conditions).pack(pady=10)

    # Ajouter une première ligne par défaut
    add_selection_row()

    window.mainloop()

def open_selected_window(column, operation, column_cb=None, operation_cb=None):
    if operation == "Numérique":
        return open_numeric_window(column, column_cb, operation_cb)
    elif operation == "Order":
        return open_order_window(column, column_cb, operation_cb)
    elif operation == "Binarisation":
        return open_binarization_window(column, column_cb, operation_cb)
    return None

def open_numeric_window(column, column_cb, operation_cb):
    """Fenêtre pour les conditions numériques."""
    num_window = tk.Toplevel()
    num_window.title(f"Condition Numérique - {column}")
    if platform.system() == "Windows":
        num_window.state("zoomed")
    tk.Label(num_window, text=f"Colonne : {column}").pack()

    operators = ["=", "<", ">", "⩽", "⩾", "≠"]
    operator_cb = ttk.Combobox(num_window, values=operators, state="readonly")
    operator_cb.pack(pady=5)

    value_entry = tk.Entry(num_window)
    value_entry.pack(pady=5)

    def save_numeric_condition():
        op = operator_cb.get()
        val = value_entry.get()
        try:
            val = float(val)
            conditions["num"].append([column, op, val])
            messagebox.showinfo("Succès", "Condition ajoutée avec succès")
            column_cb.config(state="disabled")
            operation_cb.config(state="disabled")
            if hasattr(column_cb, "stat_label") and column_cb.stat_label.winfo_exists():
                column_cb.stat_label.destroy()
            condition_text = f"{column} {op} {val}"
            label = tk.Label(operation_cb.master, text=condition_text, anchor="w")
            label.pack(side="left", padx=10)
            num_window.destroy()
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer une valeur numérique valide.")
            

    tk.Button(num_window, text="Ajouter", command=save_numeric_condition).pack(pady=10)
    return num_window

def open_order_window(column, column_cb, operation_cb):
    """Fenêtre pour ordonner les valeurs textuelles."""
    order_window = tk.Toplevel()
    order_window.title(f"Order - {column}")
    if platform.system() == "Windows":
        order_window.state("zoomed")
    tk.Label(order_window, text=f"Colonne : {column}").pack()

    value_frames = []
    for value in (df[column].unique()):
        frame = tk.Frame(order_window)
        frame.pack()
        tk.Label(frame, text=value).pack(side="left")
        entry = tk.Entry(frame, width=5)
        entry.pack(side="left")
        value_frames.append((value, entry))

    def save_order_condition():
        condition_list = [column]
        for value, entry in value_frames:
            num = entry.get()
            if num.isdigit():
                condition_list.append((value, int(num)))
        if len(condition_list) > 1:
            conditions["order"].append(condition_list)
            messagebox.showinfo("Succès", "Ordre ajouté avec succès")
            column_cb.config(state="disabled")
            operation_cb.config(state="disabled")
            if hasattr(column_cb, "stat_label") and column_cb.stat_label.winfo_exists():
                column_cb.stat_label.destroy()
            order_str = f"{column_cb.get()} : " + ", ".join([f"{v}→{n}" for v, n in condition_list[1:]])
            # order_str = ", ".join([f"{v}→{n}" for v, n in condition_list[1:]])
            label = tk.Label(operation_cb.master, text=order_str, fg="blue", anchor="w")
            label.pack(side="left", padx=10)
            order_window.destroy()

    tk.Button(order_window, text="Ajouter", command=save_order_condition).pack(pady=10)
    return order_window
def open_binarization_window(column, column_cb, operation_cb):
    """Fenêtre pour binariser les valeurs textuelles."""
    bin_window = tk.Toplevel()
    bin_window.title(f"Binarisation - {column}")
    if platform.system() == "Windows":
        bin_window.state("zoomed")
    
    tk.Label(bin_window, text=f"Colonne : {column}").pack()
    # 👇 Bloc pour afficher les fréquences
    frame_stats = tk.Frame(bin_window)
    frame_stats.pack(pady=5, anchor="w")

    value_counts = df[column].astype(str).value_counts(dropna=False)
    total = len(df)

    for val, count in value_counts.items():
        pct = count / total * 100
        if pct > 5:
            # Afficher uniquement les valeurs avec un pourcentage supérieur à 5%
            line = f"{val} : {count} ({pct:.1f}%)"
            tk.Label(frame_stats, text=line, anchor="w", justify="left").pack(anchor="w")
    value_vars = {}
    if df[column].astype(str).str.contains('/').any():
        liste = pd.unique(df[column])
        liste = [x for x in liste if str(x) != 'nan']
        features = set()
        for path in liste:
            features.update(path.strip('/').split('/'))
        
        for value in list(features):
            var = tk.BooleanVar()
            tk.Checkbutton(bin_window, text=value, variable=var).pack(anchor="w")
            value_vars[value] = var
    else:
        for value in (df[column].unique()):
            var = tk.BooleanVar()
            tk.Checkbutton(bin_window, text=value, variable=var).pack(anchor="w")
            value_vars[value] = var
    def save_binarization_condition():
        selected_values = [value for value, var in value_vars.items() if var.get()]
        if selected_values:
            conditions["bi"].append([column] + selected_values)
            messagebox.showinfo("Succès", "Binarisation ajoutée avec succès")
            column_cb.config(state="disabled")
            operation_cb.config(state="disabled")
            if hasattr(column_cb, "stat_label") and column_cb.stat_label.winfo_exists():
                column_cb.stat_label.destroy()
            bi_text = f"{column} : " + ", ".join(selected_values)
            label = tk.Label(operation_cb.master, text=bi_text, fg="purple", anchor="w")
            label.pack(side="left", padx=10)

            bin_window.destroy()

    tk.Button(bin_window, text="Ajouter", command=save_binarization_condition).pack(pady=10)
    return bin_window

def make_calcul():
    global df, conditions
    for liste_num in conditions['num']:
        name_col = liste_num[0] + str(liste_num[1]) + str(liste_num[2]).replace('.0','')
        col_index = df.columns.get_loc(liste_num[0])
        if name_col in df.columns:
            df = df.drop(columns=[name_col])
        df.insert(col_index + 1, name_col, df[liste_num[0]] * 2) 
        op = liste_num[1]
        if op == "⩽":
            op = "<="
        elif op == "⩾":
            op = ">="
        elif op == "≠":
            op = "!="
        elif op == "=":
            op = "=="
        df[name_col] = df[liste_num[0]].apply(lambda x: eval(f"x {op} {liste_num[2]}"))
        df[name_col] = df[name_col].astype(int)

    for order_condition in conditions["order"]:
        nom_colonne = order_condition[0]
        mapping_dict = {value: value_int for value, value_int in order_condition[1:]}  
        col_index = df.columns.get_loc(nom_colonne)
        new_col_name = f"{nom_colonne}_Numeric" 
        if new_col_name in df.columns:
            df = df.drop(columns=[new_col_name])
        df.insert(col_index + 1, new_col_name, df[nom_colonne] * 2) 
        df[new_col_name] = df[nom_colonne].map(mapping_dict)

    for liste_bi in conditions["bi"]:
        nom_colonne = liste_bi[0]
        valeurs = liste_bi[1:]

        # Colonnes individuelles (comme avant)
        for val in valeurs:
            name = f"{nom_colonne}_{val}"
            if name in df.columns:
                df = df.drop(columns=[name])
            col_index = df.columns.get_loc(nom_colonne)
            df.insert(col_index + 1, name, df[nom_colonne] * 2)
            df[name] = df[nom_colonne].astype(str).apply(lambda x: 1 if val in x.split('/') else 0)

        # Nouvelle colonne combinée
        combo_name = nom_colonne + "_" + " + ".join(valeurs)
        if combo_name in df.columns:
            df = df.drop(columns=[combo_name])
        col_index = df.columns.get_loc(nom_colonne)
        df.insert(col_index + 1, combo_name, df[nom_colonne] * 2)
        df[combo_name] = df[nom_colonne].astype(str).apply(
            lambda x: 1 if any(val in x.split('/') for val in valeurs) else 0
        )
    
    if filepath := filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], 
        ):
        try:
            with pd.ExcelWriter(filepath) as writer:
                df.to_excel(writer, index=False)
            messagebox.showinfo(
                "Succès", f"Résultats enregistrés dans {filepath}")
            root.destroy()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur", f"Impossible d'enregistrer le fichier : {e}")

# Fenêtre principale
root = tk.Tk()
root.title("Recodes")

if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Création de Recodes").pack(pady=20)
tk.Button(root, text="Charger un fichier Excel", command=load_file).pack(pady=10)

bouton_suivant = tk.Button(root, text="Suivant", command=open_windows_choise, state=tk.DISABLED)
bouton_suivant.pack()

root.mainloop()