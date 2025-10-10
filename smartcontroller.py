import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from datetime import datetime


class SmartControllerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.input_file = "smart_input.txt"
        self.output_file = "smart_output.txt"

        # Maak standaard invoerbestand als het nog niet bestaat
        if not os.path.exists(self.input_file):
            with open(self.input_file, "w") as f:
                f.write("date numPeople tempSetpoint tempOutside precip\n")
                f.write("05-10-2024 2 19 8 7\n06-10-2024 2 19 8 7\n")

        # === Layout ===
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Linkerzijde: Voorbeeldvenster
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(left_frame, text="Voorbeeld", font=("Arial", 14, "bold")).pack(pady=5)

        self.preview_text = tk.Text(left_frame, wrap="none", state="disabled", height=25, width=80)
        self.preview_text.pack(fill="both", expand=True, padx=5, pady=5)

        # Schakel tussen invoer en uitvoer voorbeeld
        self.preview_mode = tk.StringVar(value="input")
        switch_frame = ttk.Frame(left_frame)
        switch_frame.pack(pady=5)

        ttk.Radiobutton(switch_frame, text="Invoer", variable=self.preview_mode,
                        value="input", command=self.refresh_preview).pack(side="left", padx=5)
        ttk.Radiobutton(switch_frame, text="Uitvoer", variable=self.preview_mode,
                        value="output", command=self.refresh_preview).pack(side="left", padx=5)

        # Rechterzijde: Knoppen
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        ttk.Label(right_frame, text="Acties", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Button(right_frame, text="Selecteer Invoer", command=self.select_input).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Nieuwe Invoer", command=self.create_new_input).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Aantal Dagen", command=self.show_days).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Auto Bereken", command=self.auto_calc).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Overschrijven", command=self.overwrite).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Add Entry", command=self.add_entry_popup).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(right_frame, text="Exporteren", command=self.export_output).pack(pady=5, ipadx=10, ipady=5)

        self.refresh_preview()

    # === Functies ===
    def refresh_preview(self):
        """Update het voorbeeldvenster afhankelijk van de gekozen modus."""
        file_path = self.input_file if self.preview_mode.get() == "input" else self.output_file
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        if not os.path.exists(file_path):
            msg = "Geen bestand geselecteerd of aanwezig."
        else:
            with open(file_path, "r") as f:
                msg = f.read().strip() or "Bestand is leeg."

        self.preview_text.insert("1.0", msg)
        self.preview_text.configure(state="disabled")

    def select_input(self):
        file = filedialog.askopenfilename(filetypes=[("Tekstbestanden", "*.txt")])
        if file:
            self.input_file = file
            messagebox.showinfo("Bestand geselecteerd", f"Nieuw invoerbestand: {self.input_file}")
            self.refresh_preview()

    def create_new_input(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Tekstbestanden", "*.txt")])
        if file:
            with open(file, "w") as f:
                f.write("date numPeople tempSetpoint tempOutside precip\n")
            self.input_file = file
            messagebox.showinfo("Nieuw Bestand", f"Aangemaakt: {self.input_file}")
            self.refresh_preview()

    def show_days(self):
        try:
            days = aantal_dagen(self.input_file)
            messagebox.showinfo("Aantal dagen", f"{days} dagen gevonden in bestand.")
        except Exception as e:
            messagebox.showerror("Fout", f"Kon bestand niet lezen:\n{e}")

    def auto_calc(self):
        try:
            auto_bereken(self.input_file, self.output_file)
            messagebox.showinfo("Voltooid", f"Resultaten opgeslagen in {self.output_file}")
            self.refresh_preview()
        except Exception as e:
            messagebox.showerror("Fout", f"Berekening mislukt:\n{e}")

    def export_output(self):
        if not os.path.exists(self.output_file):
            messagebox.showerror("Fout", "Geen uitvoerbestand gevonden.")
            return
        target = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Tekstbestanden", "*.txt")])
        if target:
            with open(self.output_file, "r") as src, open(target, "w") as dst:
                dst.write(src.read())
            messagebox.showinfo("Succes", f"Uitvoer opgeslagen naar:\n{target}")

    def overwrite(self):
        if not os.path.exists(self.output_file):
            messagebox.showerror("Fout", "Geen uitvoerbestand aanwezig.")
            return

        with open(self.output_file, "r") as f:
            dates = [line.split(";")[0] for line in f]

        top = tk.Toplevel(self)
        top.title("Waarde Overschrijven")
        top.geometry("300x250")

        ttk.Label(top, text="Selecteer datum:").pack(pady=5)
        date_var = tk.StringVar(value=dates[0])
        ttk.Combobox(top, textvariable=date_var, values=dates, state="readonly").pack(pady=5)

        ttk.Label(top, text="Systeem:").pack(pady=5)
        sys_var = tk.StringVar(value="1")
        ttk.Combobox(top, textvariable=sys_var,
                     values=["1: CV", "2: Ventilatie", "3: Water"],
                     state="readonly").pack(pady=5)

        ttk.Label(top, text="Nieuwe waarde:").pack(pady=5)
        val_entry = ttk.Entry(top)
        val_entry.pack(pady=5)

        def confirm():
            result = overwrite_settings(self.output_file, date_var.get(), sys_var.get()[0], val_entry.get().strip())
            if result == 0:
                messagebox.showinfo("Succes", "Waarde overschreven.")
                top.destroy()
                self.refresh_preview()
            elif result == -1:
                messagebox.showerror("Fout", "Datum niet gevonden.")
            else:
                messagebox.showerror("Fout", "Ongeldige invoer.")

        ttk.Button(top, text="Bevestigen", command=confirm).pack(pady=10)

    def add_entry_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Nieuwe Dag Toevoegen")
        popup.geometry("300x330")

        fields = {
            "Datum (DD-MM-YYYY)": tk.StringVar(),
            "Aantal personen": tk.StringVar(),
            "Setpoint (°C)": tk.StringVar(),
            "Buitentemperatuur (°C)": tk.StringVar(),
            "Neerslag (mm)": tk.StringVar(),
        }

        for i, (label, var) in enumerate(fields.items()):
            ttk.Label(popup, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ttk.Entry(popup, textvariable=var).grid(row=i, column=1, padx=10, pady=5)

        def confirm_add():
            date = fields["Datum (DD-MM-YYYY)"].get().strip()
            try:
                datetime.strptime(date, "%d-%m-%Y")
                num_people = int(fields["Aantal personen"].get())
                setpoint = float(fields["Setpoint (°C)"].get())
                outside = float(fields["Buitentemperatuur (°C)"].get())
                precip = float(fields["Neerslag (mm)"].get())
            except ValueError:
                messagebox.showerror("Fout", "Controleer of alle velden correct zijn ingevuld.")
                return

            if not os.path.exists(self.input_file):
                with open(self.input_file, "w") as f:
                    f.write("date numPeople tempSetpoint tempOutside precip\n")

            with open(self.input_file, "r") as f:
                lines = f.readlines()

            data_lines = [line for line in lines[1:] if line.strip()]
            if any(line.startswith(date) for line in data_lines):
                messagebox.showerror("Fout", "Datum bestaat al in bestand.")
                return

            data_lines.append(f"{date} {num_people} {setpoint} {outside} {precip}\n")

            # Sorteer op datum
            data_lines.sort(key=lambda x: datetime.strptime(x.split()[0], "%d-%m-%Y"))

            with open(self.input_file, "w") as f:
                f.write(lines[0])  # header
                f.writelines(data_lines)

            messagebox.showinfo("Succes", "Nieuwe dag toegevoegd.")
            popup.destroy()
            self.refresh_preview()

        ttk.Button(popup, text="Add Entry", command=confirm_add).grid(row=len(fields), column=0, columnspan=2, pady=15)


# === Functies ===
def aantal_dagen(inputFile):
    with open(inputFile, "r") as f:
        return len(f.readlines()[1:])


def auto_bereken(inputFile, outputFile):
    with open(inputFile, "r") as f:
        lines = f.readlines()[1:]

    results = []
    for line in lines:
        date, numPeople, setTemp, outTemp, precip = line.strip().split()
        numPeople, setTemp, outTemp, precip = int(numPeople), float(setTemp), float(outTemp), float(precip)
        diff = setTemp - outTemp
        cv = 100 if diff >= 20 else 50 if diff >= 10 else 0
        vent = min(numPeople + 1, 4)
        water = "True" if precip < 3 else "False"
        results.append(f"{date};{cv};{vent};{water}")

    with open(outputFile, "w") as f:
        f.write("\n".join(results))


def overwrite_settings(outputFile, date, system, new_value):
    if not os.path.exists(outputFile):
        return -1

    with open(outputFile, "r") as f:
        lines = [line.strip() for line in f]

    for i, line in enumerate(lines):
        parts = line.split(";")
        if parts[0] == date:
            if system == "1" and new_value.isdigit() and 0 <= int(new_value) <= 100:
                parts[1] = new_value
            elif system == "2" and new_value.isdigit() and 0 <= int(new_value) <= 4:
                parts[2] = new_value
            elif system == "3" and new_value in ["0", "1"]:
                parts[3] = "True" if new_value == "1" else "False"
            else:
                return -3
            lines[i] = ";".join(parts)
            break
    else:
        return -1

    with open(outputFile, "w") as f:
        f.write("\n".join(lines))
    return 0
