from typing import Final, Optional
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy
from src.components import *
from src.modules.netManager import NetManager


class MyWindow(QMainWindow):
    # Style constants
    BG_LIGHT_BLUE: Final[str] = "background-color: #8D99AE;"
    BG_DARK_BLUE: Final[str] = "background-color: #2B2D42;"
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

        self.netManager = NetManager()
        self.pesi_box: Optional[MyComboBox] = None
        self.min_input: Optional[MyInput] = None
        self.max_input: Optional[MyInput] = None
        self.comitati_box: Optional[MyComboBox] = None
        self.qualifiche_box: Optional[MyComboBox] = None
        self.name_input: Optional[MyInput] = None
        self.combo_container: Optional[MyFrame] = None

        self.initUI()

    def create_match_input(self, parent: MyFrame, label_text: str) -> tuple[MyFrame, MyInput]:
        frame = MyFrame(
            parent=parent,
            layout=QHBoxLayout(),
            stylesheet=f"{self.BG_LIGHT_BLUE}{self.BORDER_RADIUS}"
        )

        label = MyLabel(
            parent=frame,
            text=label_text,
            stylesheet=f"{self.FONT_SIZE}{self.TEXT_BLACK}"
        )

        input_field = MyInput(
            parent=frame,
            only_numbers=True,
            height=45,
            stylesheet=f"{self.FONT_SIZE}{self.BG_DARK_BLUE}{self.INPUT_PADDING}"
        )

        frame.addWidget(label)
        frame.addWidget(input_field)
        return frame, input_field

    def create_combobox(self, elements: list[str]) -> MyComboBox:
        combobox = MyComboBox(
            parent=self.combo_container,
            items=elements,
            stylesheet=f"{self.TEXT_WHITE}{self.BG_DARK_BLUE}{self.FONT_SIZE}{self.INPUT_PADDING}"
        )
        self.combo_container.addWidget(combobox)
        return combobox

    def create_name_choice_frame(self, parent: MyFrame) -> MyFrame:
        name_choice = MyFrame(
            parent=parent,
            layout=QHBoxLayout(),
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}"
        )
        name_choice.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name_label = MyLabel(
            parent=name_choice,
            text="Inserisci il nome del file:",
            stylesheet=f"{self.TEXT_WHITE} font-weight: bold; {self.FONT_SIZE}"
        )
        name_choice.addWidget(name_label)

        self.name_input = MyInput(  # Now using class property
            parent=name_choice,
            stylesheet=f"{self.TEXT_BLACK} background-color: white; {self.BORDER_RADIUS}{self.FONT_SIZE}{self.INPUT_PADDING}"
        )
        self.name_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        name_choice.addWidget(self.name_input)

        return name_choice

    def initUI(self) -> None:
        body = MyFrame(self, layout=QVBoxLayout(), spacing=10, padding=(20, 20, 20, 20))
        self.setCentralWidget(body)

        # Matches frame
        matches = MyFrame(parent=body, layout=QHBoxLayout(), height=60, padding=(0, 0, 0, 0), spacing=10)
        body.addWidget(matches)

        min_matches, self.min_input = self.create_match_input(matches, "Incontri minimi:")
        self.min_input.setText("3")
        matches.addWidget(min_matches)

        max_matches, self.max_input = self.create_match_input(matches, "Incontri massimi:")
        self.max_input.setText("5")
        matches.addWidget(max_matches)

        # Filters frame
        filters = MyFrame(
            parent=body,
            layout=QVBoxLayout(),
            spacing=50,
            stylesheet=f"{self.BG_LIGHT_BLUE} {self.BORDER_RADIUS}"
        )
        filters.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        body.addWidget(filters)

        # Create a container for comboboxes
        self.combo_container = MyFrame(
            parent=filters,
            layout=QVBoxLayout(),
            spacing=50,
        )
        filters.addWidget(self.combo_container)

        # Create comboboxes in the container
        self.comitati_box = self.create_combobox(list(self.netManager.getComitati().keys()))
        self.comitati_box.currentTextChanged.connect(self.netManager.updateComitato)

        self.qualifiche_box = self.create_combobox(list(self.netManager.getQualifiche().keys()))
        self.qualifiche_box.currentTextChanged.connect(lambda new_str: self.updateFiltersState(new_str))

        # Add stretch to push name_choice_frame to bottom
        filters.layout.addStretch()

        # Create name choice frame at the bottom
        name_choice_frame = self.create_name_choice_frame(filters)  # Now local variable
        filters.addWidget(name_choice_frame)

        # Submission frame
        submission = MyFrame(
            parent=body,
            layout=QHBoxLayout(),
            height=50,
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}"
        )
        submission.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.addWidget(submission)

    def updateFiltersState(self, text: str) -> None:
        self.netManager.updateQualifica(text)

        if self.pesi_box:
            self.combo_container.removeWidget(self.pesi_box)
            self.pesi_box = None

        if text != "Schoolboy":
            # I pesi sono già stati caricati in cache da updateQualifica
            self.pesi_box = self.create_combobox(list(self.netManager.getPesi().keys()))
            self.pesi_box.currentTextChanged.connect(self.netManager.updatePesi)