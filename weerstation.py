import tkinter as tk
from tkinter import ttk, messagebox


#Head functions
def fahrenheit(temp_celsius: float) -> float:
    return 32 + 1.8 * temp_celsius


def gevoelstemperatuur(temp_celsius: float, windsnelheid: float, luchtvochtigheid: float) -> float:
    return temp_celsius - (luchtvochtigheid / 100) * windsnelheid


def weerrapport(temp_celsius: float, windsnelheid: float, luchtvochtigheid: float) -> str:
    gevoel = gevoelstemperatuur(temp_celsius, windsnelheid, luchtvochtigheid)

    if gevoel < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming helemaal aan!"
    elif gevoel < 0:
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"
    elif 0 <= gevoel < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; verwarming aan en roosters dicht!"
    elif 0 <= gevoel < 10:
        return "Het is een beetje koud, elektrische kachel op de benedenverdieping aan!"
    elif 10 <= gevoel < 22:
        return "Heerlijk weer, niet te koud of te warm."
    else:
        return "Warm! Airco aan!"


#Page itself
class WeerstationPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.dag = 0
        self.temperaturen = []

        #Titel
        ttk.Label(self, text="Weerstation", font=("Arial", 16, "bold")).pack(pady=10)

        #Invoer
        form = ttk.Frame(self)
        form.pack(pady=10)

        self.temp_var = tk.StringVar()
        self.wind_var = tk.StringVar()
        self.humidity_var = tk.StringVar()

        ttk.Label(form, text="Temperatuur (°C):").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.temp_var, width=10).grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(form, text="Windsnelheid (m/s):").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.wind_var, width=10).grid(row=1, column=1, padx=5, pady=3)

        ttk.Label(form, text="Luchtvochtigheid (%):").grid(row=2, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(form, textvariable=self.humidity_var, width=10).grid(row=2, column=1, padx=5, pady=3)

        ttk.Button(self, text="Voer dag in", command=self.process_day).pack(pady=10, ipadx=10)

        #Uitvoer
        output_frame = ttk.Frame(self)
        output_frame.pack(pady=10, fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_frame)
        scrollbar.pack(side="right", fill="y")

        self.output = tk.Text(output_frame, wrap="word", height=12, width=70, yscrollcommand=scrollbar.set)
        self.output.pack(fill="both", expand=True)
        scrollbar.config(command=self.output.yview)

        ttk.Label(self, text="Maximaal 7 dagen invoer toegestaan.", font=("Arial", 9, "italic")).pack(pady=(0, 5))

    #verwerking van data
    def process_day(self):
        if self.dag >= 7:
            messagebox.showinfo("Weerstation", "Maximaal 7 dagen ingevoerd.")
            return

        try:
            temp_c = float(self.temp_var.get())
            wind = float(self.wind_var.get())
            humidity = int(self.humidity_var.get())

            if not (0 <= humidity <= 100):
                raise ValueError("Vochtigheid moet tussen 0 en 100 liggen.")
        except ValueError as e:
            messagebox.showerror("Foutieve invoer", str(e))
            return

        self.dag += 1
        self.temperaturen.append(temp_c)

        temp_f = fahrenheit(temp_c)
        report = weerrapport(temp_c, wind, humidity)
        avg_temp = sum(self.temperaturen) / len(self.temperaturen)

        self.output.insert(tk.END, f"Dag {self.dag}\n")
        self.output.insert(tk.END, f"Temperatuur: {temp_c:.1f}°C ({temp_f:.1f}°F)\n")
        self.output.insert(tk.END, f"Weerrapport: {report}\n")
        self.output.insert(tk.END, f"Gemiddelde temperatuur tot nu toe: {avg_temp:.1f}°C\n")
        self.output.insert(tk.END, "--------------------------------------\n\n")

        #empty
        self.temp_var.set("")
        self.wind_var.set("")
        self.humidity_var.set("")
        self.output.see(tk.END)
