import tkinter as tk
from ttkthemes import ThemedTk
from file_organizer_app import FileOrganizerApp

if __name__ == "__main__":
    root = ThemedTk(theme="blue")  # Escolha um tema moderno, como "arc"
    app = FileOrganizerApp(root)
    root.mainloop()
