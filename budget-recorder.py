import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

DATA_FILE = 'budget_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def add_entry():
    date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
    description = simpledialog.askstring("Input", "Enter the description:")
    amount = simpledialog.askfloat("Input", "Enter the amount:")

    if date and description and amount is not None:
        try:
            # Basic validation
            if not date or not description or amount <= 0:
                raise ValueError("Invalid input values.")
            data = load_data()
            data.append({'date': date, 'description': description, 'amount': amount})
            save_data(data)
            refresh_entries()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    else:
        messagebox.showwarning("Input Error", "All fields are required.")

def delete_entry():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        data = load_data()
        del data[index]
        save_data(data)
        refresh_entries()
    else:
        messagebox.showwarning("Selection Error", "No entry selected.")

def update_entry():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        data = load_data()
        entry = data[index]

        new_date = simpledialog.askstring("Update", "Enter new date (YYYY-MM-DD):", initialvalue=entry['date'])
        new_description = simpledialog.askstring("Update", "Enter new description:", initialvalue=entry['description'])
        new_amount = simpledialog.askfloat("Update", "Enter new amount:", initialvalue=entry['amount'])

        if new_date and new_description and new_amount is not None:
            try:
                if not new_date or not new_description or new_amount <= 0:
                    raise ValueError("Invalid input values.")
                data[index] = {'date': new_date, 'description': new_description, 'amount': new_amount}
                save_data(data)
                refresh_entries()
            except ValueError as e:
                messagebox.showerror("Input Error", str(e))
        else:
            messagebox.showwarning("Input Error", "All fields are required.")
    else:
        messagebox.showwarning("Selection Error", "No entry selected.")

def refresh_entries():
    listbox.delete(0, tk.END)
    data = load_data()
    for entry in data:
        listbox.insert(tk.END, f"{entry['date']} - {entry['description']} - ${entry['amount']}")

def search_entries():
    query = search_entry.get().lower()
    listbox.delete(0, tk.END)
    data = load_data()
    for entry in data:
        if (query in entry['date'].lower() or
            query in entry['description'].lower() or
            query in str(entry['amount'])):
            listbox.insert(tk.END, f"{entry['date']} - {entry['description']} - ${entry['amount']}")

root = tk.Tk()
root.title("Budget Recording App")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

add_button = tk.Button(frame, text="Add Entry", command=add_entry)
add_button.pack(side=tk.LEFT, padx=5)

update_button = tk.Button(frame, text="Update Entry", command=update_entry)
update_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(frame, text="Delete Entry", command=delete_entry)
delete_button.pack(side=tk.LEFT, padx=5)

search_label = tk.Label(frame, text="Search:")
search_label.pack(side=tk.LEFT, padx=5)

search_entry = tk.Entry(frame, width=20)
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(frame, text="Search", command=search_entries)
search_button.pack(side=tk.LEFT, padx=5)

listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(padx=10, pady=10)

refresh_entries()

root.mainloop()
