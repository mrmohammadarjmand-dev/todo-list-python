import tkinter as tk
from tkinter import messagebox

FILE_NAME = "tasks.txt"

tasks = []

# load from file
def load_tasks():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

# save to file
def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for task in tasks:
            f.write(task + "\n")

def update_list():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

def add_task():
    task = entry.get().strip()
    if task:
        tasks.append(task)
        save_tasks()
        update_list()
        entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Write something first!")

def delete_task():
    try:
        selected = listbox.curselection()[0]
        tasks.pop(selected)
        save_tasks()
        update_list()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task!")

# window
window = tk.Tk()
window.title("To-Do List Pro")
window.geometry("350x450")

tasks = load_tasks()

entry = tk.Entry(window, width=30)
entry.pack(pady=10)

tk.Button(window, text="Add Task", command=add_task).pack()
tk.Button(window, text="Delete Task", command=delete_task).pack()

listbox = tk.Listbox(window, width=40, height=18)
listbox.pack(pady=10)

update_list()

window.mainloop()
