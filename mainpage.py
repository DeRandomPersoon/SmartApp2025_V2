import tkinter as tk
from tkinter import ttk
from weerstation import WeerstationPage
from smartcontroller import SmartControllerPage
from notepad import NotepadPage
from weatherpage import WeatherPage

class MainPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        #Grid
        self.columnconfigure((0,1), weight=1, uniform="col")
        self.rowconfigure((0,1), weight=1, uniform="row")

        #Texts for grid
        self._make_tile(0, 0, "Weerstation", "Voer weerdata in", lambda: controller.show_frame("WeerstationPage"), "#AED6F1")
        self._make_tile(0, 1, "SmartCtrl", "Slimme actuatoren", lambda: controller.show_frame("SmartControllerPage"), "#A9DFBF")
        self._make_tile(1, 0, "Notepad", "Maak notities", lambda: controller.show_frame("NotepadPage"), "#F9E79F")
        self._make_tile(1, 1, "Weer live", "Actueel weer via API", lambda: controller.show_frame("WeatherPage"), "#F5B7B1")

    def _make_tile(self, r, c, title, subtitle, command, color):
        frame = ttk.Frame(self, borderwidth=2, relief="ridge")
        frame.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        #Colours <3
        label_bg = tk.Label(frame, bg=color)
        label_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        lbl_title = ttk.Label(frame, text=title, font=("Arial", 14, "bold"))
        lbl_title.place(relx=0.5, rely=0.3, anchor="center")
        lbl_sub = ttk.Label(frame, text=subtitle, font=("Arial", 10))
        lbl_sub.place(relx=0.5, rely=0.6, anchor="center")

        #Make them clickable
        frame.bind("<Button-1>", lambda e: command())
        lbl_title.bind("<Button-1>", lambda e: command())
        lbl_sub.bind("<Button-1>", lambda e: command())
