from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from components import StyledFrame, NumericInput



class Window(QMainWindow):
    BG_COLOR = "#8D99AE"
    FRAME_COLOR = "#2B2D42"
    TEXT_COLOR = "white"

    def __init__(self):
        super().__init__(None)
        self.setWindowTitle("PyBoxe")
        self.setGeometry(100, 100, 600, 700)
        self.setMinimumSize(500, 500)

        self.min_input = NumericInput()
        self.max_input = NumericInput()

        self.initUI()
        self.show()

    def initUI(self) -> None:
        body = QWidget(self)
        layout = QVBoxLayout(body)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setCentralWidget(body)

        # Frame incontri minimi/massimi
        matches_frame = StyledFrame(parent=body, height=70, color=self.BG_COLOR)
        matches_layout = QHBoxLayout(matches_frame)
        matches_layout.setSpacing(10)

        min_frame = self.create_input_frame("Incontri minimi:", self.min_input)
        max_frame = self.create_input_frame("Incontri massimi:", self.max_input)

        matches_layout.addWidget(min_frame)
        matches_layout.addWidget(max_frame)

        # Frame principale e frame di invio
        main_frame = StyledFrame(parent=body, color=self.BG_COLOR)
        submit_frame = StyledFrame(parent=body, height=60, color=self.FRAME_COLOR)

        # Aggiunta al layout principale
        layout.addWidget(matches_frame)
        layout.addWidget(main_frame)
        layout.addWidget(submit_frame)

    def create_input_frame(self, label_text: str, input_box: NumericInput) -> StyledFrame:
        """ Crea un frame con un'etichetta e un input box. """
        frame = StyledFrame(color=self.FRAME_COLOR)
        layout = QHBoxLayout(frame)
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setStyleSheet(f"color: {self.TEXT_COLOR}; font-size: 20px;")

        layout.addWidget(label)
        layout.addWidget(input_box)
        layout.setAlignment(Qt.AlignHCenter)
        return frame