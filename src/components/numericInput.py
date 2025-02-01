from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLineEdit


class NumericInput(QLineEdit):
    """ QLineEdit che accetta solo numeri interi. """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValidator(QIntValidator())
        self.setFixedHeight(30)
        self.setStyleSheet(
            "background-color: #D9D9D9; color: black; border-radius: 3px; padding: 2px;"
        )