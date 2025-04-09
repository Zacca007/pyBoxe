from PyQt6.QtWidgets import QComboBox, QWidget
from . import BaseWidget

class MyComboBox(QComboBox, BaseWidget):
    def __init__(self, parent: QWidget, items: list[str] | None = None, default_index: int = -1, **kwargs) -> None:
        if not isinstance(parent, QWidget):
            raise TypeError("parent deve essere un QWidget")
        if items is not None:
            if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
                raise TypeError("items deve essere una lista di stringhe")
        if not isinstance(default_index, int) or (items and default_index >= len(items)):
            raise ValueError("default_index deve essere un intero valido")

        super().__init__(parent)
        self.setup(self, **kwargs)

        if items:
            self.addItems(items)
            self.setCurrentIndex(default_index)

    def setItems(self, items: list[str]) -> None:
        if not isinstance(items, list) or not all(isinstance(item, str) for item in items):
            raise TypeError("items deve essere una lista di stringhe")
        self.clear()
        self.addItems(items)

    def getSelectedItem(self) -> str:
        return self.currentText()

    def setSelectedItem(self, index: int) -> None:
        if not isinstance(index, int) or index < 0 or index >= self.count():
            raise ValueError("index deve essere un intero valido")
        self.setCurrentIndex(index)
