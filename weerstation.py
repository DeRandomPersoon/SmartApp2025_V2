import tkinter as tk
from tkinter import ttk, messagebox

def fahrenheit(temp_celsius: float) -> float:
    return 32 + 1.8 * temp_celsius

def gevoelstemperatuur(temp_celsius: float, windsnelheid: float, luchtvochtigheid: float) -> float:
    return temp_celsius - (luchtvochtigheid / 100) * windsnelheid

def weerrapport(temp_celsius: float, windsnelheid: float, luchtvochtigheid: float) -> str:
    gevoel = gevoelstemperatuur(temp_celsius, windsnelheid, luchtvochtigheid)

    if gevoel < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming helemaal aan!"
    elif gevoel < 0 and windsnelheid <= 10:
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"
    elif 0 <= gevoel < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; verwarming aan en roosters dicht!"
    elif 0 <= gevoel < 10 and windsnelheid <= 12:
        return "Het is een beetje koud, elektrische kachel op de benedenverdieping aan!"
    elif 10 <= gevoel < 22:
        return "Heerlijk weer, niet te koud of te warm."
    else:
        return "Warm! Airco aan!"

class WeerstationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.day = 0
        self.temperatures = []

        ttk.Label(self, text="Weerstation", font=("Arial", 16)).pack(pady=10)

        self.temp_var = tk.StringVar()
        self.wind_var = tk.StringVar()
        self.humidity_var = tk.StringVar()

        form = ttk.Frame(self)
        form.pack(pady=10)

        ttk.Label(form, text="Temperatuur (°C):").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.temp_var).grid(row=0, column=1)

        ttk.Label(form, text="Windsnelheid (m/s):").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.wind_var).grid(row=1, column=1)

        ttk.Label(form, text="Luchtvochtigheid (%):").grid(row=2, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.humidity_var).grid(row=2, column=1)

        ttk.Button(self, text="Voer dag in", command=self.process_day).pack(pady=10)

        self.output = tk.Text(self, height=10, width=70)
        self.output.pack(pady=10)

    def process_day(self):
        if self.day >= 7:
            messagebox.showinfo("Weerstation", "Maximaal 7 dagen ingevoerd.")
            return

        try:
            temp_c = float(self.temp_var.get())
            wind = float(self.wind_var.get())
            humidity = int(self.humidity_var.get())

            if not (0 <= humidity <= 100):
                raise ValueError("Humidity moet tussen 0 en 100 liggen")

        except ValueError as e:
            messagebox.showerror("Foutieve invoer", str(e))
            return

        self.day += 1
        self.temperatures.append(temp_c)

        temp_f = fahrenheit(temp_c)
        report = weerrapport(temp_c, wind, humidity)
        avg_temp = sum(self.temperatures) / len(self.temperatures)

        self.output.insert(tk.END, f"Dag {self.day}\n")
        self.output.insert(tk.END, f"Temperatuur: {temp_c:.1f}°C ({temp_f:.1f}°F)\n")
        self.output.insert(tk.END, f"Weerrapport: {report}\n")
        self.output.insert(tk.END, f"Gemiddelde temperatuur tot nu toe: {avg_temp:.1f}°C\n")
        self.output.insert(tk.END, "======================================\n")

        self.temp_var.set("")
        self.wind_var.set("")
        self.humidity_var.set("")
