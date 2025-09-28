import tkinter as tk
from tkinter import ttk, messagebox
from re import match
import threading
import copy
from core import FpiService, FpiWriter


class Window(tk.Tk):
    """Main application window using the new modular architecture."""

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

        # Initialize service
        self.service = FpiService()

        # UI Elements (initialized as None)
        self.weights_box = ttk.Combobox()
        self.min_input = tk.Entry()
        self.max_input = tk.Entry()
        self.committees_box = ttk.Combobox()
        self.qualifications_box = ttk.Combobox()
        self.filename_input = tk.Entry()
        self.combobox_container = None
        self.weights_label = tk.Label()

        self.init_ui()

    def create_match_input(self, parent, label_text) -> tuple[tk.Frame, tk.Entry]:
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

    @staticmethod
    def validate_number(value):
        """Validates if the input is a number or empty"""
        if value == "" or value.isdigit():
            return True
        return False

    def create_combobox(self, items) -> ttk.Combobox:
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
            state="readonly",
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

        self.committees_box = self.create_combobox([""] + self.service.committees)
        self.committees_box.bind("<<ComboboxSelected>>", self.on_committee_changed)

        qualifications_label = tk.Label(
            self.combobox_container,
            text="Qualification:",
            bg=self.BG_LIGHT_BLUE,
            fg=self.TEXT_BLACK,
            font=("Arial", self.FONT_SIZE)
        )
        qualifications_label.pack(anchor=tk.W, padx=10, pady=(20, 0))

        self.qualifications_box = self.create_combobox([""] + self.service.qualifications)
        self.qualifications_box.bind("<<ComboboxSelected>>", self.on_qualification_changed)

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

    def on_committee_changed(self, event=None):
        """Handle committee selection change."""
        selected_committee = self.committees_box.get()
        self.service.update_committee(selected_committee)

    def on_qualification_changed(self, event=None):
        """Handle qualification selection change."""
        selected_qualification = self.qualifications_box.get()
        self.service.update_qualification(selected_qualification)

        # Remove existing weights box if it exists
        if self.weights_box:
            self.weights_box.destroy()
            self.weights_box = ttk.Combobox()

        # Hide the weights label if it's currently shown
        if self.weights_label.winfo_ismapped():
            self.weights_label.pack_forget()

        # Show weights if available for the selected qualification
        available_weights = self.service.weights
        if available_weights:
            # Show the weights label
            self.weights_label.pack(anchor=tk.W, padx=10, pady=(20, 0))

            # Create weights combobox
            self.weights_box = self.create_combobox([""] + available_weights)
            self.weights_box.bind("<<ComboboxSelected>>", self.on_weight_changed)

    def on_weight_changed(self, event=None):
        """Handle weight selection change."""
        selected_weight = self.weights_box.get()
        self.service.update_weight(selected_weight)

    def validate_input(self):
        """
        Validates user input and starts the search process.
        """
        try:
            min_matches = int(self.min_input.get() or 3)
            max_matches = int(self.max_input.get() or 7)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for match counts.")
            return

        if min_matches < 0 or max_matches < 0:
            messagebox.showerror("Error", "Match counts cannot be negative.")
            return

        if min_matches > max_matches:
            messagebox.showerror("Error", "Minimum matches cannot be greater than maximum matches.")
            return

        filename = self.filename_input.get().strip()

        if not filename:
            messagebox.showerror("Error", "Please enter a file name.")
            return

        if not match(r'^[\w\-.]+$', filename):
            messagebox.showerror("Error",
                                 "The file name contains invalid characters. Use only letters, numbers, hyphens, underscores, and dots.")
            return

        # Start the search and export process
        self.perform_search(min_matches, max_matches, filename)

    def perform_search(self, min_matches, max_matches, filename):
        """
        Performs the athlete search and export operation in a separate thread.
        """
        # Create a copy of the service for this search
        service_copy = copy.deepcopy(self.service)

        def search_worker():
            try:
                # Create writer with copied service
                writer = FpiWriter(service_copy, min_matches, max_matches, filename)

                # Perform search and write
                writer.search_and_write()

                # Show success message in main thread
                self.after(0, lambda: messagebox.showinfo(
                    "Process Completed",
                    f"File '{filename}.xlsx' created successfully!\n"
                    f"Found and exported {writer.get_athlete_count()} athletes."
                ))

            except Exception as e:
                # Show error message in main thread
                self.after(0, lambda: messagebox.showerror(
                    "Error", f"An error occurred during the search:\n{str(e)}"
                ))

        # Start the search in a new thread
        search_thread = threading.Thread(target=search_worker, daemon=True)
        search_thread.start()


# If this file is run directly
if __name__ == "__main__":
    app = Window()
    app.mainloop()