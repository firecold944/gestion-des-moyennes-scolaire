import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PredictionTool:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Outil de Prédiction de Moyennes Scolaires")
        self.root.geometry("1200x800")
        
        
        self.subjects = [
            "Mathématiques", "Physique-Chimie", "SVT", "EPS",
            "Anglais", "Français", "Histoire/Géographie",
            "Philosophie", "Musique/Arts Plastiques", "Conduite"
        ]
        
        self.default_coeffs = {subject: 1 for subject in self.subjects}
        
        self.grades = {}
        self.coeffs = {}
        self.predictions = {}
        
        self.create_widgets()
        
    def create_widgets(self):
        self.tabview = ctk.CTkTabview(self.root)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab1 = self.tabview.add("Saisie des notes")
        self.tab2 = self.tabview.add("Projection")
        self.tab3 = self.tabview.add("Graphiques")
        
        self.create_input_tab()
        self.create_prediction_tab()
        self.create_chart_tab()
        
        self.status_label = ctk.CTkLabel(
            self.root, 
            text="Entrez vos notes du premier trimestre et ajustez les coefficients",
            font=("Arial", 12)
        )
        self.status_label.pack(side="bottom", pady=5)
        
    def create_input_tab(self):
        grades_frame = ctk.CTkFrame(self.tab1)
        grades_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            grades_frame, 
            text="Notes du Premier Trimestre (sur 20)",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self.grade_entries = {}
        for subject in self.subjects:
            frame = ctk.CTkFrame(grades_frame)
            frame.pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(frame, text=subject, width=180).pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, width=100, placeholder_text="0-20")
            entry.pack(side="left", padx=5)
            self.grade_entries[subject] = entry
            
            validation_label = ctk.CTkLabel(frame, text="", width=50)
            validation_label.pack(side="left", padx=5)
            
        coeffs_frame = ctk.CTkFrame(self.tab1)
        coeffs_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            coeffs_frame, 
            text="Coefficients des Matières",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        self.coeff_entries = {}
        for subject in self.subjects:
            frame = ctk.CTkFrame(coeffs_frame)
            frame.pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(frame, text=subject, width=180).pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, width=100, placeholder_text="Coefficient")
            entry.insert(0, "1")
            entry.pack(side="left", padx=5)
            self.coeff_entries[subject] = entry
            
        button_frame = ctk.CTkFrame(self.tab1)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Enregistrer les notes", 
            command=self.save_grades,
            height=40,
            font=("Arial", 14)
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        ctk.CTkButton(
            button_frame, 
            text="Calculer la moyenne", 
            command=self.calculate_average,
            height=40,
            font=("Arial", 14)
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        ctk.CTkButton(
            button_frame, 
            text="Réinitialiser", 
            command=self.reset_inputs,
            height=40,
            font=("Arial", 14),
            fg_color="gray",
            hover_color="dark gray"
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        self.average_frame = ctk.CTkFrame(self.tab1, height=100)
        self.average_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.average_label = ctk.CTkLabel(
            self.average_frame, 
            text="Moyenne générale: - / 20", 
            font=("Arial", 18, "bold")
        )
        self.average_label.pack(pady=20)
        
    def create_prediction_tab(self):
        prediction_frame = ctk.CTkFrame(self.tab2)
        prediction_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            prediction_frame, 
            text="Projection pour le Prochain Trimestre",
            font=("Arial", 18, "bold")
        ).pack(pady=15)
        
        self.prediction_entries_frame = ctk.CTkScrollableFrame(prediction_frame, height=300)
        self.prediction_entries_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.prediction_entries = {}
        for subject in self.subjects:
            frame = ctk.CTkFrame(self.prediction_entries_frame)
            frame.pack(fill="x", padx=5, pady=5)
            
            ctk.CTkLabel(frame, text=subject, width=180).pack(side="left", padx=5)
            
            current_label = ctk.CTkLabel(frame, text="Actuel: -", width=80)
            current_label.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, width=100, placeholder_text="Prédiction (0-20)")
            entry.pack(side="left", padx=5)
            
            result_label = ctk.CTkLabel(frame, text="→ -", width=80)
            result_label.pack(side="left", padx=5)
            
            self.prediction_entries[subject] = {
                "entry": entry,
                "current_label": current_label,
                "result_label": result_label
            }
        
        button_frame = ctk.CTkFrame(prediction_frame)
        button_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkButton(
            button_frame, 
            text="Calculer la projection", 
            command=self.calculate_projection,
            height=40,
            font=("Arial", 14)
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        ctk.CTkButton(
            button_frame, 
            text="Appliquer amélioration de 10%", 
            command=self.apply_improvement,
            height=40,
            font=("Arial", 14)
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        ctk.CTkButton(
            button_frame, 
            text="Réinitialiser les prédictions", 
            command=self.reset_predictions,
            height=40,
            font=("Arial", 14),
            fg_color="gray",
            hover_color="dark gray"
        ).pack(side="left", padx=20, pady=10, expand=True)
        
        self.projection_frame = ctk.CTkFrame(prediction_frame, height=120)
        self.projection_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        self.projection_label = ctk.CTkLabel(
            self.projection_frame, 
            text="Projection de moyenne générale: - / 20", 
            font=("Arial", 18, "bold")
        )
        self.projection_label.pack(pady=10)
        
        self.improvement_label = ctk.CTkLabel(
            self.projection_frame, 
            text="Évolution: -", 
            font=("Arial", 14)
        )
        self.improvement_label.pack(pady=5)
        
    def create_chart_tab(self):
        chart_frame = ctk.CTkFrame(self.tab3)
        chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            chart_frame, 
            text="Visualisation des Résultats",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        self.chart_container = ctk.CTkFrame(chart_frame)
        self.chart_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.figure, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self.chart_container)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.ax.text(0.5, 0.5, 'Entrez vos notes et calculez la moyenne\ngénérale pour voir les graphiques', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=self.ax.transAxes, fontsize=14)
        self.ax.set_axis_off()
        self.canvas.draw()
        
    def save_grades(self):
        valid = True
        
        for subject in self.subjects:
            grade_text = self.grade_entries[subject].get().strip()
            coeff_text = self.coeff_entries[subject].get().strip()
            
            try:
                if grade_text:
                    grade = float(grade_text)
                    if grade < 0 or grade > 20:
                        raise ValueError
                    self.grades[subject] = grade
                else:
                    self.grades[subject] = None
            except ValueError:
                messagebox.showerror("Erreur", f"Note invalide pour {subject}. Veuillez entrer un nombre entre 0 et 20.")
                valid = False
                break
            
            try:
                if coeff_text:
                    coeff = float(coeff_text)
                    if coeff <= 0:
                        raise ValueError
                    self.coeffs[subject] = coeff
                else:
                    self.coeffs[subject] = 1.0
            except ValueError:
                messagebox.showerror("Erreur", f"Coefficient invalide pour {subject}. Veuillez entrer un nombre positif.")
                valid = False
                break
        
        if valid:
            self.status_label.configure(text="Notes enregistrées avec succès")
            self.update_prediction_tab()
            messagebox.showinfo("Succès", "Les notes ont été enregistrées avec succès.")
    
    def calculate_average(self):
        if not self.grades:
            messagebox.showwarning("Attention", "Veuillez d'abord enregistrer vos notes.")
            return
        
        total_weighted_grades = 0
        total_coeffs = 0
        grades_with_values = 0
        
        for subject in self.subjects:
            if subject in self.grades and self.grades[subject] is not None:
                total_weighted_grades += self.grades[subject] * self.coeffs[subject]
                total_coeffs += self.coeffs[subject]
                grades_with_values += 1
        
        if total_coeffs > 0 and grades_with_values > 0:
            average = total_weighted_grades / total_coeffs
            self.average_label.configure(text=f"Moyenne générale: {average:.2f} / 20")
            self.status_label.configure(text=f"Moyenne calculée: {average:.2f}/20")
            self.update_chart()
        else:
            self.average_label.configure(text="Moyenne générale: - / 20")
            messagebox.showwarning("Attention", "Aucune note valide n'a été saisie.")
    
    def update_prediction_tab(self):
        for subject in self.subjects:
            entry_data = self.prediction_entries[subject]
            if subject in self.grades and self.grades[subject] is not None:
                entry_data["current_label"].configure(text=f"Actuel: {self.grades[subject]:.1f}")
            else:
                entry_data["current_label"].configure(text="Actuel: -")
    
    def calculate_projection(self):
        if not self.grades:
            messagebox.showwarning("Attention", "Veuillez d'abord enregistrer vos notes.")
            return
        
        total_weighted_grades = 0
        total_coeffs = 0
        predictions_entered = 0
        
        for subject in self.subjects:
            entry_data = self.prediction_entries[subject]
            prediction_text = entry_data["entry"].get().strip()
            
            if prediction_text:
                try:
                    prediction = float(prediction_text)
                    if prediction < 0 or prediction > 20:
                        raise ValueError
                    
                    if subject in self.grades and self.grades[subject] is not None:
                        variation = prediction - self.grades[subject]
                        entry_data["result_label"].configure(
                            text=f"→ {prediction:.1f} ({variation:+.1f})",
                            text_color="green" if variation >= 0 else "red"
                        )
                    else:
                        entry_data["result_label"].configure(
                            text=f"→ {prediction:.1f}",
                            text_color="white"
                        )
                    
                    total_weighted_grades += prediction * self.coeffs[subject]
                    total_coeffs += self.coeffs[subject]
                    predictions_entered += 1
                    
                except ValueError:
                    if subject in self.grades and self.grades[subject] is not None:
                        total_weighted_grades += self.grades[subject] * self.coeffs[subject]
                        total_coeffs += self.coeffs[subject]
                        entry_data["result_label"].configure(
                            text=f"→ {self.grades[subject]:.1f} (identique)",
                            text_color="yellow"
                        )
            else:
                if subject in self.grades and self.grades[subject] is not None:
                    total_weighted_grades += self.grades[subject] * self.coeffs[subject]
                    total_coeffs += self.coeffs[subject]
                    entry_data["result_label"].configure(
                        text="→ (identique)",
                        text_color="gray"
                    )
        
        if total_coeffs > 0:
            current_total_weighted = 0
            current_total_coeffs = 0
            
            for subject in self.subjects:
                if subject in self.grades and self.grades[subject] is not None:
                    current_total_weighted += self.grades[subject] * self.coeffs[subject]
                    current_total_coeffs += self.coeffs[subject]
            
            if current_total_coeffs > 0:
                current_average = current_total_weighted / current_total_coeffs
                projected_average = total_weighted_grades / total_coeffs
                evolution = projected_average - current_average
                
                self.projection_label.configure(
                    text=f"Projection de moyenne générale: {projected_average:.2f} / 20"
                )
                
                if evolution >= 0:
                    self.improvement_label.configure(
                        text=f"Évolution: +{evolution:.2f} points par rapport au trimestre précédent",
                        text_color="green"
                    )
                else:
                    self.improvement_label.configure(
                        text=f"Évolution: {evolution:.2f} points par rapport au trimestre précédent",
                        text_color="red"
                    )
                
                self.status_label.configure(
                    text=f"Projection calculée: {projected_average:.2f}/20 (évolution: {evolution:+.2f})"
                )
    
    def apply_improvement(self):
        if not self.grades:
            messagebox.showwarning("Attention", "Veuillez d'abord enregistrer vos notes.")
            return
        
        for subject in self.subjects:
            if subject in self.grades and self.grades[subject] is not None:
                improved_grade = min(self.grades[subject] * 1.1, 20)
                entry_data = self.prediction_entries[subject]
                entry_data["entry"].delete(0, "end")
                entry_data["entry"].insert(0, f"{improved_grade:.1f}")
        
        self.status_label.configure(text="Amélioration de 10% appliquée à toutes les matières")
    
    def reset_inputs(self):
        for subject in self.subjects:
            self.grade_entries[subject].delete(0, "end")
            self.coeff_entries[subject].delete(0, "end")
            self.coeff_entries[subject].insert(0, "1")
        
        self.grades = {}
        self.coeffs = {}
        self.average_label.configure(text="Moyenne générale: - / 20")
        self.status_label.configure(text="Tous les champs ont été réinitialisés")
        
        self.reset_predictions()
    
    def reset_predictions(self):
        for subject in self.subjects:
            entry_data = self.prediction_entries[subject]
            entry_data["entry"].delete(0, "end")
            entry_data["current_label"].configure(text="Actuel: -")
            entry_data["result_label"].configure(text="→ -", text_color="white")
        
        self.projection_label.configure(text="Projection de moyenne générale: - / 20")
        self.improvement_label.configure(text="Évolution: -", text_color="white")
        self.status_label.configure(text="Prédictions réinitialisées")
    
    def update_chart(self):
        self.ax.clear()
        
        subjects_with_grades = []
        grades = []
        colors = []
        
        for subject in self.subjects:
            if subject in self.grades and self.grades[subject] is not None:
                subjects_with_grades.append(subject)
                grades.append(self.grades[subject])
                
                if grades[-1] < 10:
                    colors.append('red')
                elif grades[-1] < 12:
                    colors.append('orange')
                elif grades[-1] < 14:
                    colors.append('yellow')
                elif grades[-1] < 16:
                    colors.append('lightgreen')
                else:
                    colors.append('green')
        
        if subjects_with_grades:
            x_pos = np.arange(len(subjects_with_grades))
            bars = self.ax.bar(x_pos, grades, color=colors, edgecolor='black')
            
            for bar, grade in zip(bars, grades):
                height = bar.get_height()
                self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{grade:.1f}', ha='center', va='bottom')
            
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(subjects_with_grades, rotation=45, ha='right')
            
            self.ax.set_ylim(0, 21)
            self.ax.set_ylabel('Note /20')
            self.ax.set_xlabel('Matières')
            self.ax.set_title('Notes du Premier Trimestre')
            
            self.ax.axhline(y=10, color='r', linestyle='--', alpha=0.5, label='Seuil de passage (10/20)')
            
            total_weighted = sum(g * self.coeffs[subjects_with_grades[i]] for i, g in enumerate(grades))
            total_coeffs = sum(self.coeffs[subjects_with_grades[i]] for i in range(len(grades)))
            overall_average = total_weighted / total_coeffs
            
            self.ax.axhline(y=overall_average, color='blue', linestyle='-', alpha=0.7, 
                           label=f'Moyenne générale: {overall_average:.2f}/20')
            self.ax.legend()
            
            self.figure.tight_layout()
        else:
            self.ax.text(0.5, 0.5, 'Aucune note disponible\nVeuillez saisir vos notes', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=self.ax.transAxes, fontsize=14)
            self.ax.set_axis_off()
        
        self.canvas.draw()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PredictionTool()
    app.run()