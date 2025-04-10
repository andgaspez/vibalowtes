from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


class SkylineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Skyline Detection GUI")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #202e59; color: white;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ========== Left Main Content ==========
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(left_layout, stretch=5)

        # Dataset picker
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("📁 Dataset Picker"))
        top_bar.addWidget(QLabel("Current Dataset:"))
        left_layout.addLayout(top_bar)

        # Image grid
        grid = QGridLayout()
        grid.addWidget(QLabel("RAW"), 0, 0)
        grid.addWidget(QLabel("Preprocessed"), 0, 1)
        grid.addWidget(QLabel("Skyline candidacy"), 2, 0)
        grid.addWidget(QLabel("Skyline detection:"), 2, 1)
        left_layout.addLayout(grid)

        # Bottom bar
        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(QLabel("📍 Current position:"))
        bottom_bar.addWidget(QLineEdit())
        bottom_bar.addStretch()
        bottom_bar.addWidget(QPushButton("👍 Correct"))
        bottom_bar.addWidget(QPushButton("👎 Incorrect"))
        bottom_bar.addWidget(QPushButton("💾 Save"))
        bottom_bar.addWidget(QPushButton("🗑️ Discard"))
        left_layout.addLayout(bottom_bar)

        version_label = QLabel("Version 1.0")
        version_label.setStyleSheet("color: white;")
        left_layout.addWidget(version_label)

        # ========== Right Sidebar ==========
        right_sidebar = QFrame()
        right_sidebar.setFixedWidth(350)
        right_sidebar.setStyleSheet("background-color: #101c3b;")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(0)
        right_sidebar.setLayout(sidebar_layout)

        # === Top Logos: tightly stacked with NO gap ===
        logo1 = QLabel()
        logo1.setPixmap(QPixmap("images/img1.svg"))
        logo1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo1.setContentsMargins(0, 0, 0, 0)
        logo1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        logo2 = QLabel()
        logo2.setPixmap(QPixmap("images/img2.svg"))
        logo2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo2.setContentsMargins(0, 0, 0, 0)
        logo2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        sidebar_layout.addWidget(logo1, alignment=Qt.AlignHCenter)
        sidebar_layout.addWidget(logo2, alignment=Qt.AlignHCenter)
        sidebar_layout.addSpacing(20)  # spacing after logos before menu

        # === Menu items ===
        menu_images = [
            "images/img3.svg",  # Home
            "images/img4.svg",  # Preprocessing
            "images/img5.svg",  # Feature Extraction
            "images/img6.svg",  # Skyline Candidacy
            "images/img7.svg"   # Report Generation
        ]

        for path in menu_images:
            label = QLabel()
            pixmap = QPixmap(path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
            label.setContentsMargins(70, 0, 0, 0)
            label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
            sidebar_layout.addWidget(label)

        main_layout.addWidget(right_sidebar)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkylineGUI()
    window.show()
    sys.exit(app.exec_())
