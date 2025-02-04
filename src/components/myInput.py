from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QLineEdit, QWidget
from src.components import BaseWidget

class MyInput(QLineEdit, BaseWidget):
    def __init__(self, parent: QWidget, placeholder_text: str | None = None, only_numbers: bool = False, **kwargs) -> None:
        if not isinstance(parent, QWidget):
            raise TypeError("parent deve essere un QWidget")
        if placeholder_text is not None and not isinstance(placeholder_text, str):
            raise TypeError("placeholder_text deve essere una stringa")
        if not isinstance(only_numbers, bool):
            raise TypeError("only_numbers deve essere un booleano")

        super().__init__(parent)
        self.setup(self, **kwargs)

        if placeholder_text:
            self.setPlaceholderText(placeholder_text)
        if only_numbers:
            self.setValidator(QIntValidator())
