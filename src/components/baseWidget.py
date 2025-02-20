from PyQt6.QtWidgets import QWidget


class BaseWidget:
    def setup(self, widget: QWidget,
              min_width: int | None = None, width: int | None = None, max_width: int | None = None,
              min_height: int | None = None, height: int | None = None, max_height: int | None = None,
              stylesheet: str | None = None) -> None:

        # Controlli di validità e impostazione delle dimensioni
        if min_width is not None:
            if not isinstance(min_width, int) or min_width < 0:
                raise ValueError("min_width deve essere un intero non negativo")
            widget.setMinimumWidth(min_width)

        if max_width is not None:
            if not isinstance(max_width, int) or max_width <= 0:
                raise ValueError("max_width deve essere un intero positivo")
            widget.setMaximumWidth(max_width)

        if width is not None:
            if not isinstance(width, int) or width <= 0:
                raise ValueError("width deve essere un intero positivo")
            widget.setFixedWidth(width)

        if min_height is not None:
            if not isinstance(min_height, int) or min_height < 0:
                raise ValueError("min_height deve essere un intero non negativo")
            widget.setMinimumHeight(min_height)

        if max_height is not None:
            if not isinstance(max_height, int) or max_height <= 0:
                raise ValueError("max_height deve essere un intero positivo")
            widget.setMaximumHeight(max_height)

        if height is not None:
            if not isinstance(height, int) or height <= 0:
                raise ValueError("height deve essere un intero positivo")
            widget.setFixedHeight(height)

        # Impostazione dello stylesheet se fornito
        if stylesheet is not None:
            if not isinstance(stylesheet, str):
                raise TypeError("stylesheet deve essere una stringa")
            widget.setStyleSheet(stylesheet)
