import tkinter as tk
from tkinter import ttk


class ProgressBarWindow(tk.Toplevel):
    def __init__(self, master, total_files):
        super().__init__(master)
        self.title("Progresso")
        self.geometry("300x80")

        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self, variable=self.progress_var, length=280, mode="determinate")
        self.progressbar.pack(pady=10)

        self.total_files = total_files
        self.progress_step = 100.0 / total_files

    def update_progress(self, current_file):
        self.progress_var.set(current_file * self.progress_step)
        self.update_idletasks()

    def destroy_window(self):
        self.destroy()
