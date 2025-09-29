import tkinter as tk
from tkinter import ttk

# Import the pages
from weerstation import WeerstationPage
from smartcontroller import SmartControllerPage
from notepad import NotepadPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart App")
        self.geometry("600x400")

        # Container for pages
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainPage, WeerstationPage, SmartControllerPage, NotepadPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()


class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="Smart App - Main Menu", font=("Arial", 18)).pack(pady=20)

        ttk.Button(self, text="Weerstation", command=lambda: controller.show_frame(WeerstationPage)).pack(pady=5)
        ttk.Button(self, text="Smart Controller", command=lambda: controller.show_frame(SmartControllerPage)).pack(pady=5)
        ttk.Button(self, text="Notepad", command=lambda: controller.show_frame(NotepadPage)).pack(pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
