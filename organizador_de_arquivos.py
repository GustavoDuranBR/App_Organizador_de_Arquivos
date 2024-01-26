import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer")

        # Configurar a largura e altura da janela
        self.root.geometry("450x520")

        # Variáveis
        self.selected_file_type = tk.StringVar()
        self.name_part_var = tk.StringVar()
        self.source_folder_var = tk.StringVar()
        self.destination_folder_var = tk.StringVar()

        # Interface
        self.create_widgets()

    def create_widgets(self):
        # Tipo de arquivo
        file_type_label = tk.Label(self.root, text="Tipo de Arquivo:")
        file_type_label.pack(pady=2)

        # Lista de opções para a caixa de seleção
        file_type_options = ["", "docx", "dwg", "exe", "html", "jpg", "json",
                             "mp3", "mp4", "pdf", "png", "txt", "xlsx", "xml", "zip"]

        # Variável para armazenar a opção selecionada
        file_type_combobox = ttk.Combobox(self.root, textvariable=self.selected_file_type, values=file_type_options)
        file_type_combobox.pack(pady=2)

        # Chame o método organize_files ao pressionar Enter na caixa de seleção
        file_type_combobox.bind("<Return>", lambda event: self.organize_files())

        # Parte do nome
        name_part_label = tk.Label(self.root, text="Parte do Nome:")
        name_part_label.pack(pady=2)
        name_part_entry = tk.Entry(self.root, textvariable=self.name_part_var)
        name_part_entry.pack(pady=2)

        # Pasta de origem
        source_folder_label = tk.Label(self.root, text="Pasta de Origem:")
        source_folder_label.pack(pady=2)
        source_folder_entry = tk.Entry(self.root, textvariable=self.source_folder_var)
        source_folder_entry.pack(pady=2)
        source_folder_button = tk.Button(self.root, text="Selecionar Pasta", command=self.browse_source_folder)
        source_folder_button.pack(pady=2)

        # Pasta de destino
        dest_folder_label = tk.Label(self.root, text="Pasta de Destino:")
        dest_folder_label.pack(pady=2)
        dest_folder_entry = tk.Entry(self.root, textvariable=self.destination_folder_var)
        dest_folder_entry.pack(pady=2)
        dest_folder_button = tk.Button(self.root, text="Selecionar Pasta", command=self.browse_destination_folder)
        dest_folder_button.pack(pady=5)

        # Botão de organização
        organize_button = tk.Button(self.root, text="Organizar", command=self.organize_files)
        organize_button.pack(pady=10)

        # Doação com QR code
        donation_label = tk.Label(self.root, text="Donation:")
        donation_label.pack(pady=2)

        # Adicione o caminho da imagem do QR code aqui
        qr_code_path = "NuBank2.png"
        self.qr_code_photo = self.resize_qr_code(qr_code_path)

        qr_code_canvas = tk.Canvas(self.root, width=100, height=100)
        qr_code_canvas.create_image(0, 0, anchor=tk.NW, image=self.qr_code_photo)
        qr_code_canvas.pack(pady=10)

        # Rodapé
        footer_label = tk.Label(self.root, text="Developed by: Gustavo Duran - Version: 1.0")
        footer_label.pack(side="bottom", pady=10)

    def resize_qr_code(self, qr_code_path):
        # Redimensiona o QR code para caber dentro do Canvas
        max_width = 100
        max_height = 100

        qr_code_image = Image.open(qr_code_path)
        width, height = qr_code_image.size

        # Calcula a proporção para manter a relação de aspecto
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)

        # Redimensiona a imagem
        qr_code_image = qr_code_image.resize((new_width, new_height), Image.LANCZOS)

        # Converte a imagem redimensionada para PhotoImage
        return ImageTk.PhotoImage(qr_code_image)

    def browse_source_folder(self):
        folder_selected = filedialog.askdirectory()
        self.source_folder_var.set(folder_selected)

    def browse_destination_folder(self):
        folder_selected = filedialog.askdirectory()
        self.destination_folder_var.set(folder_selected)

    def organize_files(self):
        file_type = self.selected_file_type.get()
        name_part = self.name_part_var.get()
        source_folder = self.source_folder_var.get()
        dest_folder = self.destination_folder_var.get()

        if not file_type and not name_part:
            # Se nenhum tipo de arquivo e parte do nome foram especificados,
            # exiba uma mensagem de erro
            tk.messagebox.showerror("Erro", "Especifique pelo menos o tipo de arquivo ou a parte do nome.")
            return

        if not file_type:
            # Se o campo tipo de arquivo estiver vazio, organize todos os arquivos na pasta de origem
            dest_folder = os.path.join(dest_folder, f"Organizado_{name_part}")
            os.makedirs(dest_folder, exist_ok=True)

            # Verifique se pelo menos um arquivo corresponde à parte do nome fornecida
            files_to_organize = [filename for filename in os.listdir(source_folder) if name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso", f"Nenhum arquivo encontrado com a parte do nome '{name_part}'. Verifique o nome e tente novamente.")
                return
        else:
            if not name_part and file_type != "Organizado":
                # Se o campo tipo de arquivo não estiver vazio, mas a parte do nome estiver vazia,
                # exiba uma mensagem de erro
                tk.messagebox.showerror("Erro", "Preencha o campo 'Parte do Nome'.")
                return

            # Se tudo estiver correto, organize os arquivos com base no tipo de arquivo especificado
            dest_folder = os.path.join(dest_folder, f"{name_part}_{file_type}")
            os.makedirs(dest_folder, exist_ok=True)

            # Filtra os arquivos na pasta de origem com base no tipo de arquivo
            files_to_organize = [filename for filename in os.listdir(source_folder) if file_type in filename and name_part in filename]

            if not files_to_organize:
                tk.messagebox.showwarning("Aviso", f"Nenhum arquivo encontrado com a parte do nome '{name_part}' e tipo de arquivo '{file_type}'. Verifique os campos e tente novamente.")
                return

        # Organiza os arquivos selecionados
        for filename in files_to_organize:
            source_path = os.path.join(source_folder, filename)
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy2(source_path, dest_path)

        tk.messagebox.showinfo("Concluído", "Arquivos organizados com sucesso.")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()

