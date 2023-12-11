import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont
from detect_board import return_optimal_move

class ChessApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 300)
        self.setWindowTitle("ChessSense")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        desktop_rect = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(int(desktop_rect.width() * 0.75), int(desktop_rect.height() * 0.25), 300, 300)

        self.label_icon = QLabel(self)
        pixmap = QPixmap("./logo.png")
        self.label_icon.setPixmap(pixmap)
        self.label_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_optimal_move = QLabel("Optimal Move:\n", self)
        font_optimal_move = QFont("OpenSans", 11, QFont.Weight.Bold)
        self.label_optimal_move.setFont(font_optimal_move)
        self.label_optimal_move.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label_icon)
        layout.addWidget(self.label_optimal_move)
        self.setLayout(layout)
        layout.setSpacing(0)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_optimal_move)
        self.timer.start(100)
        self.show()

    def update_optimal_move(self):
        optimal_move_value = next(optimal_move_generator)
        self.label_optimal_move.setText(f"Optimal Move:\n{optimal_move_value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    optimal_move_generator = return_optimal_move()
    chess_app = ChessApp()
    sys.exit(app.exec())
