import tkinter as tk

root = tk.Tk()
root.title("Incrémentation des KPI")

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