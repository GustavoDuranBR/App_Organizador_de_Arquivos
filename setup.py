from cx_Freeze import setup, Executable
import os

# Caminho absoluto da pasta de imagens
image_folder = "D:\\PYTHON_PROJETOS\\App_Organizador_de_Arquivos\\imagens"

# Executável
executables = [Executable("file_organizer_app.py", base="Win32GUI")]

# Opções de build
build_options = {
    "packages": ["os", "tkinter", "PIL"],
    "include_files": [
        (image_folder, "imagens")  # Inclua a pasta de imagens
    ],
    "excludes": [],
    "optimize": 2,
}

setup(
    name="Organizador de Arquivos",
    version="2.3",
    description="Programa que organiza suas pastas de maneira fácil e rápida",
    options={"build_exe": build_options},
    executables=executables
)
