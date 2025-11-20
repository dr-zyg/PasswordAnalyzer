# alternative_modern_gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Import your existing functions
import password_score
import get_password_length
import detect_sequential_characters
import detect_repetetive_characters
import check_password_pwned

# Import my icon
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class AlternativePasswordAnalyzer:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.password_visible = False
        self.analyzing = False
        
    def setup_window(self):
        self.root.iconbitmap(resource_path("logoipsum-custom-logo.ico"))
        self.root.title("Analyseur de Mot de Passe Avancé")
        self.root.geometry("600x750")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)
        self.root.minsize(810, 1000)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"600x750+{x}+{y}")
    
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Light modern color palette
        self.colors = {
            'bg_primary': '#f8f9fa',
            'bg_secondary': '#ffffff',
            'bg_tertiary': '#f1f3f4',
            'accent_primary': '#2196f3',
            'accent_secondary': '#1976d2',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'success': '#28a745',
            'warning': '#fd7e14',
            'danger': '#dc3545',
            'info': '#17a2b8',
            'border': '#dee2e6'
        }
        
        # Custom styles
        self.style.configure('Main.TFrame', background=self.colors['bg_primary'])
        self.style.configure('Card.TFrame', background=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        self.style.configure('Header.TLabel', background=self.colors['bg_primary'], foreground=self.colors['text_primary'], font=('Arial', 24, 'bold'))
        self.style.configure('Subtitle.TLabel', background=self.colors['bg_primary'], foreground=self.colors['text_secondary'], font=('Arial', 12))
        self.style.configure('Section.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], font=('Arial', 14, 'bold'))
        self.style.configure('Normal.TLabel', background=self.colors['bg_secondary'], foreground=self.colors['text_primary'], font=('Arial', 11))
        
        # Button styles
        self.style.configure('Primary.TButton', font=('Arial', 12, 'bold'), padding=(15, 10))
        self.style.map('Primary.TButton',
                      background=[('active', self.colors['accent_secondary']), ('!active', self.colors['accent_primary'])],
                      foreground=[('active', 'white'), ('!active', 'white')])
        
        # Progressbar style
        self.style.configure("Custom.Horizontal.TProgressbar",
                           troughcolor=self.colors['bg_tertiary'],
                           background=self.colors['accent_primary'],
                           borderwidth=1,
                           relief='flat')
    
    def create_widgets(self):
        # Main scrollable container
        canvas = tk.Canvas(self.root, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar_main = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Main.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_main.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_main.pack(side="right", fill="y")
        
        # Main container
        main_frame = ttk.Frame(scrollable_frame, style='Main.TFrame', padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        title_label = ttk.Label(header_frame, text="🛡️ Analyseur de Mot de Passe", style='Header.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Vérifiez la sécurité de vos mots de passe en temps réel", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Password input card
        input_card = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        input_card.pack(fill=tk.X, pady=(0, 20), padx=5)
        
        ttk.Label(input_card, text="🔐 Saisie du mot de passe", style='Section.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        # Password entry with modern styling
        entry_frame = tk.Frame(input_card, bg=self.colors['bg_secondary'])
        entry_frame.pack(fill=tk.X, pady=(0, 15))
        
        entry_border = tk.Frame(entry_frame, bg=self.colors['border'], height=2)
        entry_border.pack(fill=tk.X, side=tk.BOTTOM)
        
        entry_container = tk.Frame(entry_frame, bg=self.colors['bg_secondary'])
        entry_container.pack(fill=tk.X, pady=(0, 2))
        
        self.entry = tk.Entry(entry_container, show="*", font=('Arial', 14), bg=self.colors['bg_secondary'],
                             fg=self.colors['text_primary'], relief='flat', bd=0,
                             insertbackground=self.colors['accent_primary'])
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10)
        self.entry.bind('<KeyRelease>', self.on_password_change)
        self.entry.bind('<Return>', lambda e: self.analyze_password_threaded())
        
        # Show/Hide button
        self.toggle_btn = tk.Button(entry_container, text="👁️", font=('Arial', 12),
                                   bg=self.colors['bg_secondary'], fg=self.colors['text_secondary'],
                                   relief='flat', bd=0, cursor='hand2', command=self.toggle_password)
        self.toggle_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(input_card, bg=self.colors['bg_secondary'])
        buttons_frame.pack(fill=tk.X)
        
        self.analyze_btn = ttk.Button(buttons_frame, text="🔍 Analyser le Mot de Passe",
                                     style='Primary.TButton', command=self.analyze_password_threaded)
        self.analyze_btn.pack(side=tk.LEFT)
        
        self.clear_btn = tk.Button(buttons_frame, text="🗑️ Effacer", font=('Arial', 10),
                                  bg=self.colors['bg_tertiary'], fg=self.colors['text_secondary'],
                                  relief='flat', bd=1, cursor='hand2', command=self.clear_all,
                                  padx=15, pady=5)
        self.clear_btn.pack(side=tk.RIGHT)
        
        # Score card
        score_card = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        score_card.pack(fill=tk.X, pady=(0, 20), padx=5)
        
        ttk.Label(score_card, text="📊 Évaluation de la sécurité", style='Section.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        # Score display
        score_display_frame = tk.Frame(score_card, bg=self.colors['bg_secondary'])
        score_display_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.score_label = tk.Label(score_display_frame, text="En attente d'analyse...",
                                   font=('Arial', 16, 'bold'), bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_secondary'])
        self.score_label.pack(side=tk.LEFT)
        
        self.percentage_label = tk.Label(score_display_frame, text="",
                                        font=('Arial', 14), bg=self.colors['bg_secondary'],
                                        fg=self.colors['text_secondary'])
        self.percentage_label.pack(side=tk.RIGHT)
        
        # Progress bar
        progress_frame = tk.Frame(score_card, bg=self.colors['bg_secondary'])
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate',
                                       style="Custom.Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, ipady=8)
        
        # Loading indicator
        self.loading_label = tk.Label(score_card, text="", font=('Arial', 10, 'italic'),
                                     bg=self.colors['bg_secondary'], fg=self.colors['info'])
        self.loading_label.pack()
        
        # Results card with scrollable text
        results_card = ttk.Frame(main_frame, style='Card.TFrame', padding="25")
        results_card.pack(fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(results_card, text="📋 Détails de l'analyse", style='Section.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        # Scrollable text area
        text_frame = tk.Frame(results_card, bg=self.colors['bg_secondary'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbar
        self.output = tk.Text(text_frame, height=15, font=('Consolas', 11),
                             bg=self.colors['bg_tertiary'], fg=self.colors['text_primary'],
                             relief='flat', bd=1, wrap=tk.WORD, padx=15, pady=10,
                             insertbackground=self.colors['accent_primary'])
        
        # Vertical scrollbar
        scrollbar_v = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output.yview)
        self.output.configure(yscrollcommand=scrollbar_v.set)
        
        # Horizontal scrollbar
        scrollbar_h = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.output.xview)
        self.output.configure(xscrollcommand=scrollbar_h.set)
        
        # Pack scrollbars and text widget
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_h.pack(side=tk.BOTTOM, fill=tk.X)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure text tags for colored output
        self.output.tag_configure("success", foreground=self.colors['success'], font=('Consolas', 11, 'bold'))
        self.output.tag_configure("warning", foreground=self.colors['warning'], font=('Consolas', 11, 'bold'))
        self.output.tag_configure("danger", foreground=self.colors['danger'], font=('Consolas', 11, 'bold'))
        self.output.tag_configure("info", foreground=self.colors['info'])
        self.output.tag_configure("header", foreground=self.colors['text_primary'], font=('Consolas', 12, 'bold'))
        
        # Mouse wheel binding for canvas
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Initial message
        self.add_result("💡 Entrez un mot de passe ci-dessus et cliquez sur 'Analyser' pour commencer.", "info")
    
    def toggle_password(self):
        if self.password_visible:
            self.entry.config(show="*")
            self.toggle_btn.config(text="👁️")
            self.password_visible = False
        else:
            self.entry.config(show="")
            self.toggle_btn.config(text="🙈")
            self.password_visible = True
    
    def on_password_change(self, event=None):
        password = self.entry.get()
        if password:
            self.analyze_btn.config(text="🔍 Analyser le Mot de Passe", state='normal')
        else:
            self.analyze_btn.config(text="🔍 Analyser le Mot de Passe", state='normal')
    
    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.output.delete('1.0', tk.END)
        self.score_label.config(text="En attente d'analyse...", fg=self.colors['text_secondary'])
        self.percentage_label.config(text="")
        self.progress['value'] = 0
        self.loading_label.config(text="")
        self.add_result("💡 Entrez un mot de passe ci-dessus et cliquez sur 'Analyser' pour commencer.", "info")
    
    def analyze_password_threaded(self):
        if not self.analyzing:
            thread = threading.Thread(target=self.analyze_password)
            thread.daemon = True
            thread.start()
    
    def analyze_password(self):
        if self.analyzing:
            return
            
        pwd = self.entry.get()
        if not pwd:
            messagebox.showwarning("⚠️ Attention", "Veuillez entrer un mot de passe.")
            return

        self.analyzing = True
        self.analyze_btn.config(text="⏳ Analyse en cours...", state='disabled')
        self.loading_label.config(text="🔄 Analyse en cours, veuillez patienter...")
        
        # Clear previous results
        self.output.delete('1.0', tk.END)
        
        try:
            # Get password score
            level, percent, color = password_score.score(pwd)
            
            self.score_label.config(text=f"🎯 {level}", fg=self.get_score_color(color))
            self.percentage_label.config(text=f"{percent}%", fg=self.get_score_color(color))
            self.progress['value'] = percent
            
            # Update progress bar color
            self.update_progress_color(percent)
            
            # Add analysis header
            self.add_result("=" * 60, "header")
            self.add_result("🔍 RAPPORT D'ANALYSE DÉTAILLÉ", "header")
            self.add_result("=" * 60, "header")
            self.add_result("")
            
            # Basic information
            self.add_result("📏 INFORMATIONS GÉNÉRALES", "header")
            self.add_result(f"   Longueur du mot de passe : {get_password_length.get_password_length(pwd)} caractères", "info")
            self.add_result(f"   Force évaluée : {level} ({percent}%)", "info")
            self.add_result("")
            
            # Security checks
            self.add_result("🔒 VÉRIFICATIONS DE SÉCURITÉ", "header")
            
            # Check for sequential characters
            try:
                if detect_sequential_characters.detect_sequential_characters(pwd):
                    self.add_result("   ❌ Séquences de caractères détectées (ex: abc, 123, qwerty)", "danger")
                    self.add_result("      → Évitez les séquences prévisibles", "info")
                else:
                    self.add_result("   ✅ Aucune séquence de caractères détectée", "success")
            except Exception as e:
                self.add_result(f"   ⚠️ Erreur lors de la vérification des séquences: {e}", "warning")
            
            # Check for repetitive characters
            try:
                if detect_repetetive_characters.detect_repetetive_characters(pwd):
                    self.add_result("   ❌ Caractères répétés détectés (ex: aaa, 111, ---)", "danger")
                    self.add_result("      → Évitez la répétition de caractères", "info")
                else:
                    self.add_result("   ✅ Aucun caractère répété détecté", "success")
            except Exception as e:
                self.add_result(f"   ⚠️ Erreur lors de la vérification des répétitions: {e}", "warning")
            
            self.add_result("")
            
            # Check if password is compromised
            self.add_result("🌐 VÉRIFICATION DES FUITES DE DONNÉES", "header")
            self.add_result("   🔍 Consultation de la base HaveIBeenPwned...", "info")
            
            try:
                pwned = check_password_pwned.check_password_pwned(pwd)
                if pwned:
                    self.add_result("   🚨 ALERTE CRITIQUE !", "danger")
                    self.add_result("   ❌ Ce mot de passe a été compromis dans une fuite de données", "danger")
                    self.add_result("   📢 CHANGEZ-LE IMMÉDIATEMENT !", "danger")
                    self.add_result("      → Utilisez un nouveau mot de passe unique", "info")
                else:
                    self.add_result("   ✅ Mot de passe non trouvé dans les fuites connues", "success")
                    self.add_result("      → Ce mot de passe semble sûr côté fuites", "info")
            except Exception as e:
                self.add_result(f"   ⚠️ Impossible de vérifier les fuites: {str(e)}", "warning")
                self.add_result("      → Vérification réseau indisponible", "info")
            
            self.add_result("")
            
            # Add detailed recommendations
            self.add_recommendations(pwd, level, percent)
            
        except Exception as e:
            self.add_result(f"❌ Erreur lors de l'analyse: {str(e)}", "danger")
        
        finally:
            self.analyzing = False
            self.analyze_btn.config(text="🔍 Analyser le Mot de Passe", state='normal')
            self.loading_label.config(text="✅ Analyse terminée")
    
    def add_recommendations(self, password, level, percent):
        self.add_result("💡 RECOMMANDATIONS PERSONNALISÉES", "header")
        
        if percent <= 25:
            self.add_result("   🔴 SÉCURITÉ CRITIQUE - Action immédiate requise", "danger")
            self.add_result("   • Utilisez au moins 12-16 caractères", "warning")
            self.add_result("   • Mélangez majuscules, minuscules, chiffres et symboles", "warning")
            self.add_result("   • Évitez les mots du dictionnaire et informations personnelles", "warning")
            self.add_result("   • Considérez l'utilisation d'un gestionnaire de mots de passe", "info")
        elif percent <= 50:
            self.add_result("   🟠 SÉCURITÉ FAIBLE - Améliorations nécessaires", "warning")
            self.add_result("   • Augmentez la longueur à 14+ caractères", "warning")
            self.add_result("   • Ajoutez plus de variété dans les caractères", "warning")
            self.add_result("   • Évitez les modèles prévisibles", "info")
        elif percent <= 75:
            self.add_result("   🟡 SÉCURITÉ CORRECTE - Quelques améliorations possibles", "info")
            self.add_result("   • Votre mot de passe est relativement sûr", "success")
            self.add_result("   • Considérez l'ajout de caractères spéciaux", "info")
            self.add_result("   • Vérifiez régulièrement s'il n'est pas compromis", "info")
        else:
            self.add_result("   🟢 EXCELLENTE SÉCURITÉ - Très bon mot de passe !", "success")
            self.add_result("   • Félicitations ! Votre mot de passe est très sûr", "success")
            self.add_result("   • Continuez à utiliser des mots de passe uniques", "success")
            self.add_result("   • Changez-le régulièrement (tous les 6-12 mois)", "info")
        
        self.add_result("")
        self.add_result("🛡️ CONSEILS GÉNÉRAUX DE SÉCURITÉ", "header")
        self.add_result("   • Utilisez un mot de passe unique pour chaque compte", "info")
        self.add_result("   • Activez l'authentification à deux facteurs (2FA)", "info")
        self.add_result("   • Utilisez un gestionnaire de mots de passe", "info")
        self.add_result("   • Ne partagez jamais vos mots de passe", "info")
        self.add_result("   • Méfiez-vous des sites de phishing", "info")
        
        self.add_result("")
        self.add_result("=" * 60, "header")
        self.add_result("🔍 Analyse terminée avec succès", "success")
    
    def add_result(self, text, tag=None):
        self.output.insert(tk.END, text + "\n", tag)
        self.output.see(tk.END)
    
    def update_progress_color(self, percent):
        if percent <= 25:
            color = self.colors['danger']
        elif percent <= 50:
            color = self.colors['warning']
        elif percent <= 75:
            color = '#ffd700'
        else:
            color = self.colors['success']
        
        self.style.configure("Custom.Horizontal.TProgressbar", background=color)
    
    def get_score_color(self, color):
        color_map = {
            'red': self.colors['danger'],
            'orange': self.colors['warning'],
            'yellow': '#ffd700',
            'green': self.colors['success']
        }
        return color_map.get(color, self.colors['text_primary'])

def main():
    root = tk.Tk()
    app = AlternativePasswordAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
