import tkinter as tk
from tkinter import messagebox
import datetime

class Task:
    def __init__(self, title, priority, minutes):
        self.title = title
        self.priority = priority
        self.minutes = minutes
        self.completed = False
        self.created = datetime.datetime.now()
        self.completed_time = None

class TaskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Task App")
        self.geometry("700x500")
        self.tasks = []

        self.stats_labels = {}

        self.setup_ui()

    def setup_ui(self):
        top = tk.Frame(self, pady=10)
        top.pack(fill='x', padx=10)

        # Stat boxes
        for label in ['Pending', 'Completed', 'Total Time', 'Done %']:
            box = tk.Frame(top, bd=1, relief='solid', padx=15, pady=10)
            box.pack(side='left', padx=5, expand=True, fill='both')

            val = tk.Label(box, text='0', font=('Arial', 18))
            val.pack()
            tk.Label(box, text=label).pack()
            self.stats_labels[label] = val

        # Add Task button
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(btn_frame, text="Add Task", bg="#4CAF50", fg="white", command=self.open_task_window).pack(side='right')

        # Task list area
        self.task_list_frame = tk.Frame(self, bd=1, relief='sunken')
        self.task_list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.no_tasks_msg = tk.Label(self.task_list_frame, text="No tasks yet. Click 'Add Task' to begin.", fg="gray")
        self.no_tasks_msg.pack(pady=20)

    def open_task_window(self):
        win = tk.Toplevel(self)
        win.title("New Task")
        win.geometry("300x250")

        tk.Label(win, text="Title").pack(pady=5)
        title_entry = tk.Entry(win)
        title_entry.pack(fill='x', padx=10)

        tk.Label(win, text="Priority").pack(pady=5)
        prio = tk.StringVar(value="Medium")
        tk.OptionMenu(win, prio, "High", "Medium", "Low").pack(fill='x', padx=10)

        tk.Label(win, text="Time (minutes)").pack(pady=5)
        time_entry = tk.Entry(win)
        time_entry.insert(0, "30")
        time_entry.pack(fill='x', padx=10)

        def submit():
            title = title_entry.get().strip()
            try:
                minutes = int(time_entry.get())
            except:
                messagebox.showerror("Invalid", "Time must be a number.")
                return

            if not title:
                messagebox.showerror("Missing", "Title can't be empty.")
                return

            task = Task(title, prio.get(), minutes)
            self.tasks.append(task)
            self.render_task(task)
            self.update_stats()
            win.destroy()

        tk.Button(win, text="Submit", bg="#4CAF50", fg="white", command=submit).pack(pady=15)

    def render_task(self, task):
        if self.no_tasks_msg:
            self.no_tasks_msg.destroy()
            self.no_tasks_msg = None

        frame = tk.Frame(self.task_list_frame, bd=1, relief='solid', padx=8, pady=8)
        frame.pack(fill='x', pady=5, padx=5)

        top = tk.Frame(frame)
        top.pack(fill='x')

        done_var = tk.BooleanVar(value=task.completed)

        def toggle():
            task.completed = done_var.get()
            if task.completed:
                task.completed_time = datetime.datetime.now()
                title_lbl.config(fg='gray', font=("Arial", 11, "overstrike"))
            else:
                task.completed_time = None
                title_lbl.config(fg='black', font=("Arial", 11))
            self.update_stats()

        tk.Checkbutton(top, variable=done_var, command=toggle).pack(side='left')

        title_lbl = tk.Label(top, text=task.title, font=("Arial", 11))
        title_lbl.pack(side='left', padx=8)

        tk.Button(top, text="Delete", fg="red", command=lambda: self.remove_task(task, frame)).pack(side='right')

        meta = tk.Label(frame, text=f"{task.priority} priority | {task.minutes} min", fg="gray", font=("Arial", 9))
        meta.pack(anchor="w", pady=(5, 0))

    def remove_task(self, task, frame):
        self.tasks.remove(task)
        frame.destroy()
        if not self.tasks:
            self.no_tasks_msg = tk.Label(self.task_list_frame, text="No tasks yet. Click 'Add Task' to begin.", fg="gray")
            self.no_tasks_msg.pack(pady=20)
        self.update_stats()

    def update_stats(self):
        pending = sum(1 for t in self.tasks if not t.completed)
        done = sum(1 for t in self.tasks if t.completed)
        total_time = sum(t.minutes for t in self.tasks)
        rate = int((done / len(self.tasks)) * 100) if self.tasks else 0

        self.stats_labels["Pending"].config(text=str(pending))
        self.stats_labels["Completed"].config(text=str(done))
        self.stats_labels["Total Time"].config(text=str(total_time))
        self.stats_labels["Done %"].config(text=f"{rate}%")

if __name__ == "__main__":
    app = TaskApp()
    app.mainloop()
