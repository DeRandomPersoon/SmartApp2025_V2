import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class NotepadPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.filename = os.path.abspath("notes.txt")

        #layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.text = tk.Text(self, wrap="word")
        self.text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, pady=(0,10))

        ttk.Button(btn_frame, text="Open...", command=self.open_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Save As...", command=self.save_as).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)

        #load excisting file
        if os.path.exists(self.filename):
            self.load(self.filename)

    def load(self, path):
        """Load file into text box."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file:\n{e}")
            return
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.filename = path

    def open_file(self):
        """Select and load a .txt file."""
        path = filedialog.askopenfilename(filetypes=[("Text Files","*.txt"), ("All Files","*.*")])
        if path:
            self.load(path)

    def save(self):
        """Save current text to current filename."""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                text = self.text.get("1.0", tk.END)
                f.write(text)
            messagebox.showinfo("Saved", f"Saved to {os.path.basename(self.filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file:\n{e}")

    def save_as(self):
        """Save to a new file selected by user."""
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files","*.txt"), ("All Files","*.*")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    text = self.text.get("1.0", tk.END)
                    f.write(text)
                messagebox.showinfo("Saved", f"Saved to {os.path.basename(path)}")
                self.filename = path
            except Exception as e:
                messagebox.showerror("Error", f"Cannot save file:\n{e}")

    def clear(self):
        """Clear the text box."""
        self.text.delete("1.0", tk.END)
