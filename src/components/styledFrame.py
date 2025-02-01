from PyQt5.QtWidgets import QFrame


class StyledFrame(QFrame):
    """ Frame con stile personalizzabile. """

    def __init__(self, parent=None, height=None, width=None, color="#8D99AE"):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)