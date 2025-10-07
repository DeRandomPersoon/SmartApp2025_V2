import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class SmartControllerPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # === Layout Frames ===
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # === Left Side: Preview Area ===
        preview_frame = ttk.Frame(self)
        preview_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(preview_frame, text="File Preview", font=("Arial", 14, "bold")).pack(pady=(0, 5))

        self.preview_box = tk.Text(preview_frame, wrap="none", height=25, width=80, state="disabled")
        self.preview_box.pack(fill="both", expand=True)

        toggle_frame = ttk.Frame(preview_frame)
        toggle_frame.pack(pady=5)

        self.view_mode = tk.StringVar(value="input")
        ttk.Button(toggle_frame, text="Show Input", command=lambda: self.switch_preview("input")).pack(side="left", padx=5)
        ttk.Button(toggle_frame, text="Show Output", command=lambda: self.switch_preview("output")).pack(side="left", padx=5)

        # === Right Side: Controls ===
        control_frame = ttk.Frame(self)
        control_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

        ttk.Label(control_frame, text="Smart Controller", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        ttk.Button(control_frame, text="Select Input File", command=self.select_input, width=20).pack(pady=5, ipady=5)
        ttk.Button(control_frame, text="Create New Input", command=self.create_input_file, width=20).pack(pady=5, ipady=5)
        ttk.Button(control_frame, text="Auto Calculate", command=self.auto_calc, width=20).pack(pady=5, ipady=5)
        ttk.Button(control_frame, text="Overwrite Value", command=self.overwrite, width=20).pack(pady=5, ipady=5)
        ttk.Button(control_frame, text="Download Output", command=self.download_output, width=20).pack(pady=5, ipady=5)

        # === File Setup ===
        self.input_file = "smart_input.txt"
        self.output_file = "smart_output.txt"
        self.ensure_input_exists()
        self.refresh_preview()

    # === UI / File Handling ===
    def ensure_input_exists(self):
        """Ensure a default input file exists."""
        if not os.path.exists(self.input_file):
            with open(self.input_file, "w") as f:
                f.write("date numPeople tempSetpoint tempOutside precip\n")
                f.write("05-10-2024 2 19 8 7\n06-10-2024 2 19 8 7\n")

    def select_input(self):
        """Let user select an existing input file."""
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            self.input_file = file
            messagebox.showinfo("File Selected", f"Using {os.path.basename(self.input_file)}")
            self.refresh_preview()

    def create_input_file(self):
        """Create new input file and select it."""
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, "w") as f:
                f.write("date numPeople tempSetpoint tempOutside precip\n")
            self.input_file = file
            messagebox.showinfo("Created", f"New input file created:\n{os.path.basename(file)}")
            self.refresh_preview()

    def auto_calc(self):
        """Calculate actuator values from input to output."""
        try:
            auto_bereken(self.input_file, self.output_file)
            messagebox.showinfo("Done", f"Actuators written to {os.path.basename(self.output_file)}")
            self.refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate:\n{e}")

    def overwrite(self):
        """Open dialog to overwrite an actuator value."""
        if not os.path.exists(self.output_file):
            messagebox.showerror("Error", "No output file found. Run Auto Calc first.")
            return

        with open(self.output_file, "r") as f:
            dates = [line.split(";")[0] for line in f]

        top = tk.Toplevel(self)
        top.title("Overwrite Settings")
        top.geometry("300x250")

        ttk.Label(top, text="Select Date:").pack(pady=5)
        date_var = tk.StringVar(value=dates[0])
        ttk.Combobox(top, textvariable=date_var, values=dates, state="readonly").pack(pady=5)

        ttk.Label(top, text="Select System:").pack(pady=5)
        sys_var = tk.StringVar(value="1")
        ttk.Combobox(top, textvariable=sys_var, values=["1: CV", "2: Vent", "3: Water"], state="readonly").pack(pady=5)

        ttk.Label(top, text="New Value:").pack(pady=5)
        val_entry = ttk.Entry(top)
        val_entry.pack(pady=5)

        def confirm():
            result = overwrite_settings(self.output_file, date_var.get(), sys_var.get()[0], val_entry.get().strip())
            if result == 0:
                messagebox.showinfo("Success", "Value overwritten.")
                self.refresh_preview()
                top.destroy()
            elif result == -1:
                messagebox.showerror("Error", "Date not found.")
            else:
                messagebox.showerror("Error", "Invalid system or value.")

        ttk.Button(top, text="Confirm", command=confirm).pack(pady=10)

    def download_output(self):
        """Save output file to user-selected location."""
        if not os.path.exists(self.output_file):
            messagebox.showerror("Error", "No output file to download.")
            return
        dest = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if dest:
            with open(self.output_file, "r") as src, open(dest, "w") as dst:
                dst.write(src.read())
            messagebox.showinfo("Downloaded", f"File saved to:\n{dest}")

    def switch_preview(self, mode):
        """Switch between input and output preview."""
        self.view_mode.set(mode)
        self.refresh_preview()

    def refresh_preview(self):
        """Update the preview box based on selected mode."""
        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)

        file = self.input_file if self.view_mode.get() == "input" else self.output_file
        if not os.path.exists(file):
            msg = "No file selected. Please select or create an input file."
            self.preview_box.insert("1.0", msg)
        else:
            with open(file, "r") as f:
                self.preview_box.insert("1.0", f.read())

        self.preview_box.config(state="disabled")


# === Core Smart App Logic ===
def aantal_dagen(inputFile):
    """Return number of days in input file."""
    with open(inputFile, "r") as f:
        return len(f.readlines()[1:])

def auto_bereken(inputFile, outputFile):
    """Calculate actuator values and write to output file."""
    with open(inputFile, "r") as f:
        lines = f.readlines()[1:]

    results = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 5:
            continue
        date, numPeople, setTemp, outTemp, precip = parts
        numPeople, setTemp, outTemp, precip = int(numPeople), float(setTemp), float(outTemp), float(precip)
        diff = setTemp - outTemp
        cv = 100 if diff >= 20 else 50 if diff >= 10 else 0
        vent = min(numPeople + 1, 4)
        water = "True" if precip < 3 else "False"
        results.append(f"{date};{cv};{vent};{water}")

    with open(outputFile, "w") as f:
        f.write("\n".join(results))

def overwrite_settings(outputFile, date, system, new_value):
    """Update output file with new actuator setting."""
    if not os.path.exists(outputFile):
        return -1

    with open(outputFile, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

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
