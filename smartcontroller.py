import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class SmartControllerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # === Scrollable container ===
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # === GUI Buttons ===
        ttk.Label(self.scroll_frame, text="Smart Controller", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Button(self.scroll_frame, text="Select Input", command=self.select_input).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(self.scroll_frame, text="Count Days", command=self.show_days).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(self.scroll_frame, text="Auto Calc", command=self.auto_calc).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(self.scroll_frame, text="Overwrite", command=self.overwrite).pack(pady=5, ipadx=10, ipady=5)
        ttk.Button(self.scroll_frame, text="Preview Output", command=self.preview_file).pack(pady=5, ipadx=10, ipady=5)

        self.input_file = "smart_input.txt"
        self.output_file = "smart_output.txt"

        # Create default input file if missing
        if not os.path.exists(self.input_file):
            with open(self.input_file, "w") as f:
                f.write("date numPeople tempSetpoint tempOutside precip\n")
                f.write("05-10-2024 2 19 8 7\n06-10-2024 2 19 8 7\n")

    # === Tkinter callbacks ===
    def select_input(self):
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            self.input_file = file
            messagebox.showinfo("File Selected", f"Using {self.input_file}")

    def show_days(self):
        try:
            days = aantal_dagen(self.input_file)
            messagebox.showinfo("Days Count", f"{days} days in file.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")

    def auto_calc(self):
        try:
            auto_bereken(self.input_file, self.output_file)
            messagebox.showinfo("Done", f"Actuators written to {self.output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate:\n{e}")

    def overwrite(self):
        if not os.path.exists(self.output_file):
            messagebox.showerror("Error", "No output file found. Run Auto Calc first.")
            return

        # Load available dates from output file
        with open(self.output_file, "r") as f:
            dates = [line.split(";")[0] for line in f]

        # === Overwrite dialog ===
        top = tk.Toplevel(self)
        top.title("Overwrite Settings")
        top.geometry("300x250")

        ttk.Label(top, text="Select Date:").pack(pady=5)
        date_var = tk.StringVar(value=dates[0])
        date_menu = ttk.Combobox(top, textvariable=date_var, values=dates, state="readonly")
        date_menu.pack(pady=5)

        ttk.Label(top, text="Select System:").pack(pady=5)
        sys_var = tk.StringVar(value="1")
        sys_menu = ttk.Combobox(top, textvariable=sys_var, values=["1: CV", "2: Vent", "3: Water"], state="readonly")
        sys_menu.pack(pady=5)

        ttk.Label(top, text="New Value:").pack(pady=5)
        val_entry = ttk.Entry(top)
        val_entry.pack(pady=5)

        def confirm():
            system = sys_var.get()[0]  # only first char (1/2/3)
            value = val_entry.get().strip()
            result = overwrite_settings(self.output_file, date_var.get(), system, value)
            if result == 0:
                messagebox.showinfo("Success", "Value overwritten.")
                top.destroy()
            elif result == -1:
                messagebox.showerror("Error", "Date not found.")
            else:
                messagebox.showerror("Error", "Invalid system or value.")

        ttk.Button(top, text="Confirm", command=confirm).pack(pady=10)

    def preview_file(self):
        if not os.path.exists(self.output_file):
            messagebox.showinfo("Preview", "No output file yet.")
            return
        with open(self.output_file, "r") as f:
            content = f.read()
        top = tk.Toplevel(self)
        top.title("Output Preview")
        txt = tk.Text(top, wrap="none", width=60, height=20)
        txt.insert("1.0", content)
        txt.pack(fill="both", expand=True)


# === Core functions ===
def aantal_dagen(inputFile):
    """Return number of days in input file."""
    with open(inputFile, "r") as f:
        lines = f.readlines()[1:]
    return len(lines)


def auto_bereken(inputFile, outputFile):
    """Calculate actuators and write to output file."""
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
    """Update output file with a new value for a system."""
    if not os.path.exists(outputFile):
        return -1

    with open(outputFile, "r") as f:
        lines = [line.strip() for line in f]

    updated = False
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
            updated = True
            break

    if not updated:
        return -1

    with open(outputFile, "w") as f:
        f.write("\n".join(lines))
    return 0
