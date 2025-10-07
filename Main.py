import tkinter as tk
from mainpage import MainPage
from weerstation import WeerstationPage
from smartcontroller import SmartControllerPage
from notepad import NotepadPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart App")
        self.geometry("900x600")

        # === Navigation Bar (always visible) ===
        navbar = tk.Frame(self, bg="#ddd", height=40)
        navbar.pack(side="top", fill="x")

        tk.Button(navbar, text="Main", command=lambda: self.show_frame("MainPage")).pack(side="left", padx=5, pady=5)
        tk.Button(navbar, text="Weerstation", command=lambda: self.show_frame("WeerstationPage")).pack(side="left", padx=5, pady=5)
        tk.Button(navbar, text="SmartCtrl", command=lambda: self.show_frame("SmartControllerPage")).pack(side="left", padx=5, pady=5)
        tk.Button(navbar, text="Notepad", command=lambda: self.show_frame("NotepadPage")).pack(side="left", padx=5, pady=5)

        # === Container for all pages ===
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (MainPage, WeerstationPage, SmartControllerPage, NotepadPage):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
