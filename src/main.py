from PyQt6.QtWidgets import QApplication
from interface.window import MyWindow

def main() -> None:
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()