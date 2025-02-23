from typing import Final, Optional
import re
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox
from components import *
from modules import *


class MyWindow(QMainWindow):
    # Style constants
    BG_LIGHT_BLUE: Final[str] = "background-color: #8D99AE;"
    BG_DARK_BLUE: Final[str] = "background-color: #2B2D42;"
    BG_WHITE: Final[str] = "background-color: white;"
    BORDER_RADIUS: Final[str] = "border-radius: 5px;"
    TEXT_WHITE: Final[str] = "color: white;"
    TEXT_BLACK: Final[str] = "color: black;"
    FONT_SIZE: Final[str] = "font-size: 18px;"
    INPUT_PADDING: Final[str] = "padding: 5px;"

    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowTitle("My Custom Window")
        self.setMinimumSize(QSize(550, 550))
        self.setWindowIcon(QIcon("../assets/boxe.ico"))

        # Managers
        self.net_manager = NetManager()
        self.data_manager: Optional[DataManager] = None

        # UI Elements (initialized as None)
        self.weights_box: Optional[MyComboBox] = None
        self.min_input: Optional[MyInput] = None
        self.max_input: Optional[MyInput] = None
        self.committees_box: Optional[MyComboBox] = None
        self.qualifications_box: Optional[MyComboBox] = None
        self.filename_input: Optional[MyInput] = None
        self.combobox_container: Optional[MyFrame] = None

        self.init_ui()

    def create_match_input(self, parent: MyFrame, label_text: str) -> tuple[MyFrame, MyInput]:
        """
        Creates a horizontal frame with a label and an input field for match counts.
        """
        frame = MyFrame(parent, layout=QHBoxLayout(), stylesheet=f"{self.BG_LIGHT_BLUE}{self.BORDER_RADIUS}")
        label = MyLabel(parent=frame, text=label_text, stylesheet=f"{self.FONT_SIZE}{self.TEXT_BLACK}")
        input_field = MyInput(
            parent=frame,
            only_numbers=True,
            height=45,
            stylesheet=f"{self.FONT_SIZE}{self.BG_DARK_BLUE}{self.INPUT_PADDING}"
        )
        frame.addWidget(label)
        frame.addWidget(input_field)
        return frame, input_field

    def create_combobox(self, items: list[str]) -> MyComboBox:
        """
        Creates a combobox with the given items and adds it to the combobox container.
        """
        combobox = MyComboBox(
            parent=self.combobox_container,
            items=items,
            stylesheet=f"{self.TEXT_WHITE}{self.BG_DARK_BLUE}{self.FONT_SIZE}{self.INPUT_PADDING}"
        )
        self.combobox_container.addWidget(combobox)
        return combobox

    def init_ui(self) -> None:
        """
        Initializes the main UI layout.
        """
        body = MyFrame(self, layout=QVBoxLayout(), spacing=10, padding=(20, 20, 20, 20))
        self.setCentralWidget(body)

        # Match input section
        matches_frame = MyFrame(parent=body, layout=QHBoxLayout(), height=60, padding=(0, 0, 0, 0), spacing=10)
        body.addWidget(matches_frame)

        min_matches_frame, self.min_input = self.create_match_input(matches_frame, "Minimum matches:")
        self.min_input.setText("3")
        matches_frame.addWidget(min_matches_frame)

        max_matches_frame, self.max_input = self.create_match_input(matches_frame, "Maximum matches:")
        self.max_input.setText("7")
        matches_frame.addWidget(max_matches_frame)

        # Filters section
        filters_frame = MyFrame(
            parent=body,
            layout=QVBoxLayout(),
            spacing=50,
            stylesheet=f"{self.BG_LIGHT_BLUE}{self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        body.addWidget(filters_frame)

        self.combobox_container = MyFrame(parent=filters_frame, layout=QVBoxLayout(), spacing=50)
        filters_frame.addWidget(self.combobox_container)

        # Combo boxes for committees and qualifications
        self.committees_box = self.create_combobox(list(self.net_manager.get_committees().keys()))
        self.committees_box.currentTextChanged.connect(self.net_manager.update_committee)

        self.qualifications_box = self.create_combobox(list(self.net_manager.get_qualifications().keys()))
        self.qualifications_box.currentTextChanged.connect(self.update_filters_state)

        filters_frame.layout.addStretch()

        # Filename input
        filename_frame = MyFrame(
            parent=filters_frame,
            layout=QHBoxLayout(),
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        filename_label = MyLabel(
            parent=filename_frame,
            text="Enter file name:",
            stylesheet=f"{self.TEXT_WHITE} font-weight: bold; {self.FONT_SIZE}"
        )
        filename_frame.addWidget(filename_label)

        self.filename_input = MyInput(
            parent=filename_frame,
            stylesheet=f"{self.TEXT_BLACK}{self.BG_WHITE}{self.BORDER_RADIUS}{self.FONT_SIZE}{self.INPUT_PADDING}"
        )
        self.filename_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        filename_frame.addWidget(self.filename_input)
        filters_frame.addWidget(filename_frame)

        # Submit button
        submission_frame = MyFrame(
            parent=body,
            layout=QHBoxLayout(),
            height=60,
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        body.addWidget(submission_frame)
        submit_btn = MyButton(
            parent=submission_frame,
            text="Search athletes",
            stylesheet=f"{self.TEXT_BLACK}{self.BORDER_RADIUS}{self.FONT_SIZE}{self.BG_WHITE}{self.INPUT_PADDING}"
        )
        submit_btn.clicked.connect(self.validate_input)
        submission_frame.addWidget(submit_btn)

    def update_filters_state(self, text: str) -> None:
        """
        Updates the state of filters based on the selected qualification.
        """
        self.net_manager.update_qualification(text)
        if self.weights_box:
            self.combobox_container.removeWidget(self.weights_box)
            self.weights_box = None
        if text != "Schoolboy":
            self.weights_box = self.create_combobox(list(self.net_manager.get_weights().keys()))
            self.weights_box.currentTextChanged.connect(self.net_manager.update_weights)

    def validate_input(self) -> None:
        """
        Validates user input and starts the search process.
        """
        min_matches = int(self.min_input.text() or 3)
        max_matches = int(self.max_input.text() or 7)

        if not re.match(r'^[\w\-.]+$', self.filename_input.text()):
            QMessageBox.critical(QMessageBox(), "Error", "The file name contains invalid characters.")
            return

        self.data_manager = DataManager(
            self.net_manager,
            min_matches,
            max_matches,
            self.filename_input.text()
        )
        self.data_manager.search()