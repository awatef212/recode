root = tk.Tk()
root.title("Incrémentation des KPI")

if platform.system() == "Windows":
    root.state("zoomed")

tk.Label(root, text="Bienvenue dans l'application de Simulation de KPI").pack(pady=20)

tk.Button(root, text="Charger un fichier Excel", command=load_file).pack(pady=10)

tk.Label(root, text="Start :",).pack()
entry_start = tk.Entry(root)
entry_start.pack()
entry_start.bind("<KeyRelease>", lambda event: verifier_conditions())

tk.Label(root, text="Stop :",).pack()
entry_stop = tk.Entry(root)
entry_stop.pack()
entry_stop.bind("<KeyRelease>", lambda event: verifier_conditions())

tk.Label(root, text="Step :",).pack()
entry_step = tk.Entry(root)
entry_step.pack()
entry_step.bind("<KeyRelease>", lambda event: verifier_conditions())

choix_var = tk.StringVar(value="Valeur continue")  
frame_choix = tk.Frame(root)
frame_choix.pack(pady=10)

tk.Label(frame_choix, text="Choisissez le type de valeur :").pack(side="left", padx=5)

rb_binaire = tk.Radiobutton(frame_choix, text="Valeur binaire", variable=choix_var, value="Valeur binaire", command=toggle_valeur)
rb_continue = tk.Radiobutton(frame_choix, text="Valeur continue", variable=choix_var, value="Valeur continue", command=toggle_valeur)

rb_binaire.pack(side="left")
rb_continue.pack(side="left")

bouton_suivant = tk.Button(
    root, text="Suivant", command=open_windows_choise, state=tk.DISABLED, )
bouton_suivant.pack()

root.mainloop()