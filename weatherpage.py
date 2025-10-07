import tkinter as tk
from tkinter import ttk, messagebox
import requests

class WeatherPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Layout: at top: location input & button, below: display area
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        input_frame = ttk.Frame(self)
        input_frame.grid(row=0, column=0, pady=10, padx=10)

        ttk.Label(input_frame, text="Plaats of stad:").pack(side="left")
        self.location_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.location_var, width=25).pack(side="left", padx=5)
        ttk.Button(input_frame, text="Zoek", command=self.fetch_weather).pack(side="left")

        self.output = tk.Text(self, wrap="word", state="disabled", height=15)
        self.output.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def fetch_weather(self):
        loc = self.location_var.get().strip()
        if not loc:
            messagebox.showwarning("Input ontbreekt", "Voer een locatie in.")
            return
        try:
            # First, geocoding:
            geourl = f"https://geocoding-api.open-meteo.com/v1/search?name={loc}"
            r = requests.get(geourl, timeout=5)
            r.raise_for_status()
            data = r.json()
            results = data.get("results", [])
            if not results:
                raise ValueError("Locatie niet gevonden")
            place = results[0]
            lat = place["latitude"]
            lon = place["longitude"]
            name = place["name"]

            # Then, weather:
            weather_url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={lat}&longitude={lon}"
                f"&current_weather=true"
            )
            wr = requests.get(weather_url, timeout=5)
            wr.raise_for_status()
            wdata = wr.json().get("current_weather", {})

            msg = f"Actuele weer voor {name}:\n"
            msg += f"Temperatuur: {wdata.get('temperature')} °C\n"
            msg += f"Windsnelheid: {wdata.get('windspeed')} m/s\n"
            # Open-Meteo returns some additional fields, but check keys
            # If humidity is available under "relativehumidity" or similar, include that.

        except Exception as e:
            msg = f"Kon weerdata niet ophalen:\n{e}"

        self.output.configure(state="normal")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, msg)
        self.output.configure(state="disabled")
