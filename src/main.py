import sys
from PyQt5.QtWidgets import QApplication
from window import Window

"""
Entry point of the application.
Initializes the Qt application and shows the main window.
"""
def main() -> None:
    application = QApplication(sys.argv)
    main_window = Window()
    main_window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    main()