import tkinter as tk
from tkinter import ttk
from mainpage import MainPage
from weerstation import WeerstationPage
from smartcontroller import SmartControllerPage
from notepad import NotepadPage
from weatherpage import WeatherPage 

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart App")
        self.geometry("900x600")
        self.minsize(800, 500)

        #Navbar
        navbar = ttk.Frame(self)
        navbar.grid(row=0, column=0, columnspan=5, sticky="ew")
        navbar.columnconfigure((0, 1, 2, 3, 4), weight=1)

        #Buttons in navbar
        ttk.Button(navbar, text="Hoofdmenu", command=lambda: self.show_frame("MainPage")).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(navbar, text="Weerstation", command=lambda: self.show_frame("WeerstationPage")).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(navbar, text="SmartCtrl", command=lambda: self.show_frame("SmartControllerPage")).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        ttk.Button(navbar, text="Notepad", command=lambda: self.show_frame("NotepadPage")).grid(row=0, column=3, sticky="ew", padx=2, pady=2)
        ttk.Button(navbar, text="Weerpagina", command=lambda: self.show_frame("WeatherPage")).grid(row=0, column=4, sticky="ew", padx=2, pady=2)

        #Container
        container = ttk.Frame(self)
        container.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        #Load all pages
        self.frames = {}
        for PageClass in (MainPage, WeerstationPage, SmartControllerPage, NotepadPage, WeatherPage):
            page_name = PageClass.__name__
            frame = PageClass(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Default startup page
        self.show_frame("MainPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
