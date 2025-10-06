from tkinter import ttk


class NotepadPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Notepad (Coming soon)", font=("Arial", 16)).pack(pady=20)
