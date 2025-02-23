from PyQt6.QtWidgets import QLabel, QWidget
from components import BaseWidget

class MyLabel(QLabel, BaseWidget):
    def __init__(self, text: str, parent: QWidget, **kwargs) -> None:
        if not isinstance(text, str):
            raise TypeError("text deve essere una stringa")
        if not isinstance(parent, QWidget):
            raise TypeError("parent deve essere un QWidget")

        super().__init__(text, parent)
        self.setup(self, **kwargs)
