import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import importlib.resources
from PIL import Image, ImageTk
import shutil
from progress_bar_window import ProgressBarWindow
from ttkthemes import ThemedTk
from datetime import datetime


class FileOrganizerAppWithThread:
    def __init__(self, tk_root: tk.Tk):
        self.root = tk_root
        self.root.title("Organizer")
        self.root.geometry("600x700")

        # Inicialize a lista de ações
        self.actions_history = []

        # Inicialize a variável action_on_close como None no __init__
        self.action_on_close = None
        self.files_to_organize_on_close = None
        self.source_folder_on_close = None
        self.dest_folder_on_close = None

        # Associar a função ao evento de fechamento
        tk_root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Criar a pasta padrão em Meus Documentos
        self.documents_folder = os.path.join(os.path.expanduser("~"), "Documents", "Organizer")
        os.makedirs(self.documents_folder, exist_ok=True)

        self.QR_CODE_PATH = "D:\\PYTHON_PROJETOS\\App_Organizador_de_Arquivos\\NuBank2.png"
        self.selected_file_type = tk.StringVar()
        self.name_part_var = tk.StringVar()
        self.source_folder_var = tk.StringVar()
        self.destination_folder_var = tk.StringVar()

        self.qr_code_photo: tk.PhotoImage = self.resize_qr_code(self.QR_CODE_PATH)

        self.selected_action = tk.StringVar(value="Copy")
        self.organizing_in_progress = False
        self.progress_window = None

        self.create_widgets()

    def load_icon(self):
        # Corrigir a inicialização da variável icon_path
        icon_path = "D:\\PYTHON_PROJETOS\\App_Organizador_de_Arquivos\\icone.ico"

        # Carregar a imagem do ícone
        try:
            if os.path.exists(icon_path):
                with open(icon_path, "rb") as icon_file:
                    icon_image = Image.open(icon_file)
                    icon_image = icon_image.resize((32, 32), Image.LANCZOS)
                    FileOrganizerAppWithThread.icon_photo = ImageTk.PhotoImage(icon_image)
            else:
                tk.messagebox.showwarning("Aviso",
                                          "Ícone não encontrado. Certifique-se de que o caminho está correto.")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar o ícone: {str(e)}")

    def create_widgets(self):
        self.create_header()
        self.create_file_options()
        self.create_folder_options()
        self.create_action_button()
        self.create_donation_section()
        self.create_footer()

    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=6)

        # Carregar a imagem
        image_path = os.path.join(os.getcwd(), 'D:\\PYTHON_PROJETOS\\App_Organizador_de_Arquivos\\imagem_software2.jpg')
        header_image = Image.open(image_path)
        header_image = ImageTk.PhotoImage(header_image)

        # Adicionar a imagem ao rótulo
        header_label = tk.Label(header_frame, image=header_image)
        header_label.image = header_image  # Garante que a imagem não seja coletada pelo coletor de lixo
        header_label.pack()

    def create_file_options(self):
        frame = ttk.LabelFrame(self.root, text="Opções de Arquivo", padding=(8, 3))
        frame.pack(pady=8, padx=8, fill="both", expand=True)

        self.create_combobox(frame, "Ação:", ["Copy", "Move"], self.selected_action)
        self.create_combobox(frame, "Tipo de Arquivo:", ["", "avi", "docx", "dwg", "exe", "jpg", "json",
                                                         "mp3", "mp4", "pdf", "png", "txt", "xlsx", "xml", "zip"],
                             self.selected_file_type)
        self.create_entry(frame, "Parte do Nome:", self.name_part_var)

    def create_folder_options(self):
        frame = ttk.LabelFrame(self.root, text="Opções de Pasta", padding=(8, 3))
        frame.pack(pady=8, padx=8, fill="both", expand=True)

        self.create_folder_entry(frame, "Pasta de Origem:", self.source_folder_var, self.browse_source_folder)
        self.create_folder_entry(frame, "Pasta de Destino:", self.destination_folder_var,
                                 self.browse_destination_folder)

        # Reduza o espaço entre o LabelFrame de doação e o rodapé
        frame.pack_configure(pady=1)

    def create_action_button(self):
        organize_button = tk.Button(self.root, text="Organizar", command=self.organize_files,
                                    font=("Helvetica", 12, "bold"))
        organize_button.pack(pady=1)

    def create_donation_section(self):
        frame = ttk.LabelFrame(self.root, text="Doação", padding=(4, 4))
        frame.pack(pady=8, padx=8, fill="both", expand=True)  # Ajuste conforme necessário

        self.create_qr_code(frame)

        # Reduza o espaço entre o LabelFrame de doação e o rodapé
        frame.pack_configure(pady=1)

    def create_footer(self):
        footer_label = tk.Label(self.root, text="Developed by: Gustavo Duran - Version: 2.0", font=("Helvetica", 11))
        footer_label.pack(side="bottom", pady=4)

    def create_combobox(self, parent, label_text, values, variable):
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=len(parent.grid_slaves()), column=10, pady=5, padx=5, sticky="w")

        combobox = ttk.Combobox(parent, textvariable=variable, values=values)
        combobox.grid(row=len(parent.grid_slaves()) - 1, column=11, pady=5, padx=5, sticky="w")

    def create_entry(self, parent, label_text, variable):
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=len(parent.grid_slaves()), column=10, pady=5, padx=5, sticky="w")

        entry = tk.Entry(parent, textvariable=variable)
        entry.grid(row=len(parent.grid_slaves()) - 1, column=11, pady=5, padx=5, sticky="w")

    def create_folder_entry(self, parent, label_text, variable, browse_command):
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=len(parent.grid_slaves()), column=10, pady=5, padx=5, sticky="w")

        entry = tk.Entry(parent, textvariable=variable)
        entry.grid(row=len(parent.grid_slaves()) - 1, column=11, pady=5, padx=5, sticky="w")

        button = tk.Button(parent, text="Selecionar Pasta", command=browse_command)
        button.grid(row=len(parent.grid_slaves()) - 1, column=12, pady=5, padx=5, sticky="w")

    def create_qr_code(self, parent):
        donation_label = tk.Label(parent, text="Doações são bem-vindas!", font=("Helvetica", 11))
        donation_label.grid(row=0, column=11, pady=5)

        qr_code_canvas = tk.Canvas(parent, width=105, height=105)
        qr_code_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_code_photo)
        qr_code_canvas.grid(row=1, column=10, pady=1)

    def resize_qr_code(self, qr_code_path: str) -> tk.PhotoImage:
        max_width = 110
        max_height = 110

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

                if os.path.isdir(source_path):
                    # Se for um diretório, use copytree
                    try:
                        shutil.copytree(source_path, dest_path)
                    except Exception as e:
                        tk.messagebox.showerror("Erro", f"Erro ao copiar o diretório: {str(e)}")
                else:
                    # Se for um arquivo, use copy2
                    try:
                        shutil.copy2(source_path, dest_path)
                    except PermissionError as pe:
                        tk.messagebox.showerror("Erro de Permissão", f"Erro de permissão: {str(pe)}")
                    except Exception as e:
                        tk.messagebox.showerror("Erro", f"Erro ao copiar o arquivo: {str(e)}")

                self.progress_window.update_progress(i)

            tk.messagebox.showinfo("Concluído", f"Arquivos {action.lower()}ados com sucesso.")
        finally:
            if self.progress_window:
                self.progress_window.destroy_window()
            self.organizing_in_progress = False

        # Adicione a ação à lista de histórico
        self.actions_history.append({
            "action": action,
            "files_to_organize": files_to_organize,
            "source_folder": source_folder,
            "dest_folder": dest_folder,
            "timestamp": datetime.now()
        })

    def on_close(self):
        # Iterar sobre a lista de ações e gerar um arquivo TXT para cada uma
        for action_info in self.actions_history:
            date_str = action_info["timestamp"].strftime("%Y-%m-%d_%H-%M-%S")
            action = action_info["action"].lower()

            organized_files_txt_path = os.path.join(self.documents_folder,
                                                    f"organized_files_{date_str}_{action}.txt")

            try:
                with open(organized_files_txt_path, "w") as txt_file:
                    for filename in action_info["files_to_organize"]:
                        source_path = os.path.join(action_info["source_folder"], filename)
                        dest_path = os.path.join(action_info["dest_folder"], filename)
                        txt_file.write(f"Arquivo: {filename}\n"
                                       f"Origem: {source_path}\n"
                                       f"Destino: {dest_path}\n\n")
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Erro ao criar o arquivo de texto: {str(e)}")
            else:
                tk.messagebox.showinfo("Concluído", f"Arquivo de texto criado em:\n{organized_files_txt_path}")

        # Fechar o aplicativo
        self.root.destroy()


if __name__ == "__main__":
    root = ThemedTk(theme="blue")
    app = FileOrganizerAppWithThread(root)
    root.mainloop()