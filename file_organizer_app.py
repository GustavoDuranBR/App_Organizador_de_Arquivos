import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import shutil
from progress_bar_window import ProgressBarWindow
from ttkthemes import ThemedTk
from datetime import datetime


class SplashScreen:
    def __init__(self, root, image_path, duration):
        self.root = root
        self.image_path = image_path
        self.duration = duration

    def show(self):
        splash_root = tk.Toplevel(self.root)
        splash_root.overrideredirect(True)  # Remove a borda da janela
        splash_root.geometry("+{}+{}".format(
            int(self.root.winfo_screenwidth() / 2 - 200),
            int(self.root.winfo_screenheight() / 2 - 200)
        ))

        # Carregar e exibir a imagem de splash
        splash_image = Image.open(self.image_path)
        splash_image = splash_image.resize((400, 400), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(splash_image)
        splash_label = tk.Label(splash_root, image=photo)
        splash_label.image = photo
        splash_label.pack()

        # Fechar a tela de splash após o tempo de duração
        splash_root.after(self.duration, splash_root.destroy)


class FileOrganizerApp:
    def __init__(self, tk_root: tk.Tk):
        self.root = tk_root
        self.root.title("FileWizard")
        self.root.geometry("600x700")

        # Definir o ícone do programa
        self.set_window_icon()

        # Inicialize a lista de ações
        self.actions_history = []

        # Inicialize a variável action_on_close como None no __init__
        self.action_on_close = None
        self.files_to_organize_on_close = None
        self.source_folder_on_close = None
        self.dest_folder_on_close = None

        # Adicione o atributo selection_type à classe
        self.selection_type_acao = tk.StringVar(value="Copy")
        self.selection_type_selecao = tk.StringVar(value="Ambos")

        # Associar a função ao evento de fechamento
        tk_root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Criar a pasta padrão em Meus Documentos
        self.documents_folder = os.path.join(os.path.expanduser("~"), "Documents", "Organizer")
        os.makedirs(self.documents_folder, exist_ok=True)

        if getattr(sys, 'frozen', False):
            # Se o script estiver congelado (executando como executável)
            self.QR_CODE_PATH = os.path.join(os.path.dirname(sys.executable), '_internal/imagens', 'NuBank.png')
        else:
            # Se o script estiver sendo executado diretamente
            self.QR_CODE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imagens', 'NuBank.png')

        self.selected_file_type = tk.StringVar()
        self.name_part_var = tk.StringVar()
        self.source_folder_var = tk.StringVar()
        self.destination_folder_var = tk.StringVar()

        self.qr_code_photo: tk.PhotoImage = self.resize_qr_code(self.QR_CODE_PATH)

        self.organizing_in_progress = False
        self.progress_window = None

        self.create_widgets()

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
            self.root.iconbitmap(icon_path)
        else:
            print(f"Ícone não encontrado: {icon_path}")

    def create_widgets(self):
        self.create_header()
        self.create_file_options()
        self.create_folder_options()
        self.create_action_button()
        self.create_donation_section()
        self.create_footer()

    def create_header(self):
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=0)

        # Carregar a imagem
        if getattr(sys, 'frozen', False):
            # Se o script estiver congelado (executando como executável)
            image_path = os.path.join(os.path.dirname(sys.executable), '_internal/imagens','imagem_software.png')
        else:
            # Se o script estiver sendo executado diretamente
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imagens', 'imagem_software.png')
        header_image = Image.open(image_path)
        header_image = ImageTk.PhotoImage(header_image)

        # Adicionar a imagem ao rótulo
        header_label = tk.Label(header_frame, image=header_image)
        header_label.image = header_image  # Garante que a imagem não seja coletada pelo coletor de lixo
        header_label.pack()

    def create_file_options(self):
        frame = ttk.LabelFrame(self.root, text="Opções de Arquivo", padding=(8, 3))
        frame.pack(pady=0, padx=10, fill="both", expand=True)

        self.create_combobox(frame, "Seleção:", ["Extensão", "Parte do Nome", "Ambos"], self.selection_type_selecao)  # Adicione uma opção para selecionar apenas a extensão, parte do nome ou ambos
        self.create_combobox(frame, "Ação:", ["Copy", "Move"], self.selection_type_acao)
        self.create_combobox(frame, "Tipo de Arquivo:", ["", "avi", "docx", "dwg", "exe", "jpg", "json",
                                                         "mp3", "mp4", "pdf", "png", "txt", "xlsx", "xml", "zip"],
                             self.selected_file_type)
        self.create_entry(frame, "Parte do Nome:", self.name_part_var)

    def create_folder_options(self):
        frame = ttk.LabelFrame(self.root, text="Opções de Pasta", padding=(10, 10))
        frame.pack(pady=8, padx=10, fill="both", expand=True)

        self.create_folder_entry(frame, "Pasta de Origem:", self.source_folder_var,
                                 self.browse_source_folder)
        self.create_folder_entry(frame, "Pasta de Destino:", self.destination_folder_var,
                                 self.browse_destination_folder)
        frame.pack_configure(pady=0)

    def create_action_button(self):
        frame = ttk.LabelFrame(self.root, padding=(0, 0))

        # Use ttk.Button dentro do frame
        organize_button = ttk.Button(frame, text="  Organizar", command=self.organize_files,
                                    cursor="hand2",  # Cursor de mão ao passar sobre o botão
                                    style="Custom.TButton")  # Estilo personalizado para o botão
        # Adicione um estilo para bordas arredondadas
        self.root.style = ttk.Style()
        self.root.style.configure("Custom.TButton", padding=10,
                                relief="flat", borderwidth=0,
                                font=("Helvetica", 16, "bold"), foreground="#001f3f")
        organize_button.pack(pady=10, padx=10, ipadx=20)  # Ajuste o preenchimento interno e externo

        frame.pack_configure(pady=0, padx=10, fill="both", expand=True)

    def create_donation_section(self):
        frame = ttk.LabelFrame(self.root, text="Doação", padding=(10, 10))
        frame.pack(pady=0, padx=10, fill="both", expand=True)  # Ajuste conforme necessário

        self.create_qr_code(frame)

        # Reduza o espaço entre o LabelFrame de doação e o rodapé
        frame.pack_configure(pady=0)

    def create_combobox(self, parent, label_text, values, variable):
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=len(parent.grid_slaves()), column=10, pady=0, padx=5, sticky="w")

        combobox = ttk.Combobox(parent, textvariable=variable, values=values)
        combobox.grid(row=len(parent.grid_slaves()) - 1, column=11, pady=4, padx=5, sticky="w")

    def create_entry(self, parent, label_text, variable):
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=len(parent.grid_slaves()), column=10, pady=0, padx=5, sticky="w")

        entry = tk.Entry(parent, textvariable=variable)
        entry.grid(row=len(parent.grid_slaves()) - 1, column=11, pady=0, padx=5, sticky="w")

    def create_folder_entry(self, parent, label_text, variable, browse_command):
        row_index = len(parent.grid_slaves()) // 2  # calcula o índice da linha dividindo pela metade
        label = tk.Label(parent, text=label_text, font=("Helvetica", 11))
        label.grid(row=row_index, column=0, pady=0, padx=5, sticky="w")

        entry = tk.Entry(parent, textvariable=variable, width=40)
        entry.grid(row=row_index, column=1, pady=0, padx=5, sticky="w")

        # Crie o botão "Selecionar Pasta" com o mesmo estilo personalizado
        select_folder_button = ttk.Button(parent, text="Selecionar Pasta", command=browse_command)
        select_folder_button.grid(row=row_index, column=2, pady=0, padx=5, sticky="w")

    def create_qr_code(self, parent):
        donation_label = tk.Label(parent, text="Doações são bem-vindas!", font=("Helvetica", 11))
        donation_label.grid(row=0, column=11, pady=0)

        qr_code_canvas = tk.Canvas(parent, width=105, height=105)
        qr_code_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_code_photo)
        qr_code_canvas.grid(row=1, column=50, pady=0)

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
    
    def create_footer(self):
        footer_label = tk.Label(self.root, text="Developed by: Gustavo Duran - Version: 2.4", font=("Helvetica", 11))
        footer_label.pack(side="bottom", pady=0)

    def browse_source_folder(self):
        folder_selected = filedialog.askdirectory()
        self.source_folder_var.set(folder_selected)

    def browse_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        self.destination_folder_var.set(folder_selected)

    def organize_files(self):
        if self.organizing_in_progress:
            messagebox.showwarning("Aviso", "A organização já está em andamento.")
            return

        selected_action = self.selection_type_acao.get()  # Obtenha a seleção do usuário (Copy ou Move)
        selection_type_selecao = self.selection_type_selecao.get()  # Obtenha a seleção do usuário (Extensão, Parte do Nome ou Ambos)
        file_type = self.selected_file_type.get().lower()
        name_part = self.name_part_var.get()
        source_folder = self.source_folder_var.get()
        dest_folder = self.destination_folder_var.get()

        if selection_type_selecao == "Extensão" and not file_type:  # Verifique se o usuário selecionou apenas a extensão, mas não forneceu uma extensão
            messagebox.showerror("Erro", "Selecione o tipo de arquivo.")
            return

        if selection_type_selecao == "Parte do Nome" and not name_part:  # Verifique se o usuário selecionou apenas parte do nome, mas não forneceu uma parte do nome
            messagebox.showerror("Erro", "Digite a parte do nome.")
            return

        if selection_type_selecao == "Ambos" and not file_type and not name_part:  # Verifique se o usuário selecionou ambos, mas não forneceu nem a extensão nem a parte do nome
            messagebox.showerror("Erro", "Especifique pelo menos o tipo de arquivo ou a parte do nome.")
            return

        self.organizing_in_progress = True

        try:
            if selection_type_selecao == "Extensão" and not name_part:
                # Se a seleção for feita apenas por extensão e não houver parte do nome especificada
                dest_folder = os.path.join(dest_folder, f"Organizado_{file_type}")
                os.makedirs(dest_folder, exist_ok=True)
                files_to_organize = [filename for filename in os.listdir(source_folder) if filename.lower().endswith(f".{file_type}")]
            else:
                # Caso contrário, faça como antes
                if not file_type and not name_part:
                    messagebox.showerror("Erro", "Especifique pelo menos o tipo de arquivo ou a parte do nome.")
                    return

                if not file_type:
                    dest_folder = os.path.join(dest_folder, f"Organizado {name_part}")
                    os.makedirs(dest_folder, exist_ok=True)
                    files_to_organize = [filename for filename in os.listdir(source_folder) if name_part in filename]

                    if not files_to_organize:
                        messagebox.showwarning("Aviso",
                                                f"Nenhum arquivo encontrado com a parte do nome '{name_part}'. Verifique o "
                                                f"nome e tente novamente.")
                        return
                else:
                    if not name_part and file_type != "Organizado":
                        messagebox.showerror("Erro", "Preencha o campo 'Parte do Nome'.")
                        return

                    dest_folder = os.path.join(dest_folder, f"{name_part}_{file_type}")
                    os.makedirs(dest_folder, exist_ok=True)
                    files_to_organize = [filename for filename in os.listdir(source_folder) if
                                        file_type in filename and name_part in filename]

                    if not files_to_organize:
                        messagebox.showwarning("Aviso",
                                                f"Nenhum arquivo encontrado com a parte do nome '{name_part}' e tipo de "
                                                f"arquivo '{file_type}'. Verifique os campos e tente novamente.")
                        return

            total_files = len(files_to_organize)
            self.progress_window = ProgressBarWindow(self.root, total_files)
            self.root.update_idletasks()

            for i, filename in enumerate(files_to_organize, start=1):
                source_path = os.path.join(source_folder, filename)
                dest_path = os.path.join(dest_folder, filename)

                if os.path.isdir(source_path):
                    if selected_action == "Copy":
                        # Se for um diretório e a ação for "Copy", use copytree
                        try:
                            shutil.copytree(source_path, dest_path)
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao copiar o diretório: {str(e)}")
                    elif selected_action == "Move":
                        # Se for um diretório e a ação for "Move", use move
                        try:
                            shutil.move(source_path, dest_path)
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao mover o diretório: {str(e)}")
                else:
                    if selected_action == "Copy":
                        # Se for um arquivo e a ação for "Copy", use copy2
                        try:
                            shutil.copy2(source_path, dest_path)
                        except PermissionError as pe:
                            messagebox.showerror("Erro de Permissão", f"Erro de permissão: {str(pe)}")
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao copiar o arquivo: {str(e)}")
                    elif selected_action == "Move":
                        # Se for um arquivo e a ação for "Move", use move
                        try:
                            shutil.move(source_path, dest_path)
                        except PermissionError as pe:
                            messagebox.showerror("Erro de Permissão", f"Erro de permissão: {str(pe)}")
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao mover o arquivo: {str(e)}")

                self.progress_window.update_progress(current_file=i)

            messagebox.showinfo("Concluído", f"Os arquivos foram organizados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao organizar os arquivos: {str(e)}")
        finally:
            if self.progress_window:
                self.progress_window.destroy_window()
            self.organizing_in_progress = False

            # Adicione a ação à lista de histórico
        self.actions_history.append({
            "action": selected_action,
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

            dest_folder = action_info["dest_folder"]  # Use a pasta de destino

            organized_files_txt_path = os.path.join(dest_folder, f"organized_files_{date_str}_{action}.txt")

            try:
                with open(organized_files_txt_path, "w") as txt_file:
                    for filename in action_info["files_to_organize"]:
                        source_path = os.path.join(action_info["source_folder"], filename)
                        dest_path = os.path.join(action_info["dest_folder"], filename)
                        txt_file.write(f"Arquivo: {filename}\n"
                                       f"Origem: {source_path}\n"
                                       f"Destino: {dest_path}\n\n")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar o arquivo de texto: {str(e)}")
            else:
                messagebox.showinfo("Concluído", f"Arquivo de texto criado em:\n{organized_files_txt_path}")

        # Fechar o aplicativo
        self.root.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="plastik")
    root.withdraw()

    # Mostrar a SplashScreen antes de iniciar a aplicação principal
    if getattr(sys, 'frozen', False):
        splash_screen_path = os.path.join(os.path.dirname(sys.executable), '_internal/imagens/splash_screen.png')
    else:
        splash_screen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imagens/splash_screen.png')

    splash = SplashScreen(root, splash_screen_path, 3000)
    splash.show()

    # Esperar o tempo da SplashScreen antes de iniciar a aplicação principal
    root.after(3000, lambda: (root.deiconify(), FileOrganizerApp(root)))
    root.mainloop()
