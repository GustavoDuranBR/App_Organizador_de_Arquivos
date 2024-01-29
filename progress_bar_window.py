import tkinter as tk
from tkinter import ttk


class ProgressBarWindow:
    def __init__(self, parent, total_files):
        self.parent = parent
        self.total_files = total_files

        self.progress_window = tk.Toplevel(parent)
        self.progress_window.title("Progresso")
        self.progress_window.geometry("300x80")

        self.label = ttk.Label(self.progress_window, text="Organizando arquivos...")
        self.label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.pack(pady=5)

    def update_progress(self, current_file):
        progress_percentage = (current_file / self.total_files) * 100
        self.progress_bar["value"] = progress_percentage
        self.parent.update_idletasks()

    def destroy_window(self):
        self.progress_window.destroy()
