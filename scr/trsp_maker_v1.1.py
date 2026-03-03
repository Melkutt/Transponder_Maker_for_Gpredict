# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 19:50:30 2026

@author: Melker
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser

class TrspGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title(" Gpredict .trsp Maker V1.1")
        self.root.geometry("450x820")
        
        self.blocks = []
        self.error_color = "#FFCDD2" 
        self.valid_color = "white"

        # --- Satellite Info ---
        tk.Label(root, text="SATELLITE INFO", font=("Arial", 10, "bold")).pack(pady=5)
        
        frame_norad = tk.Frame(root)
        frame_norad.pack(fill="x", padx=20)
        tk.Label(frame_norad, text="NORAD ID:", width=15, anchor="w").pack(side="left")
        self.entry_norad = tk.Entry(frame_norad)
        self.entry_norad.pack(side="right", expand=True, fill="x")
        self.entry_norad.bind("<KeyRelease>", lambda e: self.validate_all())

        tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=10)

        # --- Transponder Data ---
        tk.Label(root, text="ADD TRANSPONDER BLOCK", font=("Arial", 10, "bold")).pack(pady=5)

        self.inputs = {}
        self.create_input_fields()
        
        self.var_invert = tk.BooleanVar()
        tk.Checkbutton(root, text="Inverting Transponder (INVERT=true)", variable=self.var_invert).pack()

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        self.btn_add = tk.Button(btn_frame, text="Add This Block", command=self.add_block, 
                                 bg="#2196F3", fg="white", state="disabled", width=15)
        self.btn_add.pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear Block Fields", command=self.clear_fields, width=15).pack(side="left", padx=5)

        # --- Preview List ---
        tk.Label(root, text="ADDED BLOCKS PREVIEW:", font=("Arial", 9, "bold")).pack(pady=(10,0))
        self.listbox = tk.Listbox(root, height=6, bg="#F5F5F5")
        self.listbox.pack(fill="x", padx=20, pady=5)
        
        tk.Button(root, text="Delete Selected Block", command=self.delete_block, bg="#F44336", fg="white").pack(pady=5)

        # --- Status and Save ---
        tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=10, pady=10)
        
        self.btn_save = tk.Button(root, text="SAVE .TRSP FILE", command=self.save_file, 
                                  bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), height=2)
        self.btn_save.pack(pady=15, padx=20, fill="x")

        # --- GitHub Link at the bottom ---
        link_label = tk.Label(root, text="Visit GitHub Repository", fg="blue", cursor="hand2", font=("Arial", 8, "underline"))
        link_label.pack(side="bottom", pady=10)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Melkutt/Transponder_Maker_for_Gpredict"))

    def create_input_fields(self):
        fields = [
            ("Block Name:", "name", "Unique name (e.g. FM Voice)"),
            ("Mode:", "mode", "e.g. FM, USB, APT, BPSK"),
            ("Downlink Low (Hz):", "d_low", "Numeric only"),
            ("Downlink High (Hz):", "d_high", ">= Low (leave empty if same)"),
            ("Uplink Low (Hz):", "u_low", "Numeric (0 if none)"),
            ("Uplink High (Hz):", "u_high", ">= Low (0 if none)"),
            ("BAUD:", "baud", "Numeric only (optional)")
        ]
        for text, key, hint in fields:
            f = tk.Frame(self.root)
            f.pack(fill="x", padx=20, pady=1)
            tk.Label(f, text=text, width=18, anchor="w").pack(side="left")
            ent = tk.Entry(f)
            ent.pack(side="right", expand=True, fill="x")
            ent.bind("<KeyRelease>", lambda e: self.validate_all())
            self.inputs[key] = ent
            tk.Label(self.root, text=hint, font=("Arial", 7), fg="gray").pack(anchor="e", padx=20)

    def validate_all(self):
        errors = False
        
        # 1. NORAD ID
        norad_val = self.entry_norad.get().strip()
        if norad_val and not norad_val.isdigit():
            self.entry_norad.config(bg=self.error_color)
            errors = True
        else:
            self.entry_norad.config(bg=self.valid_color)

        # 2. Block name
        current_name = self.inputs["name"].get().strip()
        existing_names = [self.listbox.get(i).split(' (')[0] for i in range(self.listbox.size())]
        
        if current_name in existing_names:
            self.inputs["name"].config(bg=self.error_color)
            errors = True
        else:
            self.inputs["name"].config(bg=self.valid_color)

        # 3. Number check
        num_fields = ["d_low", "d_high", "u_low", "u_high", "baud"]
        for key in num_fields:
            val = self.inputs[key].get().strip()
            if val and not val.isdigit():
                self.inputs[key].config(bg=self.error_color)
                errors = True
            else:
                self.inputs[key].config(bg=self.valid_color)

        # 4. Logic control (High >= Low)
        try:
            d_low_str = self.inputs["d_low"].get().strip()
            d_high_str = self.inputs["d_high"].get().strip()
            if d_low_str and d_high_str and int(d_high_str) < int(d_low_str):
                self.inputs["d_high"].config(bg=self.error_color)
                errors = True
            
            u_low_str = self.inputs["u_low"].get().strip()
            u_high_str = self.inputs["u_high"].get().strip()
            if u_low_str and u_high_str and int(u_high_str) < int(u_low_str):
                self.inputs["u_high"].config(bg=self.error_color)
                errors = True
        except ValueError:
            errors = True

        # 5. Mandatory fields
        if not current_name or not self.inputs["d_low"].get().strip() or not norad_val:
            errors = True
        
        self.btn_add.config(state="normal" if not errors else "disabled")

    def add_block(self):
        name = self.inputs["name"].get().strip()
        block_lines = [f"[{name}]"]
        block_lines.append(f"MODE={self.inputs['mode'].get().strip().upper()}")
        block_lines.append(f"DOWN_LOW={self.inputs['d_low'].get().strip()}")
        
        d_high = self.inputs['d_high'].get().strip() or self.inputs['d_low'].get().strip()
        block_lines.append(f"DOWN_HIGH={d_high}")
        
        u_low = self.inputs['u_low'].get().strip() or "0"
        block_lines.append(f"UP_LOW={u_low}")
        
        u_high = self.inputs['u_high'].get().strip() or u_low
        block_lines.append(f"UP_HIGH={u_high}")
        
        baud = self.inputs['baud'].get().strip()
        if baud:
            block_lines.append(f"BAUD={baud}")
            
        if self.var_invert.get():
            block_lines.append("INVERT=true")
        
        self.blocks.append("\n".join(block_lines))
        self.listbox.insert(tk.END, f"{name} ({self.inputs['mode'].get().strip().upper()})")
        self.clear_fields()

    def delete_block(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            self.blocks.pop(index)
            self.validate_all()

    def clear_fields(self):
        for ent in self.inputs.values():
            ent.delete(0, tk.END)
            ent.config(bg=self.valid_color)
        self.var_invert.set(False)
        self.btn_add.config(state="disabled")

    def save_file(self):
        norad = self.entry_norad.get().strip()
        if not norad or not self.blocks:
            messagebox.showwarning("Error", "Missing NORAD ID or Blocks!")
            return

        full_content = "\n\n".join(self.blocks)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".trsp",
            initialfile=f"{norad}.trsp",
            title="Save File"
        )

        if file_path:
            with open(file_path, "w") as f:
                f.write(full_content)
            messagebox.showinfo("Success", f"File saved with {len(self.blocks)} blocks.")
            
            self.blocks = []
            self.listbox.delete(0, tk.END)
            self.entry_norad.delete(0, tk.END)
            self.clear_fields()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrspGenerator(root)
    root.mainloop()