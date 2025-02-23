from typing import Final, Optional
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox
from src.components import *
from src.modules.netManager import NetManager
from src.modules.dataManager import DataManager
import re


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

        self.netManager = NetManager()
        self.dataManager: Optional[DataManager] = None
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

    def initUI(self) -> None:
        body = MyFrame(self, layout=QVBoxLayout(), spacing=10, padding=(20, 20, 20, 20))
        self.setCentralWidget(body)

        matches = MyFrame(parent=body, layout=QHBoxLayout(), height=60, padding=(0, 0, 0, 0), spacing=10)
        body.addWidget(matches)

        min_matches, self.min_input = self.create_match_input(matches, "Incontri minimi:")
        self.min_input.setText("3")
        matches.addWidget(min_matches)

        max_matches, self.max_input = self.create_match_input(matches, "Incontri massimi:")
        self.max_input.setText("5")
        matches.addWidget(max_matches)

        filters = MyFrame(
            parent=body,
            layout=QVBoxLayout(),
            spacing=50,
            stylesheet=f"{self.BG_LIGHT_BLUE} {self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        body.addWidget(filters)

        self.combo_container = MyFrame(
            parent=filters,
            layout=QVBoxLayout(),
            spacing=50,
        )
        filters.addWidget(self.combo_container)

        self.comitati_box = self.create_combobox(list(self.netManager.getComitati().keys()))
        self.comitati_box.currentTextChanged.connect(self.netManager.updateComitato)

        self.qualifiche_box = self.create_combobox(list(self.netManager.getQualifiche().keys()))
        self.qualifiche_box.currentTextChanged.connect(self.updateFiltersState)

        filters.layout.addStretch()

        name_choice = MyFrame(
            parent=filters,
            layout=QHBoxLayout(),
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        name_label = MyLabel(
            parent=name_choice,
            text="Inserisci il nome del file:",
            stylesheet=f"{self.TEXT_WHITE} font-weight: bold; {self.FONT_SIZE}"
        )
        name_choice.addWidget(name_label)

        self.name_input = MyInput(
            parent=name_choice,
            stylesheet=f"{self.TEXT_BLACK}{self.BG_WHITE}{self.BORDER_RADIUS}{self.FONT_SIZE}{self.INPUT_PADDING}"
        )
        self.name_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        name_choice.addWidget(self.name_input)

        filters.addWidget(name_choice)

        submission = MyFrame(
            parent=body,
            layout=QHBoxLayout(),
            height=60,
            stylesheet=f"{self.BG_DARK_BLUE}{self.BORDER_RADIUS}",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        body.addWidget(submission)

        submit_btn = MyButton(parent=submission, text="cerca atleti", stylesheet=f"{self.TEXT_BLACK}{self.BORDER_RADIUS}{self.FONT_SIZE}{self.BG_WHITE}{self.INPUT_PADDING}")
        submit_btn.clicked.connect(self.validateInput)
        submission.addWidget(submit_btn)

    def updateFiltersState(self, text: str) -> None:
        self.netManager.updateQualifica(text)

        if self.pesi_box:
            self.combo_container.removeWidget(self.pesi_box)
            self.pesi_box = None

        if text != "Schoolboy":
            # I pesi sono già stati caricati in cache da updateQualifica
            self.pesi_box = self.create_combobox(list(self.netManager.getPesi().keys()))
            self.pesi_box.currentTextChanged.connect(self.netManager.updatePesi)

    def validateInput(self) -> None:
        min_matches = self.min_input.text()
        max_matches = self.max_input.text()

        if min_matches != "":
            min_matches = int(min_matches)
        else:
            min_matches = 3

        if max_matches != "":
            max_matches = int(max_matches)
        else:
            max_matches = 10

        if not bool(re.match(r'^[\w\-.]+$', self.name_input.text())):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Si è verificato un errore!")
            msg.setInformativeText("il nome del file contiene caratteri non validi.")
            msg.setWindowTitle("Errore")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()

            return

        self.dataManager = DataManager(self.netManager, min_matches, max_matches)
        self.dataManager.search()