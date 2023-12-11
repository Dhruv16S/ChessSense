import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from detect_board import return_optimal_move
from fen_notation import FenNotation

fen_notation = FenNotation()

class ChessApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 400)
        self.setWindowTitle("ChessSense")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        desktop_rect = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(int(desktop_rect.width() * 0.75), int(desktop_rect.height() * 0.25), 300, 400)

        self.label_icon = QLabel(self)
        pixmap = QPixmap("./logo.png")
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_optimal_move = QLabel("Optimal Move:\n", self)
        font_optimal_move = QFont("OpenSans", 11, QFont.Weight.Bold)
        self.label_optimal_move.setFont(font_optimal_move)
        self.label_optimal_move.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_playing_as = QLabel("Playing As?", self)
        self.label_playing_as.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_white = QPushButton("White", self)
        self.button_white.clicked.connect(lambda: self.set_player_choice("w"))

        self.button_black = QPushButton("Black", self)
        self.button_black.clicked.connect(lambda: self.set_player_choice("b"))

        layout = QVBoxLayout()
        layout.addWidget(self.label_icon)
        layout.addWidget(self.label_optimal_move)
        layout.addWidget(self.label_playing_as)
        layout.addWidget(self.button_white)
        layout.addWidget(self.button_black)
        self.setLayout(layout)
        layout.setSpacing(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_optimal_move)
        self.timer.start(100)
        self.show()
        self.player_choice = None

    def set_player_choice(self, choice):
        self.player_choice = choice
        self.label_playing_as.setText(f"Playing As: {choice.capitalize()}")
        fen_notation.define_choice(choice)

    def update_optimal_move(self):
        if self.player_choice:
            optimal_move_value = next(optimal_move_generator)
            self.label_optimal_move.setText(f"Optimal Move:\n{optimal_move_value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    optimal_move_generator = return_optimal_move()
    chess_app = ChessApp()
    sys.exit(app.exec())
