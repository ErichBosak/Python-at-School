import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from datetime import datetime
from medicalClasses import Patient, Appointment, AppointmentType

class PatientManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Praxis-Verwaltungssystem")
        self.root.geometry("800x600")
        
        # Datenstrukturen
        self.patients = {}  # Dictionary für Patienten (ID -> Patient)
        
        # Haupt-Tabs erstellen
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)
        
        # Patienten-Tab
        self.patients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patients_frame, text="Patienten")
        self.setup_patients_tab()
        
        # Termine-Tab
        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text="Termine")
        self.setup_appointments_tab()
        
        # Daten laden beim Start
        self.load_data()
        
    def setup_patients_tab(self):
        # Linke Seite - Patientenliste
        list_frame = ttk.Frame(self.patients_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(list_frame, text="Patienten:").pack()
        
        self.patient_listbox = tk.Listbox(list_frame, width=40)
        self.patient_listbox.pack(fill=tk.BOTH, expand=True)
        self.patient_listbox.bind('<<ListboxSelect>>', self.on_patient_select)
        
        # Rechte Seite - Patientendetails und Eingabe
        details_frame = ttk.Frame(self.patients_frame)
        details_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Eingabefelder
        ttk.Label(details_frame, text="ID:").pack()
        self.id_entry = ttk.Entry(details_frame)
        self.id_entry.pack()
        
        ttk.Label(details_frame, text="Pseudonym:").pack()
        self.pseudonym_entry = ttk.Entry(details_frame)
        self.pseudonym_entry.pack()
        
        ttk.Label(details_frame, text="Geburtsdatum (YYYY-MM-DD):").pack()
        self.birthdate_entry = ttk.Entry(details_frame)
        self.birthdate_entry.pack()
        
        ttk.Label(details_frame, text="Geschlecht:").pack()
        self.gender_entry = ttk.Entry(details_frame)
        self.gender_entry.pack()
        
        # Buttons
        ttk.Button(details_frame, text="Neuer Patient", 
                  command=self.add_patient).pack(pady=5)
        ttk.Button(details_frame, text="Patient aktualisieren", 
                  command=self.update_patient).pack(pady=5)
        ttk.Button(details_frame, text="Patient löschen", 
                  command=self.delete_patient).pack(pady=5)
        ttk.Button(details_frame, text="Daten speichern", 
                  command=self.save_data).pack(pady=5)

    def setup_appointments_tab(self):
        # Linke Seite - Terminliste
        list_frame = ttk.Frame(self.appointments_frame)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(list_frame, text="Termine:").pack()
        
        self.appointment_listbox = tk.Listbox(list_frame, width=40)
        self.appointment_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Rechte Seite - Termineingabe
        input_frame = ttk.Frame(self.appointments_frame)
        input_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Patient ID:").pack()
        self.appointment_patient_id = ttk.Entry(input_frame)
        self.appointment_patient_id.pack()
        
        ttk.Label(input_frame, text="Datum (YYYY-MM-DD):").pack()
        self.appointment_date = ttk.Entry(input_frame)
        self.appointment_date.pack()
        
        ttk.Label(input_frame, text="Termintyp:").pack()
        self.appointment_type = ttk.Combobox(input_frame, 
                                           values=[t.name for t in AppointmentType])
        self.appointment_type.pack()
        
        ttk.Label(input_frame, text="Grund:").pack()
        self.appointment_reason = ttk.Entry(input_frame)
        self.appointment_reason.pack()
        
        ttk.Button(input_frame, text="Termin hinzufügen", 
                  command=self.add_appointment).pack(pady=5)

    def on_patient_select(self, event):
            selection = self.patient_listbox.curselection()
            if not selection:
                return
            
            try:
                selected_text = self.patient_listbox.get(selection[0])
                patient_id = selected_text.split(' - ')[0]
                patient = self.patients[patient_id]
                
                # Einträge leeren und neue Werte einfügen
                self.clear_patient_entries()
                self.id_entry.insert(0, patient.id)
                self.id_entry.config(state='disabled')  # ID-Feld deaktivieren während der Bearbeitung
                self.pseudonym_entry.insert(0, patient.pseudonym)
                self.birthdate_entry.insert(0, patient.birthdate.strftime('%Y-%m-%d'))
                self.gender_entry.insert(0, patient.gender)
            except (IndexError, KeyError) as e:
                messagebox.showerror("Fehler", f"Fehler beim Laden des Patienten: {str(e)}")
                
    def add_patient(self):
        try:
            patient_id = self.id_entry.get()
            if patient_id in self.patients:
                messagebox.showerror("Fehler", "Patient ID existiert bereits!")
                return
                
            birthdate = datetime.strptime(self.birthdate_entry.get(), 
                                        '%Y-%m-%d').date()
            
            new_patient = Patient(
                id=patient_id,
                pseudonym=self.pseudonym_entry.get(),
                birthdate=birthdate,
                gender=self.gender_entry.get()
            )
            
            self.patients[patient_id] = new_patient
            self.update_patient_listbox()
            self.clear_patient_entries()
            messagebox.showinfo("Erfolg", "Patient wurde hinzugefügt!")
            
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(e)}")
    
    def add_appointment(self):
        try:
            patient_id = self.appointment_patient_id.get()
            if patient_id not in self.patients:
                messagebox.showerror("Fehler", "Patient nicht gefunden!")
                return
                
            date = datetime.strptime(self.appointment_date.get(), 
                                   '%Y-%m-%d').date()
            
            appointment = Appointment(
                date=date,
                type=AppointmentType[self.appointment_type.get()],
                reason=self.appointment_reason.get(),
                patient=self.patients[patient_id]
            )
            
            self.patients[patient_id].appointments.append(appointment)
            self.update_appointment_listbox()
            self.clear_appointment_entries()
            messagebox.showinfo("Erfolg", "Termin wurde hinzugefügt!")
            
        except (ValueError, KeyError) as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(e)}")

    def update_patient_listbox(self):
        self.patient_listbox.delete(0, tk.END)
        for patient in self.patients.values():
            self.patient_listbox.insert(tk.END, 
                f"{patient.id} - {patient.pseudonym}")

    def update_appointment_listbox(self):
        self.appointment_listbox.delete(0, tk.END)
        for patient in self.patients.values():
            for appointment in patient.appointments:
                self.appointment_listbox.insert(tk.END, 
                    f"{patient.id} - {appointment.date} - {appointment.type.name}")

    def clear_patient_entries(self):
        self.id_entry.delete(0, tk.END)
        self.pseudonym_entry.delete(0, tk.END)
        self.birthdate_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)

    def clear_appointment_entries(self):
        self.appointment_patient_id.delete(0, tk.END)
        self.appointment_date.delete(0, tk.END)
        self.appointment_type.set('')
        self.appointment_reason.delete(0, tk.END)

    def on_patient_select(self, event):
        selection = self.patient_listbox.curselection()
        if not selection:
            return
        
        patient_id = self.patient_listbox.get(selection[0]).split(' - ')[0]
        patient = self.patients[patient_id]
        
        self.clear_patient_entries()
        self.id_entry.insert(0, patient.id)
        self.pseudonym_entry.insert(0, patient.pseudonym)
        self.birthdate_entry.insert(0, patient.birthdate.strftime('%Y-%m-%d'))
        self.gender_entry.insert(0, patient.gender)

    def update_patient(self):
        selection = self.patient_listbox.curselection()
        if not selection:
            messagebox.showerror("Fehler", "Kein Patient ausgewählt!")
            return
            
        try:
            selected_text = self.patient_listbox.get(selection[0])
            patient_id = selected_text.split(' - ')[0]
            
            if patient_id not in self.patients:
                messagebox.showerror("Fehler", "Patient nicht gefunden!")
                return
                
            birthdate = datetime.strptime(self.birthdate_entry.get(), '%Y-%m-%d').date()
            
            # Patient aktualisieren, aber ID beibehalten
            self.patients[patient_id].pseudonym = self.pseudonym_entry.get()
            self.patients[patient_id].birthdate = birthdate
            self.patients[patient_id].gender = self.gender_entry.get()
            
            self.update_patient_listbox()
            self.id_entry.config(state='normal')  # ID-Feld wieder aktivieren
            self.clear_patient_entries()
            messagebox.showinfo("Erfolg", "Patient wurde aktualisiert!")
            
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(e)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Aktualisieren: {str(e)}")

    def delete_patient(self):
        selection = self.patient_listbox.curselection()
        if not selection:
            messagebox.showerror("Fehler", "Kein Patient ausgewählt!")
            return
            
        patient_id = self.patient_listbox.get(selection[0]).split(' - ')[0]
        
        if messagebox.askyesno("Löschen bestätigen", 
                             "Möchten Sie den Patienten wirklich löschen?"):
            del self.patients[patient_id]
            self.update_patient_listbox()
            self.clear_patient_entries()
            messagebox.showinfo("Erfolg", "Patient wurde gelöscht!")

    def save_data(self):
        try:
            with open('patient_data.pkl', 'wb') as f:
                pickle.dump(self.patients, f)
            messagebox.showinfo("Erfolg", "Daten wurden gespeichert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")

    def load_data(self):
        try:
            with open('patient_data.pkl', 'rb') as f:
                self.patients = pickle.load(f)
            self.update_patient_listbox()
            self.update_appointment_listbox()
        except FileNotFoundError:
            self.patients = {}
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Laden: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PatientManagementSystem(root)
    root.mainloop()