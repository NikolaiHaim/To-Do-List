import tkinter as tk
from tkinter import messagebox, simpledialog
import json, os

DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, ValueError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("230x400")

        self.tasks = load_tasks()

        # --- Listbox setup ---
        self.listbox = tk.Listbox(root, height=15, width=40, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10, fill="both", expand=True)
        self.load_into_listbox()

        # Bind double-click for editing
        self.listbox.bind("<Double-Button-1>", self.edit_task)

        # Bind drag-drop reordering
        self.listbox.bind("<Button-1>", self.start_drag)
        self.listbox.bind("<B1-Motion>", self.do_drag)
        self.drag_data = {"index": None}

        # --- Buttons ---
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)
        #tk.Button(btn_frame, text="Save", command=self.save_all).pack(side="left", padx=5)

    # ----- Core functions -----
    def load_into_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def add_task(self):
        new_task = simpledialog.askstring("Add Task", "Enter new task:")
        if new_task:
            self.tasks.append(new_task)
            self.listbox.insert(tk.END, new_task)
            save_tasks(self.tasks)

    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a task to delete.")
            return
        idx = selected[0]
        del self.tasks[idx]
        self.listbox.delete(idx)
        save_tasks(self.tasks)

    def save_all(self):
        save_tasks(self.tasks)
        messagebox.showinfo("Saved", "Tasks saved successfully!")

    # ----- Edit existing task -----
    def edit_task(self, event=None):
        selected = self.listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        old_text = self.tasks[idx]
        new_text = simpledialog.askstring("Edit Task", "Update task:", initialvalue=old_text)
        if new_text and new_text.strip():
            self.tasks[idx] = new_text.strip()
            self.listbox.delete(idx)
            self.listbox.insert(idx, new_text)
            save_tasks(self.tasks)

    # ----- Drag & Drop Reordering -----
    def start_drag(self, event):
        self.drag_data["index"] = self.listbox.nearest(event.y)

    def do_drag(self, event):
        i = self.listbox.nearest(event.y)
        if i != self.drag_data["index"]:
            item = self.tasks.pop(self.drag_data["index"])
            self.tasks.insert(i, item)
            self.load_into_listbox()
            self.listbox.select_set(i)
            self.drag_data["index"] = i
            save_tasks(self.tasks)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
