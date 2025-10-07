import tkinter as tk
from tkinter import ttk
from mainpage import MainPage
from weerstation import WeerstationPage
from smartcontroller import SmartControllerPage
from notepad import NotepadPage
from weatherpage import WeatherPage  # your new weather page

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart App")
        self.geometry("800x600")

        # Navbar
        navbar = ttk.Frame(self)
        navbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        navbar.columnconfigure((0,1,2,3), weight=1)  # distribute buttons evenly

        btn_main = ttk.Button(navbar, text="Hoofdmenu", command=lambda: self.show_frame("MainPage"))
        btn_main.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        btn_weer = ttk.Button(navbar, text="Weerstation", command=lambda: self.show_frame("WeerstationPage"))
        btn_weer.grid(row=0, column=1, sticky="ew", padx=2, pady=2)

        btn_ctrl = ttk.Button(navbar, text="SmartCtrl", command=lambda: self.show_frame("SmartControllerPage"))
        btn_ctrl.grid(row=0, column=2, sticky="ew", padx=2, pady=2)

        btn_notes = ttk.Button(navbar, text="Notepad", command=lambda: self.show_frame("NotepadPage"))
        btn_notes.grid(row=0, column=3, sticky="ew", padx=2, pady=2)

        # Pages container
        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frames = {}
        for PageClass in (MainPage, WeerstationPage, SmartControllerPage, NotepadPage, WeatherPage):
            page_name = PageClass.__name__
            frame = PageClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
