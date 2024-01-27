import os
import shutil
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from threading import Thread
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


class FileOrganizerApp:
    def __init__(self, tk_root: tk.Tk):
        self.root = tk_root
        self.root.title("File Organizer")
        self.root.geometry("480x610")

        self.QR_CODE_PATH = "NuBank2.png"
        self.selected_file_type = tk.StringVar()
        self.name_part_var = tk.StringVar()
        self.source_folder_var = tk.StringVar()
        self.destination_folder_var = tk.StringVar()

        self.qr_code_photo: tk.PhotoImage = self.resize_qr_code(self.QR_CODE_PATH)

        self.selected_action = tk.StringVar(value="Copy")
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0.0)
        self.organizing_in_progress = False
        self.progress_window = None

        self.create_widgets()

    def create_widgets(self):
        self.create_action_widgets()
        self.create_file_type_widgets()
        self.create_name_part_widgets()
        self.create_folder_widgets()
        self.create_organization_button()
        self.create_donation_widgets()
        self.create_footer_label()

    def create_action_widgets(self):
        action_label = tk.Label(self.root, text="Ação:")
        action_label.pack(pady=4)

        action_combobox = ttk.Combobox(self.root, textvariable=self.selected_action, values=["Copy", "Move"])
        action_combobox.pack(pady=4)

    def create_file_type_widgets(self):
        file_type_label = tk.Label(self.root, text="Tipo de Arquivo:")
        file_type_label.pack(pady=4)

        file_type_options = ["", "avi", "docx", "dwg", "exe", "html", "jpg", "json",
                             "mp3", "mp4", "mp5", "pdf", "png", "txt", "xlsx", "xml", "zip"]

        file_type_combobox = ttk.Combobox(self.root, textvariable=self.selected_file_type, values=file_type_options)
        file_type_combobox.pack(pady=4)
        file_type_combobox.bind("<Return>", lambda event: self.organize_files())

    def create_name_part_widgets(self):
        name_part_label = tk.Label(self.root, text="Parte do Nome:")
        name_part_label.pack(pady=4)

        name_part_entry = tk.Entry(self.root, textvariable=self.name_part_var)
        name_part_entry.pack(pady=4)

    def create_folder_widgets(self):
        self.create_folder_entry("Pasta de Origem:", self.source_folder_var, self.browse_source_folder)
        self.create_folder_entry("Pasta de Destino:", self.destination_folder_var, self.browse_destination_folder)

    def create_folder_entry(self, label_text, var, browse_command):
        label = tk.Label(self.root, text=label_text)
        label.pack(pady=4)

        entry = tk.Entry(self.root, textvariable=var)
        entry.pack(pady=4)

        button = tk.Button(self.root, text="Selecionar Pasta", command=browse_command)
        button.pack(pady=4)

    def create_organization_button(self):
        organize_button = tk.Button(self.root, text="Organizar", command=self.organize_files)
        organize_button.pack(pady=10)

    def create_donation_widgets(self):
        donation_label = tk.Label(self.root, text="Donation:")
        donation_label.pack(pady=4)

        qr_code_canvas = tk.Canvas(self.root, width=100, height=100)
        qr_code_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_code_photo)
        qr_code_canvas.pack(pady=4)

    def create_footer_label(self):
        footer_label = tk.Label(self.root, text="Developed by: Gustavo Duran - Version: 1.0")
        footer_label.pack(side="bottom", pady=4)

    def resize_qr_code(self, qr_code_path: str) -> tk.PhotoImage:
        max_width = 100
        max_height = 100

        qr_code_image = Image.open(qr_code_path)
        width, height = qr_code_image.size

        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        qr_code_image = qr_code_image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(qr_code_image)

    def browse_source_folder(self):
        folder_selected = filedialog.askdirectory()
        self.source_folder_var.set(folder_selected)

    def browse_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        self.destination_folder_var.set(folder_selected)

    def organize_files(self):
        if self.organizing_in_progress:
            tk.messagebox.showwarning("Aviso", "A organização já está em andamento.")
            return

        file_type = self.selected_file_type.get()
        name_part = self.name_part_var.get()
        source_folder = self.source_folder_var.get()
        dest_folder = self.destination_folder_var.get()
        self.selected_action.get()

        if not file_type and not name_part:
            tk.messagebox.showerror("Erro", "Especifique pelo menos o tipo de arquivo ou a parte do nome.")
            return

        if not file_type:
            dest_folder = os.path.join(dest_folder, f"Organizado_{name_part}")
            os.makedirs(dest_folder, exist_ok=True)
            files_to_organize = [filename for filename in os.listdir(source_folder) if name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso",
                                          f"Nenhum arquivo encontrado com a parte do nome '{name_part}'. Verifique o "
                                          f"nome e tente novamente.")
                return
        else:
            if not name_part and file_type != "Organizado":
                tk.messagebox.showerror("Erro", "Preencha o campo 'Parte do Nome'.")
                return

            dest_folder = os.path.join(dest_folder, f"{name_part}_{file_type}")
            os.makedirs(dest_folder, exist_ok=True)
            files_to_organize = [filename for filename in os.listdir(source_folder) if
                                 file_type in filename and name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso",
                                          f"Nenhum arquivo encontrado com a parte do nome '{name_part}' e tipo de "
                                          f"arquivo '{file_type}'. Verifique os campos e tente novamente.")
                return

        Thread(target=self.organize_files_thread).start()

    def organize_files_thread(self):
        file_type = self.selected_file_type.get()
        name_part = self.name_part_var.get()
        source_folder = self.source_folder_var.get()
        dest_folder = self.destination_folder_var.get()
        action = self.selected_action.get()

        if not file_type and not name_part:
            tk.messagebox.showerror("Erro", "Especifique pelo menos o tipo de arquivo ou a parte do nome.")
            return

        if not file_type:
            dest_folder = os.path.join(dest_folder, f"Organizado_{name_part}")
            os.makedirs(dest_folder, exist_ok=True)
            files_to_organize = [filename for filename in os.listdir(source_folder) if name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso",
                                          f"Nenhum arquivo encontrado com a parte do nome '{name_part}'. Verifique o "
                                          f"nome e tente novamente.")
                return
        else:
            if not name_part and file_type != "Organizado":
                tk.messagebox.showerror("Erro", "Preencha o campo 'Parte do Nome'.")
                return

            dest_folder = os.path.join(dest_folder, f"{name_part}_{file_type}")
            os.makedirs(dest_folder, exist_ok=True)
            files_to_organize = [filename for filename in os.listdir(source_folder) if
                                 file_type in filename and name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso",
                                          f"Nenhum arquivo encontrado com a parte do nome '{name_part}' e tipo de "
                                          f"arquivo '{file_type}'. Verifique os campos e tente novamente.")
                return

        self.organizing_in_progress = True

        try:
            total_files = len(files_to_organize)
            self.progress_window = ProgressBarWindow(self.root, total_files)
            self.root.update_idletasks()

            for i, filename in enumerate(files_to_organize, start=1):
                source_path = os.path.join(source_folder, filename)
                dest_path = os.path.join(dest_folder, filename)

                if action == "Copy":
                    shutil.copy2(source_path, dest_path)
                elif action == "Move":
                    shutil.move(source_path, dest_path)

                self.progress_window.update_progress(i)

            tk.messagebox.showinfo("Concluído", f"Arquivos {action.lower()}ados com sucesso.")
        finally:
            if self.progress_window:
                self.progress_window.destroy_window()
            self.organizing_in_progress = False


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
