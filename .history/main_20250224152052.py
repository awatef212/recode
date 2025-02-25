import tkinter as tk
import platform
root = tk.Tk()
root.title("Incrémentation des KPI")



def load_file():
    global dfs, fichier_charger
    file_path = filedialog.askopenfilename(
        filetypes=[("Fichiers Excel", "*.xlsx *.xls")]
    )
    if file_path:
        try:
            dfs = pd.read_excel(file_path, sheet_name=None)
            fichier_charger = True
            bouton_suivant.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier : {e}")


if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Simulation de KPI").pack(pady=20)

tk.Button(root, text="Charger un fichier Excel", command=load_file).pack(pady=10)

rb_binaire.pack(side="left")
rb_continue.pack(side="left")

bouton_suivant = tk.Button(
    root, text="Suivant", command=open_windows_choise, state=tk.DISABLED, )
bouton_suivant.pack()

root.mainloop()