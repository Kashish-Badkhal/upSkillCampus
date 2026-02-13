import customtkinter as ctk
from tkinter import messagebox, ttk, Menu
import tkinter as tk
import pyperclip
from src import backend, generator

# --- Professional Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green") 

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("600x520")
        self.root.resizable(False, False)

        # Initialize Database
        backend.init_db()

        self.create_widgets()

    def create_widgets(self):
        # 1. Main Title
        title_label = ctk.CTkLabel(self.root, text="Password Manager", font=("Segoe UI", 24, "bold"), text_color="#E0E0E0")
        title_label.pack(pady=(25, 10))

        # 2. Card Container
        self.container_frame = ctk.CTkFrame(self.root, width=500, fg_color="#2b2b2b", border_width=1, border_color="#3a3a3a", corner_radius=10)
        self.container_frame.pack(pady=20, padx=40, fill="both", expand=False)

        # Card Header
        lbl_title = ctk.CTkLabel(self.container_frame, text="ADD NEW CREDENTIAL", font=("Segoe UI", 12, "bold"), text_color="#888888")
        lbl_title.pack(pady=(15, 20))

        # --- Input Grid ---
        input_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        input_frame.pack(pady=0, padx=20)

        # Website
        ctk.CTkLabel(input_frame, text="Website", font=("Segoe UI", 13), width=80, anchor="w", text_color="#CCCCCC").grid(row=0, column=0, pady=10)
        self.entry_site = ctk.CTkEntry(input_frame, width=240, height=35, placeholder_text="e.g. Netflix", border_color="#555555")
        self.entry_site.grid(row=0, column=1, padx=10, pady=10)

        # Username
        ctk.CTkLabel(input_frame, text="Username", font=("Segoe UI", 13), width=80, anchor="w", text_color="#CCCCCC").grid(row=1, column=0, pady=10)
        self.entry_user = ctk.CTkEntry(input_frame, width=240, height=35, placeholder_text="email@example.com", border_color="#555555")
        self.entry_user.grid(row=1, column=1, padx=10, pady=10)

        # Password
        ctk.CTkLabel(input_frame, text="Password", font=("Segoe UI", 13), width=80, anchor="w", text_color="#CCCCCC").grid(row=2, column=0, pady=10)
        self.entry_pass = ctk.CTkEntry(input_frame, width=240, height=35, show="*", border_color="#555555")
        self.entry_pass.grid(row=2, column=1, padx=10, pady=10)

        # Generate Button
        btn_gen = ctk.CTkButton(input_frame, text="Generate", width=80, height=35, command=self.generate_pass, 
                                fg_color="#444444", hover_color="#555555", font=("Segoe UI", 11))
        btn_gen.grid(row=2, column=2, padx=(5, 0))

        # Save Button
        btn_save = ctk.CTkButton(self.container_frame, text="SAVE PASSWORD", command=self.save_pass, 
                                 width=200, height=40, corner_radius=20,
                                 fg_color="#00C853", hover_color="#009624", 
                                 font=("Segoe UI", 13, "bold"))
        btn_save.pack(pady=(25, 25))

        # 3. View Button
        btn_view = ctk.CTkButton(self.root, text="View & Manage Database", command=self.open_view_window, 
                                 width=250, height=45, corner_radius=8,
                                 fg_color="transparent", border_width=1, border_color="#555555", 
                                 text_color="#E0E0E0", hover_color="#333333")
        btn_view.pack(pady=10)

    # --- Logic Methods ---
    def generate_pass(self):
        pw = generator.generate_strong_password()
        self.entry_pass.delete(0, tk.END)
        self.entry_pass.insert(0, pw)

    def save_pass(self):
        site = self.entry_site.get()
        user = self.entry_user.get()
        password = self.entry_pass.get()

        if not site or not user or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        if backend.add_password(site, user, password):
            self.entry_site.delete(0, tk.END)
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
            messagebox.showinfo("Success", "Credential secured successfully.")
        else:
            messagebox.showerror("System Error", "Database connection failed.")

    # --- VIEW WINDOW (Now with Search) ---
    def open_view_window(self):
        self.view_window = ctk.CTkToplevel(self.root)
        self.view_window.title("Database Records")
        self.view_window.geometry("700x500")
        self.view_window.grab_set()

        # 1. Search Bar Frame (NEW)
        search_frame = ctk.CTkFrame(self.view_window, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(20, 0))

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search website or username...", height=35)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Search Button (Magnifying glass style)
        btn_search = ctk.CTkButton(search_frame, text="Search", width=80, height=35, 
                                   command=self.perform_search, fg_color="#1f538d", hover_color="#14375e")
        btn_search.pack(side="left", padx=(0, 5))

        # Reset Button (To clear search)
        btn_reset = ctk.CTkButton(search_frame, text="✕", width=35, height=35, 
                                  command=self.reset_search, fg_color="#444444", hover_color="#555555")
        btn_reset.pack(side="left")

        # 2. Table Frame
        table_frame = ctk.CTkFrame(self.view_window, fg_color="transparent")
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Style Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#2b2b2b", 
                        foreground="white", 
                        fieldbackground="#2b2b2b", 
                        rowheight=35,
                        borderwidth=0,
                        font=("Segoe UI", 11))
        
        style.map('Treeview', background=[('selected', '#00C853')])
        
        style.configure("Treeview.Heading", 
                        background="#1f1f1f", 
                        foreground="#E0E0E0", 
                        relief="flat",
                        font=("Segoe UI", 11, "bold"))
        
        # Create Table
        cols = ("ID", "Website", "Username", "Password")
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode='browse')
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        
        # Columns
        self.tree.column("ID", width=0, stretch=tk.NO)
        self.tree.column("Website", width=180, anchor="w")
        self.tree.column("Username", width=220, anchor="w")
        self.tree.column("Password", width=180, anchor="w")
        
        self.tree.heading("ID", text="ID")
        self.tree.heading("Website", text="WEBSITE")
        self.tree.heading("Username", text="USERNAME")
        self.tree.heading("Password", text="PASSWORD")
        
        self.tree.pack(fill="both", expand=True)

        # Context Menu
        self.context_menu = Menu(self.view_window, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#00C853")
        self.context_menu.add_command(label="Copy Username", command=self.copy_username)
        self.context_menu.add_command(label="Copy Password", command=self.copy_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Entry", command=self.update_entry_ui)
        self.context_menu.add_command(label="Delete Entry", command=self.delete_entry)

        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # Load all data initially
        self.load_data()

    def perform_search(self):
        query = self.search_entry.get()
        self.load_data(query)

    def reset_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def load_data(self, query=""):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Pass the query to the backend
        data = backend.get_passwords(query) 
        
        for item in data:
            self.tree.insert("", "end", values=item)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def copy_username(self):
        sel = self.tree.selection()
        if sel: pyperclip.copy(self.tree.item(sel[0])['values'][2])

    def copy_password(self):
        sel = self.tree.selection()
        if sel: pyperclip.copy(self.tree.item(sel[0])['values'][3])

    def delete_entry(self):
        sel = self.tree.selection()
        if sel and messagebox.askyesno("Confirm Deletion", "Are you sure you want to permanently delete this record?"):
            backend.delete_password(self.tree.item(sel[0])['values'][0])
            self.load_data()

    def update_entry_ui(self):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel[0])['values']
        pw_id = vals[0]
        
        edit_win = ctk.CTkToplevel(self.root)
        edit_win.title("Edit Credential")
        edit_win.geometry("400x320")
        edit_win.attributes("-topmost", True)
        
        frame = ctk.CTkFrame(edit_win, fg_color="transparent")
        frame.pack(pady=20, padx=20)

        ctk.CTkLabel(frame, text="Website").pack(anchor="w")
        e_site = ctk.CTkEntry(frame, width=300); e_site.pack(pady=(5, 15)); e_site.insert(0, vals[1])
        
        ctk.CTkLabel(frame, text="Username").pack(anchor="w")
        e_user = ctk.CTkEntry(frame, width=300); e_user.pack(pady=(5, 15)); e_user.insert(0, vals[2])
        
        ctk.CTkLabel(frame, text="Password").pack(anchor="w")
        e_pass = ctk.CTkEntry(frame, width=300); e_pass.pack(pady=(5, 15)); e_pass.insert(0, vals[3])
        
        def save():
            backend.update_password(pw_id, e_site.get(), e_user.get(), e_pass.get())
            edit_win.destroy()
            self.load_data()
            
        ctk.CTkButton(edit_win, text="Save Changes", command=save, fg_color="#00C853", hover_color="#009624", width=200).pack(pady=10)