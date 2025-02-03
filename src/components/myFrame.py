from PyQt6.QtWidgets import QFrame, QLayout, QWidget
from src.components import BaseWidget


class MyFrame(QFrame, BaseWidget):
    def __init__(self, parent: QWidget, layout: QLayout, spacing: int | None = None,
                 padding: tuple[int, int, int, int] | None = None, **kwargs) -> None:
        if not isinstance(parent, QWidget):
            raise TypeError("parent deve essere un QWidget")
        if not isinstance(layout, QLayout):
            raise TypeError("layout deve essere un QLayout")

        super().__init__(parent)
        self.setup(self, **kwargs)

        self.layout = layout
        self.setLayout(self.layout)

        if spacing is not None:
            if not isinstance(spacing, int) or spacing < 0:
                raise ValueError("spacing deve essere un intero positivo")
            self.layout.setSpacing(spacing)

        if padding is not None:
            if not (isinstance(padding, tuple) and len(padding) == 4 and all(isinstance(x, int) and x >= 0 for x in padding)):
                raise ValueError("padding deve essere una tupla di 4 interi positivi")
            self.layout.setContentsMargins(*padding)

    def addWidget(self, widget: QWidget) -> None:
        if not isinstance(widget, QWidget):
            raise TypeError("widget deve essere un QWidget")
        self.layout.addWidget(widget)
