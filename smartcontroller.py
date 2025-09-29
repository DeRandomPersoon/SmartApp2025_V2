from tkinter import ttk


class SmartControllerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Smart Controller (Coming soon)", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Terug naar menu", command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)
