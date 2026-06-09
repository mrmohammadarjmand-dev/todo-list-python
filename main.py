import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

TASKS_FILE = "tasks.json"

BG = "#f0f4f8"
PRIMARY = "#1e3a8a"
SECONDARY = "#3b82f6"
ACCENT = "#f59e0b"
DONE_COLOR = "#10b981"
DELETE_COLOR = "#ef4444"

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LIST = ("Segoe UI", 12)
FONT_BTN = ("Segoe UI", 10, "bold")
FONT_ENTRY = ("Segoe UI", 12)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("500x480")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.root.eval("tk::PlaceWindow . center")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=BG)
        self.style.configure("Title.TLabel", font=FONT_TITLE, foreground=PRIMARY, background=BG)
        self.style.configure("Counter.TLabel", font=("Segoe UI", 10), foreground="#64748b", background=BG)
        self.style.configure("Add.TButton", font=FONT_BTN, background=SECONDARY, foreground="white", borderwidth=0, padding=8)
        self.style.map("Add.TButton", background=[("active", PRIMARY)])
        self.style.configure("Done.TButton", font=FONT_BTN, background=DONE_COLOR, foreground="white", borderwidth=0, padding=8)
        self.style.map("Done.TButton", background=[("active", "#059669")])
        self.style.configure("Delete.TButton", font=FONT_BTN, background=DELETE_COLOR, foreground="white", borderwidth=0, padding=8)
        self.style.map("Delete.TButton", background=[("active", "#dc2626")])
        self.style.configure("Clear.TButton", font=FONT_BTN, background="#94a3b8", foreground="white", borderwidth=0, padding=8)
        self.style.map("Clear.TButton", background=[("active", "#64748b")])

        self.tasks = self.load_tasks()

        self.build_ui()
        self.refresh_listbox()

    def build_ui(self):
        ttk.Label(self.root, text="My To-Do List", style="Title.TLabel").pack(pady=(20, 5))

        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.listbox = tk.Listbox(
            list_frame,
            font=FONT_LIST,
            bg="white",
            fg="#1e293b",
            selectbackground=SECONDARY,
            selectforeground="white",
            activestyle="none",
            relief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#cbd5e1",
            highlightbackground="#cbd5e1"
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        entry_frame = ttk.Frame(self.root)
        entry_frame.pack(fill=tk.X, padx=20, pady=5)

        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(entry_frame, textvariable=self.entry_var, font=FONT_ENTRY)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        self.entry.bind("<Return>", lambda e: self.add_task())

        ttk.Button(entry_frame, text="Add", style="Add.TButton", command=self.add_task).pack(side=tk.LEFT, padx=(8, 0))

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=(10, 5))

        ttk.Button(btn_frame, text="Mark Done", style="Done.TButton", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete", style="Delete.TButton", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", style="Clear.TButton", command=self.clear_tasks).pack(side=tk.LEFT, padx=5)

        self.counter_label = ttk.Label(self.root, text="", style="Counter.TLabel")
        self.counter_label.pack(pady=(5, 15))

    def load_tasks(self):
        if not os.path.exists(TASKS_FILE):
            return []
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save_tasks(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks):
            prefix = "✓  " if task["done"] else "○  "
            self.listbox.insert(tk.END, f"{prefix}{task['title']}")
        pending = sum(1 for t in self.tasks if not t["done"])
        self.counter_label.config(text=f"{pending} task(s) remaining")

    def add_task(self):
        title = self.entry_var.get().strip()
        if not title:
            messagebox.showwarning("Empty", "Please enter a task title.")
            return
        self.tasks.append({"title": title, "done": False})
        self.save_tasks()
        self.entry_var.set("")
        self.refresh_listbox()

    def mark_done(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a task to mark as done.")
            return
        self.tasks[sel[0]]["done"] = True
        self.save_tasks()
        self.refresh_listbox()

    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a task to delete.")
            return
        del self.tasks[sel[0]]
        self.save_tasks()
        self.refresh_listbox()

    def clear_tasks(self):
        if not self.tasks:
            return
        if messagebox.askyesno("Confirm", "Delete all tasks permanently?"):
            self.tasks.clear()
            self.save_tasks()
            self.refresh_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
