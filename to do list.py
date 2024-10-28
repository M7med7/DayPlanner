import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from datetime import datetime, timedelta

class ToDoList:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("To Do List")
        self.window.geometry("400x700")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="My To Do List",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(pady=20)
        
        self.task_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter a new task...",
            width=300
        )
        self.task_entry.pack(pady=10)

        self.time_button = ctk.CTkButton(
            self.main_frame,
            text="Select Time",
            command=self.show_time_picker,
            width=140
        )
        self.time_button.pack(pady=10)

        self.selected_time = {"hour": 1, "minute": 0, "am_pm": "AM"}
        self.time_display = ctk.CTkLabel(
            self.main_frame,
            text="Selected time: 1:00 AM",
            font=("Helvetica", 16)
        )
        self.time_display.pack(pady=5)
        
        self.add_button = ctk.CTkButton(
            self.main_frame,
            text="Add Task",
            command=self.add_task,
            width=140
        )
        self.add_button.pack(pady=10)
        
        self.delete_all_button = ctk.CTkButton(
            self.main_frame,
            text="Delete All Tasks",
            command=self.delete_all_tasks,
            width=140,
            fg_color="#8B0000",
            hover_color="#4B0000"
        )
        self.delete_all_button.pack(pady=10)
        
        self.tasks_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=300,
            height=400
        )
        self.tasks_frame.pack(pady=10, fill="both", expand=True)
        
        self.tasks = []
        self.timer = None

    def show_time_picker(self):
        self.time_picker = ctk.CTkToplevel(self.window)
        self.time_picker.title("Select Time")
        self.time_picker.geometry("300x200")
        
        time_frame = ctk.CTkFrame(self.time_picker)
        time_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        hour_frame = ctk.CTkFrame(time_frame)
        hour_frame.pack(pady=5)
        
        ctk.CTkLabel(hour_frame, text="Hour:").pack(side="left", padx=5)
        hour_var = tk.StringVar(value=str(self.selected_time["hour"]))
        hour_spinbox = ttk.Spinbox(
            hour_frame,
            from_=1,
            to=12,
            width=5,
            textvariable=hour_var
        )
        hour_spinbox.pack(side="left", padx=5)
        
        minute_frame = ctk.CTkFrame(time_frame)
        minute_frame.pack(pady=5)
        
        ctk.CTkLabel(minute_frame, text="Minute:").pack(side="left", padx=5)
        minute_var = tk.StringVar(value=str(self.selected_time["minute"]))
        minute_spinbox = ttk.Spinbox(
            minute_frame,
            from_=0,
            to=59,
            width=5,
            textvariable=minute_var
        )
        minute_spinbox.pack(side="left", padx=5)
        
        am_pm_frame = ctk.CTkFrame(time_frame)
        am_pm_frame.pack(pady=5)
        
        am_pm_var = tk.StringVar(value=self.selected_time["am_pm"])
        am_pm_menu = ctk.CTkOptionMenu(
            am_pm_frame,
            values=["AM", "PM"],
            variable=am_pm_var
        )
        am_pm_menu.pack(pady=5)
        
        def confirm_time():
            self.selected_time["hour"] = int(hour_var.get())
            self.selected_time["minute"] = int(minute_var.get())
            self.selected_time["am_pm"] = am_pm_var.get()
            self.update_time_display()
            self.time_picker.destroy()
            
        confirm_btn = ctk.CTkButton(
            time_frame,
            text="Confirm",
            command=confirm_time
        )
        confirm_btn.pack(pady=10)
        
    def update_time_display(self):
        self.time_display.configure(
            text=f"Selected time: {self.selected_time['hour']}:{self.selected_time['minute']:02d} {self.selected_time['am_pm']}"
        )
        
    def add_task(self):
        if self.task_entry.get().strip():
            current_time = datetime.now()
            hour = self.selected_time["hour"]
            minute = self.selected_time["minute"]
            am_pm = self.selected_time["am_pm"]
            
            if am_pm == "PM" and hour != 12:
                hour += 12
            elif am_pm == "AM" and hour == 12:
                hour = 0
                
            target_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if target_time <= current_time:
                target_time += timedelta(days=1)
            
            time_diff = target_time - current_time
            if time_diff > timedelta(days=1):
                messagebox.showerror("Invalid Time", "The selected time has exceeded 24 hours. Please choose a valid time within the 24 hours.")
                return
                
            time_diff_ms = int(time_diff.total_seconds() * 1000)

            task_frame = ctk.CTkFrame(self.tasks_frame)
            task_frame.pack(pady=5, fill="x", padx=5)
            
            var = tk.BooleanVar()
            
            checkbox = ctk.CTkCheckBox(
                task_frame,
                text=f"{self.task_entry.get()} (Due: {hour}:{minute:02d} {am_pm})",
                variable=var,
                command=lambda f=task_frame: self.animate_completion(f, var)
            )
            checkbox.pack(side="left", pady=5, padx=10)
            
            delete_btn = ctk.CTkButton(
                task_frame,
                text="X",
                width=30,
                command=lambda f=task_frame: self.delete_task(f),
                fg_color="red",
                hover_color="darkred"
            )
            delete_btn.pack(side="right", pady=5, padx=10)
            
            self.tasks.append(task_frame)
            self.task_entry.delete(0, tk.END)

            if self.timer:
                self.window.after_cancel(self.timer)
            self.timer = self.window.after(time_diff_ms, self.time_up)
            
    def delete_task(self, frame):
        frame.destroy()
        self.tasks.remove(frame)
        
    def delete_all_tasks(self):
        for task in self.tasks[:]:
            task.destroy()
        self.tasks.clear()
            
    def animate_completion(self, frame, var):
        if var.get():
            frame.configure(fg_color=("gray70", "gray30"))
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.configure(text_color=("gray50", "gray50"))
        else:
            frame.configure(fg_color=("gray90", "gray13"))
            for widget in frame.winfo_children():
                if isinstance(widget, ctk.CTkCheckBox):
                    widget.configure(text_color=("gray10", "gray90"))

    def time_up(self):
        for task in self.tasks[:]:
            task.destroy()
        self.tasks.clear()
        
        messagebox.showinfo("Time's Up!", "Timer ended! All tasks have been cleared. Please add new tasks.")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ToDoList()
    app.run()
