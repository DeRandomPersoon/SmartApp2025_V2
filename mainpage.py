from tkinter import ttk


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Smart App - Main Menu", font=("Arial", 18)).pack(pady=20)

        ttk.Button(self, text="Weerstation", command=lambda: controller.show_frame("WeerstationPage")).pack(pady=5)
        ttk.Button(self, text="Smart Controller", command=lambda: controller.show_frame("SmartControllerPage")).pack(pady=5)
        ttk.Button(self, text="Notepad", command=lambda: controller.show_frame("NotepadPage")).pack(pady=5)
