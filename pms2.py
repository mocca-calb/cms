import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class PatientManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Patient Management System")

        self.create_widgets()
        self.view_patients()
        self.view_doctors()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        self.patient_tab = ttk.Frame(tab_control)
        self.doctor_tab = ttk.Frame(tab_control)
        self.appointment_tab = ttk.Frame(tab_control)

        tab_control.add(self.patient_tab, text='Patients')
        tab_control.add(self.doctor_tab, text='Doctors')
        tab_control.add(self.appointment_tab, text='Appointments')
        tab_control.pack(expand=1, fill='both')

        self.create_patient_tab()
        self.create_doctor_tab()
        self.create_appointment_tab()

    def create_patient_tab(self):
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.selected_patient_id = None

        tk.Label(self.patient_tab, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.patient_tab, text="Age").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.age_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.patient_tab, text="Gender").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.gender_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.patient_tab, text="Contact").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.contact_var).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.patient_tab, text="Address").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.address_var).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.patient_tab, text="Add Patient", command=self.add_patient).grid(row=5, column=0, padx=10, pady=5)
        tk.Button(self.patient_tab, text="Update Patient", command=self.update_patient).grid(row=5, column=1, padx=10, pady=5)
        tk.Button(self.patient_tab, text="Delete Patient", command=self.delete_patient).grid(row=5, column=2, padx=10, pady=5)

        tk.Label(self.patient_tab, text="Search by Name").grid(row=6, column=0, padx=10, pady=5)
        tk.Entry(self.patient_tab, textvariable=self.search_var).grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.patient_tab, text="Search", command=self.search_patients).grid(row=6, column=2, padx=10, pady=5)

        self.patient_list = tk.Listbox(self.patient_tab, width=80)
        self.patient_list.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
        self.patient_list.bind('<<ListboxSelect>>', self.select_patient)

    def create_doctor_tab(self):
        self.doctor_name_var = tk.StringVar()
        self.specialization_var = tk.StringVar()
        self.availability_var = tk.StringVar()
        self.selected_doctor_id = None

        tk.Label(self.doctor_tab, text="Name").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.doctor_tab, textvariable=self.doctor_name_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.doctor_tab, text="Specialization").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.doctor_tab, textvariable=self.specialization_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.doctor_tab, text="Availability").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.doctor_tab, textvariable=self.availability_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.doctor_tab, text="Add Doctor", command=self.add_doctor).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self.doctor_tab, text="Update Doctor", command=self.update_doctor).grid(row=3, column=1, padx=10, pady=5)
        tk.Button(self.doctor_tab, text="Delete Doctor", command=self.delete_doctor).grid(row=3, column=2, padx=10, pady=5)

        self.doctor_list = tk.Listbox(self.doctor_tab, width=80)
        self.doctor_list.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.doctor_list.bind('<<ListboxSelect>>', self.select_doctor)

    def create_appointment_tab(self):
        self.appointment_patient_var = tk.StringVar()
        self.appointment_doctor_var = tk.StringVar()
        self.appointment_time_var = tk.StringVar()

        tk.Label(self.appointment_tab, text="Patient").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.appointment_tab, textvariable=self.appointment_patient_var).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.appointment_tab, text="Doctor").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.appointment_tab, textvariable=self.appointment_doctor_var).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.appointment_tab, text="Time").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.appointment_tab, textvariable=self.appointment_time_var).grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.appointment_tab, text="Book Appointment", command=self.book_appointment).grid(row=3, column=0, padx=10, pady=5)

        self.appointment_list = tk.Listbox(self.appointment_tab, width=80)
        self.appointment_list.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.view_appointments()

    def add_patient(self):
        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        address = self.address_var.get()

        if not name or not age or not gender or not contact or not address:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, contact, address) VALUES (?, ?, ?, ?, ?)",
                       (name, age, gender, contact, address))
        conn.commit()
        conn.close()
        self.view_patients()
        self.clear_fields()

    def update_patient(self):
        if self.selected_patient_id is None:
            messagebox.showwarning("Selection Error", "No patient selected for updating")
            return

        name = self.name_var.get()
        age = self.age_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        address = self.address_var.get()

        if not name or not age or not gender or not contact or not address:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET name = ?, age = ?, gender = ?, contact = ?, address = ? WHERE id = ?",
                       (name, age, gender, contact, address, self.selected_patient_id))
        conn.commit()
        conn.close()
        self.view_patients()
        self.clear_fields()
        self.selected_patient_id = None

    def delete_patient(self):
        if self.selected_patient_id is None:
            messagebox.showwarning("Selection Error", "No patient selected for deletion")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE id = ?", (self.selected_patient_id,))
        conn.commit()
        conn.close()
        self.view_patients()
        self.clear_fields()
        self.selected_patient_id = None

    def add_doctor(self):
        name = self.doctor_name_var.get()
        specialization = self.specialization_var.get()
        availability = self.availability_var.get()

        if not name or not specialization or not availability:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (name, specialization, availability) VALUES (?, ?, ?)",
                       (name, specialization, availability))
        conn.commit()
        conn.close()
        self.view_doctors()
        self.clear_doctor_fields()

    def update_doctor(self):
        if self.selected_doctor_id is None:
            messagebox.showwarning("Selection Error", "No doctor selected for updating")
            return

        name = self.doctor_name_var.get()
        specialization = self.specialization_var.get()
        availability = self.availability_var.get()

        if not name or not specialization or not availability:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE doctors SET name = ?, specialization = ?, availability = ? WHERE id = ?",
                       (name, specialization, availability, self.selected_doctor_id))
        conn.commit()
        conn.close()
        self.view_doctors()
        self.clear_doctor_fields()
        self.selected_doctor_id = None

    def delete_doctor(self):
        if self.selected_doctor_id is None:
            messagebox.showwarning("Selection Error", "No doctor selected for deletion")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id = ?", (self.selected_doctor_id,))
        conn.commit()
        conn.close()
        self.view_doctors()
        self.clear_doctor_fields()
        self.selected_doctor_id = None

    def book_appointment(self):
        patient = self.appointment_patient_var.get()
        doctor = self.appointment_doctor_var.get()
        time = self.appointment_time_var.get()

        if not patient or not doctor or not time:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (patient, doctor, time) VALUES (?, ?, ?)",
                       (patient, doctor, time))
        conn.commit()
        conn.close()
        self.view_appointments()
        self.clear_appointment_fields()

    def view_patients(self):
        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()
        conn.close()

        self.patient_list.delete(0, tk.END)
        for row in rows:
            self.patient_list.insert(tk.END, row)

    def view_doctors(self):
        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors")
        rows = cursor.fetchall()
        conn.close()

        self.doctor_list.delete(0, tk.END)
        for row in rows:
            self.doctor_list.insert(tk.END, row)

    def view_appointments(self):
        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        rows = cursor.fetchall()
        conn.close()

        self.appointment_list.delete(0, tk.END)
        for row in rows:
            self.appointment_list.insert(tk.END, row)

    def search_patients(self):
        search_term = self.search_var.get()
        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search_term + '%',))
        rows = cursor.fetchall()
        conn.close()

        self.patient_list.delete(0, tk.END)
        for row in rows:
            self.patient_list.insert(tk.END, row)

    def select_patient(self, event):
        selected_row = self.patient_list.curselection()
        if selected_row:
            patient = self.patient_list.get(selected_row)
            self.selected_patient_id = patient[0]
            self.name_var.set(patient[1])
            self.age_var.set(patient[2])
            self.gender_var.set(patient[3])
            self.contact_var.set(patient[4])
            self.address_var.set(patient[5])

    def select_doctor(self, event):
        selected_row = self.doctor_list.curselection()
        if selected_row:
            doctor = self.doctor_list.get(selected_row)
            self.selected_doctor_id = doctor[0]
            self.doctor_name_var.set(doctor[1])
            self.specialization_var.set(doctor[2])
            self.availability_var.set(doctor[3])

    def clear_fields(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.address_var.set("")

    def clear_doctor_fields(self):
        self.doctor_name_var.set("")
        self.specialization_var.set("")
        self.availability_var.set("")

    def clear_appointment_fields(self):
        self.appointment_patient_var.set("")
        self.appointment_doctor_var.set("")
        self.appointment_time_var.set("")

if __name__ == "__main__":
    def setup_database():
        conn = sqlite3.connect('pms.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                contact TEXT,
                address TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY,
                name TEXT,
                specialization TEXT,
                availability TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                patient TEXT,
                doctor TEXT,
                time TEXT
            )
        ''')
        conn.commit()
        conn.close()

    setup_database()
    root = tk.Tk()
    app = PatientManagementSystem(root)
    root.mainloop()