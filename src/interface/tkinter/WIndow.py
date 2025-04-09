import re
import tkinter as tk
from tkinter import ttk, messagebox
import os
from core import *

class Window(tk.Tk):
    # Style constants
    BG_LIGHT_BLUE = "#8D99AE"
    BG_DARK_BLUE = "#2B2D42"
    BG_WHITE = "white"
    TEXT_WHITE = "white"
    TEXT_BLACK = "black"
    FONT_SIZE = 18
    PADDING = 5

    def __init__(self):
        super().__init__()
        self.title("PyBoxe")
        self.minsize(700, 600)
        self.configure(bg="#555555")
        
        # Set icon if exists
        if os.path.exists("../assets/boxe.ico"):
            self.iconbitmap("../assets/boxe.ico")

        # Managers
        self.network = Network()

        # UI Elements (initialized as None)
        self.weights_box = None
        self.min_input = None
        self.max_input = None
        self.committees_box = None
        self.qualifications_box = None
        self.filename_input = None
        self.combobox_container = None
        self.weights_label = None

        self.init_ui()

    def create_match_input(self, parent, label_text):
        """
        Creates a horizontal frame with a label and an input field for match counts.
        """
        frame = tk.Frame(parent, bg=self.BG_LIGHT_BLUE, padx=5, pady=5, height=60)
        frame.pack_propagate(False)  # Prevent frame from shrinking to child widgets
        
        label = tk.Label(
            frame, 
            text=label_text, 
            bg=self.BG_LIGHT_BLUE, 
            fg=self.TEXT_BLACK, 
            font=("Arial", self.FONT_SIZE)
        )
        label.pack(side=tk.LEFT, padx=5)
        
        # Create validation for numbers only
        vcmd = (self.register(self.validate_number), '%P')
        input_field = tk.Entry(
            frame,
            font=("Arial", self.FONT_SIZE),
            bg=self.BG_DARK_BLUE,
            fg=self.TEXT_WHITE,
            insertbackground=self.TEXT_WHITE,  # cursor color
            validate='key',
            validatecommand=vcmd
        )
        input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        return frame, input_field

    def validate_number(self, value):
        """Validates if the input is a number or empty"""
        if value == "" or value.isdigit():
            return True
        return False

    def create_combobox(self, items):
        """
        Creates a combobox with the given items and adds it to the combobox container.
        """
        style = ttk.Style()
        style.configure(
            "Custom.TCombobox",
            foreground=self.TEXT_BLACK,
            background=self.BG_DARK_BLUE,
            fieldbackground=self.BG_DARK_BLUE
        )
        
        combobox = ttk.Combobox(
            self.combobox_container,
            values=items,
            font=("Arial", self.FONT_SIZE),
            style="Custom.TCombobox",
            height=10  # Show up to 10 items in dropdown
        )
        combobox.pack(fill=tk.X, padx=10, pady=5)
        return combobox

    def init_ui(self):
        """
        Initializes the main UI layout.
        """
        # Main frame
        body = tk.Frame(self, bg="#555555", padx=20, pady=20)
        body.pack(fill=tk.BOTH, expand=True)

        # Match input section
        matches_frame = tk.Frame(body, bg="#555555", height=60)
        matches_frame.pack(fill=tk.X, pady=10)
        matches_frame.pack_propagate(False)  # Prevent resizing

        # Create match inputs side by side
        min_matches_frame, self.min_input = self.create_match_input(matches_frame, "Minimum matches:")
        min_matches_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.min_input.insert(0, "3")

        max_matches_frame, self.max_input = self.create_match_input(matches_frame, "Maximum matches:")
        max_matches_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.max_input.insert(0, "7")

        # Filters section
        filters_frame = tk.Frame(body, bg=self.BG_LIGHT_BLUE, padx=10, pady=10)
        filters_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Combobox container
        self.combobox_container = tk.Frame(filters_frame, bg=self.BG_LIGHT_BLUE)
        self.combobox_container.pack(fill=tk.X, pady=10)

        # Combo boxes for committees and qualifications
        committees_label = tk.Label(
            self.combobox_container, 
            text="Committee:", 
            bg=self.BG_LIGHT_BLUE, 
            fg=self.TEXT_BLACK, 
            font=("Arial", self.FONT_SIZE)
        )
        committees_label.pack(anchor=tk.W, padx=10)
        
        self.committees_box = self.create_combobox([""]+self.network.committees)
        self.committees_box.bind("<<ComboboxSelected>>", lambda e: self.network.update_committee(self.committees_box.get()))
        
        qualifications_label = tk.Label(
            self.combobox_container, 
            text="Qualification:", 
            bg=self.BG_LIGHT_BLUE, 
            fg=self.TEXT_BLACK, 
            font=("Arial", self.FONT_SIZE)
        )
        qualifications_label.pack(anchor=tk.W, padx=10, pady=(20, 0))
        
        self.qualifications_box = self.create_combobox([""]+self.network.qualifications)
        self.qualifications_box.bind("<<ComboboxSelected>>", lambda e: self.update_filters_state(self.qualifications_box.get()))

        # Create weights label that will be shown/hidden as needed
        self.weights_label = tk.Label(
            self.combobox_container, 
            text="Weight:", 
            bg=self.BG_LIGHT_BLUE, 
            fg=self.TEXT_BLACK, 
            font=("Arial", self.FONT_SIZE)
        )
        # We don't pack this yet - it will be packed only when needed

        # Filename input section
        filename_frame = tk.Frame(filters_frame, bg=self.BG_DARK_BLUE, padx=10, pady=10)
        filename_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)

        filename_label = tk.Label(
            filename_frame,
            text="Enter file name:",
            bg=self.BG_DARK_BLUE,
            fg=self.TEXT_WHITE,
            font=("Arial", self.FONT_SIZE, "bold")
        )
        filename_label.pack(side=tk.LEFT, padx=5)

        self.filename_input = tk.Entry(
            filename_frame,
            font=("Arial", self.FONT_SIZE),
            bg=self.BG_WHITE,
            fg=self.TEXT_BLACK
        )
        self.filename_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        # Submit button
        submission_frame = tk.Frame(body, bg=self.BG_DARK_BLUE, padx=10, pady=10, height=60)
        submission_frame.pack(fill=tk.X, pady=10)
        submission_frame.pack_propagate(False)  # Prevent resizing

        submit_btn = tk.Button(
            submission_frame,
            text="Search athletes",
            font=("Arial", self.FONT_SIZE),
            bg=self.BG_WHITE,
            fg=self.TEXT_BLACK,
            command=self.validate_input,
            padx=10,
            pady=5
        )
        submit_btn.pack(expand=True)

    def update_filters_state(self, text):
        """
        Updates the state of filters based on the selected qualification.
        """
        self.network.update_qualification(text)
        
        # Remove existing weights box if it exists
        if self.weights_box:
            self.weights_box.destroy()
            self.weights_box = None
            
        # Hide the weights label if it's currently shown
        if self.weights_label.winfo_ismapped():
            self.weights_label.pack_forget()
        
        if self.network.weights != "":
            # Show the weights label
            self.weights_label.pack(anchor=tk.W, padx=10, pady=(20, 0))
            
            # Create weights combobox
            self.weights_box = self.create_combobox([""]+self.network.weights)
            self.weights_box.bind("<<ComboboxSelected>>", lambda e: self.network.update_weights(self.weights_box.get()))

    def validate_input(self):
        """
        Validates user input and starts the search process.
        """
        min_matches = int(self.min_input.get() or 3)
        max_matches = int(self.max_input.get() or 7)
        filename = self.filename_input.get()

        if not re.match(r'^[\w\-.]+$', filename):
            messagebox.showerror("Error", "The file name contains invalid characters.")
            return

        data_manager = Writer(
            self.network,
            min_matches,
            max_matches,
            filename
        )
        
        try:
            data_manager.search()
            messagebox.showinfo(
                "Process Completed", 
                f"File '{filename}.xlsx' created successfully!"
            )
        except Exception as e:
            messagebox.showerror("Unable to save the file", str(e))

# If this file is run directly
if __name__ == "__main__":
    app = Window()
    app.mainloop()