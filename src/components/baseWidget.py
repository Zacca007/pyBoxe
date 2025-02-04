from PyQt6.QtWidgets import QWidget

class BaseWidget:
    def setup(self, widget: QWidget, width: int | None = None, height: int | None = None, stylesheet: str | None = None) -> None:
        if width is not None:
            if not isinstance(width, int) or width <= 0:
                raise ValueError("width deve essere un intero positivo")
            widget.setFixedWidth(width)

        if height is not None:
            if not isinstance(height, int) or height <= 0:
                raise ValueError("height deve essere un intero positivo")
            widget.setFixedHeight(height)

        if stylesheet is not None:
            if not isinstance(stylesheet, str):
                raise TypeError("stylesheet deve essere una stringa")
            widget.setStyleSheet(stylesheet)
