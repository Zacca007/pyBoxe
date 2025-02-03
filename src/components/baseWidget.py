from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget


class BaseWidget:
    def setup(self, widget: QWidget, width: int | None = None, height: int | None = None,
              font_size: int | None = None, stylesheet: str | None = None) -> None:
        if width is not None:
            if not isinstance(width, int) or width <= 0:
                raise ValueError("width deve essere un intero positivo")
            widget.setFixedWidth(width)

        if height is not None:
            if not isinstance(height, int) or height <= 0:
                raise ValueError("height deve essere un intero positivo")
            widget.setFixedHeight(height)

        if font_size is not None:
            if not isinstance(font_size, int) or font_size <= 0:
                raise ValueError("font_size deve essere un intero positivo")
            widget.setFont(QFont("Arial", font_size))

        if stylesheet is not None:
            if not isinstance(stylesheet, str):
                raise TypeError("stylesheet deve essere una stringa")
            widget.setStyleSheet(stylesheet)
