import tkinter as tk
from tkinter import messagebox, ttk

import password_score
import get_password_length
import detect_sequential_characters
import detect_repetetive_characters
import check_password_pwned

def analyze_password():
    pwd = entry.get()
    if not pwd:
        messagebox.showwarning("Attention", "Veuillez entrer un mot de passe.")
        return

    level, percent, color = password_score.score(pwd)
    score_label.config(text=f"Score: {level}", foreground=color)
    progress['value'] = percent

    results = []

    # Appeler les fonctions et stocker les résultats
    results.append(f"Longueur : {get_password_length.get_password_length(pwd)}")
    if detect_sequential_characters.detect_sequential_characters(pwd):
        results.append(f"⚠ Séquences détectées")
    else:
        results.append(f"✅ Non séquences détectées")
    
    if detect_repetetive_characters.detect_repetetive_characters(pwd):
        results.append(f"⚠ Caractères répétés détectés")
    else:
        results.append(f"✅ Non Caractères répétés détectés")

    # Vérifier s'il est compromis (ex: via API ou base locale)
    try:
        pwned = check_password_pwned.check_password_pwned(pwd)
        if pwned :
            results.append(f"⚠ Mot de passe compromis")
        else:
            results.append(f"✅ Mot de passe non compromis")
    except Exception as e:
        results.append(f"Erreur vérification pwned: {e}")

    # Afficher les résultats
    output.delete('1.0', tk.END)
    output.insert(tk.END, "\n".join(results))


# Interface Tkinter
root = tk.Tk()
root.title("🔒 Analyseur de mot de passe")
root.geometry("450x450")
root.configure(bg="#f0f2f5")

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=("Segoe UI", 10))
style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 11))

label = tk.Label(root, text="Entrez votre mot de passe :")
label.pack(pady=10)

entry = tk.Entry(root, show="*", width=40)
entry.pack(pady=5)

btn = tk.Button(root, text="Analyser", command=analyze_password)
btn.pack(pady=10)

score_label = ttk.Label(root, text="Score: ")
score_label.pack(pady=5)

progress = ttk.Progressbar(root, length=200, mode='determinate')
progress.pack(pady=5)

output = tk.Text(root, height=10, width=50, font=("Consolas", 10))
output.pack(pady=10)

root.mainloop()
