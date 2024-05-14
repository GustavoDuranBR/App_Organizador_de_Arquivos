import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk


class ProgressBarWindow:
    def __init__(self, parent, total_files):
        self.parent = parent
        self.total_files = total_files

        self.progress_window = tk.Toplevel(parent)
        self.progress_window.title("Progresso")
        self.progress_window.geometry("300x80")

        self.set_window_icon()

        self.label = ttk.Label(self.progress_window, text="Organizando arquivos...")
        self.label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.pack(pady=5)

    def set_window_icon(self):
        # Definir o caminho do ícone
        if getattr(sys, 'frozen', False):
            # Se o script estiver congelado (executando como executável)
            icon_path = os.path.join(os.path.dirname(sys.executable), '_internal/imagens', 'icone.ico')
        else:
            # Se o script estiver sendo executado diretamente
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imagens', 'icone.ico')

        # Verificar se o arquivo de ícone existe
        if os.path.exists(icon_path):
            # Configurar iconphoto para a barra de tarefas
            icon = ImageTk.PhotoImage(file=icon_path)
            self.progress_window.iconphoto(True, icon)
        else:
            print(f"Ícone não encontrado: {icon_path}")
    
    def update_progress(self, current_file):
        progress_percentage = (current_file / self.total_files) * 100
        self.progress_bar["value"] = progress_percentage
        self.parent.update_idletasks()

    def destroy_window(self):
        self.progress_window.destroy()
