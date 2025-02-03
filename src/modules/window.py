from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout

from src.components import MyFrame

class MyWindow(QMainWindow):
    LIGHT_BLUE = "background-color: #8D99AE;"
    DARK_BLUE = "background-color: #2B2D42;"
    BORDER = "border-radius: 5px"
    TEXT_COLOR = "white"


    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowTitle("My Custom Window")
        self.setMinimumSize(QSize(500, 500))
        self.initUI()

    def initUI(self) -> None:
        body = MyFrame(self, layout = QVBoxLayout(), spacing=10, padding=(20, 20, 20, 20))
        self.setCentralWidget(body)

        matches = MyFrame(parent=body, layout=QHBoxLayout(), spacing=10, height=50, stylesheet=f"{self.LIGHT_BLUE}{self.BORDER}")
        body.addWidget(matches)

        filters = MyFrame(parent=body, layout=QVBoxLayout(), stylesheet=f"{self.LIGHT_BLUE}{self.BORDER}")
        body.addWidget(filters)

        submission = MyFrame(parent=body, layout= QHBoxLayout(), height=50, stylesheet=f"{self.DARK_BLUE}{self.BORDER}")
        body.addWidget(submission)