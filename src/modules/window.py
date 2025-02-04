from typing import Final
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout
from src.components import *

class MyWindow(QMainWindow):
    # Costanti di stile migliorate
    BG_LIGHT_BLUE: Final[str] = "background-color: #8D99AE;"
    BG_DARK_BLUE: Final[str] = "background-color: #2B2D42;"
    BORDER_RADIUS: Final[str] = "border-radius: 5px;"
    TEXT_WHITE: Final[str] = "color: white;"
    TEXT_BLACK: Final[str] = "color: black;"
    FONT_SIZE: Final[str] = "font-size: 18px;"
    INPUT_PADDING: Final[str] = "padding: 10px;"

    min_input: MyInput
    max_input: MyInput

    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowTitle("My Custom Window")
        self.setMinimumSize(QSize(500, 500))
        self.setWindowIcon(QIcon("../assets/boxe.ico"))
        self.initUI()

    #Crea un frame con label e input numerico
    def create_match_input(self, parent: MyFrame, label_text: str) -> tuple[MyFrame, MyInput]:
        frame = MyFrame(parent=parent, layout=QHBoxLayout(), stylesheet=f"{self.BG_LIGHT_BLUE} {self.BORDER_RADIUS}")
        label = MyLabel(parent=frame, text=label_text, stylesheet=f"{self.FONT_SIZE} {self.TEXT_BLACK}")
        input_field = MyInput(parent=frame, only_numbers=True, height=45,
                              stylesheet=f"{self.FONT_SIZE} {self.BG_DARK_BLUE} {self.INPUT_PADDING}")
        frame.addWidget(label)
        frame.addWidget(input_field)
        return frame, input_field

    def initUI(self) -> None:
        body = MyFrame(self, layout=QVBoxLayout(), spacing=10, padding=(20, 20, 20, 20))
        self.setCentralWidget(body)

        # Frame per selezionare incontri minimi e massimi
        matches = MyFrame(parent=body, layout=QHBoxLayout(), height=60, padding=(0, 0, 0, 0), spacing=10)
        body.addWidget(matches)

        min_matches, self.min_input = self.create_match_input(matches, "Incontri minimi:")
        matches.addWidget(min_matches)

        max_matches, self.max_input = self.create_match_input(matches, "Incontri massimi:")
        matches.addWidget(max_matches)

        # Frame per filtri
        filters = MyFrame(parent=body, layout=QVBoxLayout(), stylesheet=f"{self.BG_LIGHT_BLUE} {self.BORDER_RADIUS}")
        body.addWidget(filters)

        # Frame per il pulsante di invio
        submission = MyFrame(parent=body, layout=QHBoxLayout(), height=60, stylesheet=f"{self.BG_DARK_BLUE} {self.BORDER_RADIUS}")
        body.addWidget(submission)
