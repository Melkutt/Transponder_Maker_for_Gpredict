# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 21:01:28 2026

GitHub: https://github.com/Melkutt/Transponder_Maker_for_Gpredict
Credit to https://www.flaticon.com/free-icon/satellite-tv_88136 for the satelltite dish logo

@author: Melker
"""


import os
import tkinter as tk
from tkinter import messagebox, filedialog
import webbrowser
import sys

def resource_path(relative_path):
    
    
    # --- Saves the image as a temporary file ---
    
    try:
        # --- PyInstaller creates a temporary folder _MEIPASS ---
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class TrspGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Satellite Transponder Maker v1.3")
        self.root.geometry("450x850")
        
        self.blocks = []
        
        
        # --- Icon ---

        try:
            icon_path = resource_path("satellite-dish.png")
            icon = tk.PhotoImage(file=icon_path)
            self.root.iconphoto(False, icon)
        except Exception:
            pass

        
        # --- Base colors for Dark Mode (Default)
        
        self.dark_bg = "#1e1e1e"
        self.dark_entry = "#333333"
        self.dark_fg = "#ffffff"
        
        self.root.configure(bg=self.dark_bg)


        # --- Satellite Info ---

        tk.Label(root, text="SATELLITE INFO", font=("Arial", 10, "bold"), bg=self.dark_bg, fg=self.dark_fg).pack(pady=5)
        
        frame_norad = tk.Frame(root, bg=self.dark_bg)
        frame_norad.pack(fill="x", padx=20)
        tk.Label(frame_norad, text="NORAD ID:", width=18, anchor="w", bg=self.dark_bg, fg=self.dark_fg).pack(side="left")
        self.entry_norad = tk.Entry(frame_norad, bg=self.dark_entry, fg="white", insertbackground="white")
        self.entry_norad.pack(side="right", expand=True, fill="x")
        self.entry_norad.bind("<KeyRelease>", lambda e: self.validate_all())

        tk.Frame(root, height=2, bd=0, bg="#444444").pack(fill="x", padx=10, pady=10)


        # --- Transponder Data ---

        tk.Label(root, text="ADD TRANSPONDER BLOCK", font=("Arial", 10, "bold"), bg=self.dark_bg, fg=self.dark_fg).pack(pady=5)

        self.inputs = {}
        self.create_input_fields()
   
        
        # --- Checkboxar ---
        
        self.var_invert = tk.BooleanVar()
        frame_inv = tk.Frame(root, bg=self.dark_bg)
        frame_inv.pack(fill="x", padx=20, pady=2)
        tk.Label(frame_inv, text="Inverting Transponder:", width=18, anchor="w", bg=self.dark_bg, fg=self.dark_fg).pack(side="left")
        self.cb_inv = tk.Checkbutton(frame_inv, variable=self.var_invert, bg=self.dark_bg, activebackground=self.dark_bg, selectcolor="#444444")
        self.cb_inv.pack(side="left")
        
        self.var_readonly = tk.BooleanVar(value=True)
        frame_ro = tk.Frame(root, bg=self.dark_bg)
        frame_ro.pack(fill="x", padx=20, pady=2)
        tk.Label(frame_ro, text="Set File Read-Only:", width=18, anchor="w", bg=self.dark_bg, fg=self.dark_fg).pack(side="left")
        self.cb_ro = tk.Checkbutton(frame_ro, variable=self.var_readonly, bg=self.dark_bg, activebackground=self.dark_bg, selectcolor="#444444")
        self.cb_ro.pack(side="left")

        self.var_lightmode = tk.BooleanVar(value=False)
        frame_light = tk.Frame(root, bg=self.dark_bg)
        frame_light.pack(fill="x", padx=20, pady=2)
        tk.Label(frame_light, text="Light Mode:", width=18, anchor="w", bg=self.dark_bg, fg=self.dark_fg).pack(side="left")
        self.cb_light = tk.Checkbutton(frame_light, variable=self.var_lightmode, command=self.toggle_theme, bg=self.dark_bg, activebackground=self.dark_bg, selectcolor="#444444")
        self.cb_light.pack(side="left")


        # --- Buttons---

        btn_frame = tk.Frame(root, bg=self.dark_bg)
        btn_frame.pack(pady=10)
        self.btn_add = tk.Button(btn_frame, text="Add This Block", command=self.add_block, bg="#1976D2", fg="white", state="disabled", width=15)
        self.btn_add.pack(side="left", padx=5)
        self.btn_clear = tk.Button(btn_frame, text="Clear Block Fields", command=self.clear_fields, width=15, bg="#444444", fg="white")
        self.btn_clear.pack(side="left", padx=5)


        # --- Preview List ---

        tk.Label(root, text="ADDED BLOCKS PREVIEW:", font=("Arial", 9, "bold"), bg=self.dark_bg, fg=self.dark_fg).pack(pady=(10,0))
        self.listbox = tk.Listbox(root, height=6, bg=self.dark_entry, fg="white", borderwidth=0)
        self.listbox.pack(fill="x", padx=20, pady=5)
        self.btn_del = tk.Button(root, text="Delete Selected Block", command=self.delete_block, bg="#B71C1C", fg="white")
        self.btn_del.pack(pady=5)


        # --- Save ---

        self.btn_save = tk.Button(root, text="SAVE .TRSP FILE", command=self.save_file, bg="#2E7D32", fg="white", font=("Arial", 11, "bold"), height=2)
        self.btn_save.pack(pady=15, padx=20, fill="x")


        # --- Footer ---

        info_frame = tk.Frame(root, bg=self.dark_bg)
        info_frame.pack(side="bottom", fill="x", pady=10)
        tk.Label(info_frame, text="Created by SA1CKW", font=("Arial", 8, "bold"), fg="gray", bg=self.dark_bg).pack()
        link_label = tk.Label(info_frame, text="GitHub link", font=("Arial", 8, "underline"), fg="#64B5F6", bg=self.dark_bg, cursor="hand2")
        link_label.pack()
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Melkutt/Transponder_Maker_for_Gpredict"))

    def get_theme_colors(self):
        is_light = self.var_lightmode.get()
        return {
            "bg": "#F5F5F5" if is_light else self.dark_bg,
            "fg": "black" if is_light else self.dark_fg,
            "entry_bg": "white" if is_light else self.dark_entry,
            "entry_fg": "black" if is_light else "white",
            "error": "#FFCDD2" if is_light else "#B71C1C",
            "select": "#E0E0E0" if is_light else "#444444"
        }

    def toggle_theme(self):
        c = self.get_theme_colors()
        self.root.configure(bg=c["bg"])

        
        # --- Update ALL children in the window recursively ---

        def update_all(parent):
            for w in parent.winfo_children():
                if isinstance(w, (tk.Frame, tk.Label)):
                    w.configure(bg=c["bg"])
                    if isinstance(w, tk.Label) and w.cget("fg") not in ["gray", "#64B5F6", "blue"]:
                        w.configure(fg=c["fg"])
                elif isinstance(w, tk.Entry):
                    w.configure(bg=c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"])
                elif isinstance(w, tk.Checkbutton):
                    w.configure(bg=c["bg"], activebackground=c["bg"], selectcolor=c["select"])
                elif isinstance(w, tk.Listbox):
                    w.configure(bg=c["entry_bg"], fg=c["entry_fg"])
                if w.winfo_children(): update_all(w)
        
        update_all(self.root)
        self.validate_all()

    def create_input_fields(self):
        fields = [
            ("Block Name:", "name", "Unique name"), ("Mode:", "mode", "e.g. FM"),
            ("Downlink Low (Hz):", "d_low", "Numeric"), ("Downlink High (Hz):", "d_high", ">= Low"),
            ("Uplink Low (Hz):", "u_low", "Numeric"), ("Uplink High (Hz):", "u_high", ">= Low"),
            ("BAUD:", "baud", "Numeric (optional)")
        ]
        for text, key, hint in fields:
            f = tk.Frame(self.root, bg=self.dark_bg)
            f.pack(fill="x", padx=20, pady=1)
            tk.Label(f, text=text, width=18, anchor="w", bg=self.dark_bg, fg=self.dark_fg).pack(side="left")
            ent = tk.Entry(f, bg=self.dark_entry, fg="white", insertbackground="white")
            ent.pack(side="right", expand=True, fill="x")
            ent.bind("<KeyRelease>", lambda e: self.validate_all())
            self.inputs[key] = ent
            tk.Label(self.root, text=hint, font=("Arial", 7), fg="gray", bg=self.dark_bg).pack(anchor="e", padx=20)

    def validate_all(self):
        c = self.get_theme_colors()
        errors = False
        
        def set_style(w, is_err):
            w.config(bg=c["error"] if is_err else c["entry_bg"], fg=c["entry_fg"], insertbackground=c["entry_fg"])


        # --- NORAD ID check ---

        v_norad = self.entry_norad.get().strip()
        e_norad = bool(v_norad and not v_norad.isdigit())
        set_style(self.entry_norad, e_norad)
        
        # --- UNIQUE NAME check (Important for Gpredict) ---
        v_name = self.inputs["name"].get().strip()
        # Hämta alla namn som redan finns i listboxen
        existing_names = [self.listbox.get(i).split(' (')[0].strip() for i in range(self.listbox.size())]
        
        name_exists = v_name in existing_names
        name_empty = not v_name
        
        # --- If name exists or is empty = Error ---
        set_style(self.inputs["name"], name_exists or name_empty)
        if name_exists:
            errors = True

        # ---  Numeric check for frequencies and baud ---
        for k in ["d_low", "d_high", "u_low", "u_high", "baud"]:
            val = self.inputs[k].get().strip()
            err = bool(val and not val.isdigit())
            set_style(self.inputs[k], err)
            if err: errors = True
            
        # --- Logic check (High must not be lower than Low) ---
        try:
            d_low = self.inputs["d_low"].get().strip()
            d_high = self.inputs["d_high"].get().strip()
            if d_low and d_high and int(d_high) < int(d_low):
                set_style(self.inputs["d_high"], True)
                errors = True
        except ValueError:
            pass

        # --- Final check to activate the button ---
        if not v_norad or not v_name or not self.inputs["d_low"].get().strip() or e_norad or name_exists:
            errors = True
        
        self.btn_add.config(state="normal" if not errors else "disabled")


    def add_block(self):
        name = self.inputs["name"].get().strip()
        # ... logic ...
        self.blocks.append(f"[{name}]")
        self.listbox.insert(tk.END, f"{name}")
        self.clear_fields()

    def delete_block(self):
        sel = self.listbox.curselection()
        if sel:
            idx = sel[0]
            self.listbox.delete(idx)
            self.blocks.pop(idx)
            self.validate_all()

    def clear_fields(self):
        for ent in self.inputs.values():
            ent.delete(0, tk.END)
        self.var_invert.set(False)
        self.validate_all()

    def save_file(self):
        if not self.entry_norad.get() or not self.blocks: return
        p = filedialog.asksaveasfilename(defaultextension=".trsp")
        if p:
            with open(p, "w") as f: f.write("\n".join(self.blocks))
            messagebox.showinfo("Done", "File saved!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrspGenerator(root)
    root.mainloop()