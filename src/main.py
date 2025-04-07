def pyqt() -> None:
    from PyQt6.QtWidgets import QApplication
    from interface.pyqt.window import MyWindow
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

def tkinter() -> None:
    from interface.tkinter.WIndow import Window
    window = Window()
    window.mainloop()

if __name__ == "__main__":
    pyqt()