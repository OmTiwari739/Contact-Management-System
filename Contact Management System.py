import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import re

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            return json.load(file)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as file:
        json.dump(contacts, file, indent=4)

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.root.geometry("700x500")
        self.root.configure(bg="#e6f2ff")
        self.root.resizable(False, False)

        self.contacts = load_contacts()

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#e6f2ff")
        self.style.configure("TLabel", font=("Arial", 12), background="#e6f2ff")
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.configure("TEntry", font=("Arial", 12))
        self.style.map("TButton", foreground=[('active', 'blue')], background=[('active', '#cce6ff')])

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.name_label = ttk.Label(self.main_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", pady=5)

        self.phone_label = ttk.Label(self.main_frame, text="Phone:")
        self.phone_label.grid(row=1, column=0, sticky="w", pady=5)
        self.phone_entry = ttk.Entry(self.main_frame, validate="key")
        self.phone_entry.grid(row=1, column=1, sticky="ew", pady=5)
        self.phone_entry.configure(validatecommand=(self.phone_entry.register(self.validate_phone), '%P'))

        self.email_label = ttk.Label(self.main_frame, text="Email:")
        self.email_label.grid(row=2, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(self.main_frame)
        self.email_entry.grid(row=2, column=1, sticky="ew", pady=5)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.add_button = ttk.Button(self.button_frame, text="Add Contact", command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=10)

        self.edit_button = ttk.Button(self.button_frame, text="Edit Contact", command=self.edit_contact)
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ttk.Button(self.button_frame, text="Delete Contact", command=self.delete_contact)
        self.delete_button.grid(row=0, column=2, padx=10)

        self.view_button = ttk.Button(self.button_frame, text="View Contacts", command=self.view_contacts)
        self.view_button.grid(row=0, column=3, padx=10)

        self.listbox_frame = ttk.Frame(self.main_frame)
        self.listbox_frame.grid(row=4, column=0, columnspan=2, pady=20)

        self.contacts_listbox = tk.Listbox(self.listbox_frame, width=80, height=12, font=("Arial", 10), selectmode=tk.SINGLE)
        self.contacts_listbox.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = ttk.Scrollbar(self.listbox_frame, orient="vertical", command=self.contacts_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.contacts_listbox.configure(yscrollcommand=self.scrollbar.set)

        self.refresh_contacts_list()

    def validate_phone(self, phone):
        return phone.isdigit() or phone == ""

    def validate_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if name and phone and email:
            if self.validate_email(email):
                self.contacts.append({"name": name, "phone": phone, "email": email})
                save_contacts(self.contacts)
                self.refresh_contacts_list()
                self.clear_entries()
                messagebox.showinfo("Success", "Contact added successfully.")
            else:
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def edit_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()

            if name and phone and email:
                if self.validate_email(email):
                    self.contacts[index] = {"name": name, "phone": phone, "email": email}
                    save_contacts(self.contacts)
                    self.refresh_contacts_list()
                    self.clear_entries()
                    messagebox.showinfo("Success", "Contact updated successfully.")
                else:
                    messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        selected_index = self.contacts_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.contacts[index]
            save_contacts(self.contacts)
            self.refresh_contacts_list()
            self.clear_entries()
            messagebox.showinfo("Success", "Contact deleted successfully.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def view_contacts(self):
        self.refresh_contacts_list()

    def refresh_contacts_list(self):
        self.contacts_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contacts_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()