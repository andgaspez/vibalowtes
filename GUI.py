from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QFrame, QSizePolicy,
    QScrollArea
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


# === HoverLabel Class for Sidebar Menu Items ===
class HoverLabel(QLabel):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(path))
        self.setContentsMargins(70, 40, 0, 40)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setStyleSheet("background-color: transparent;")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgba(255, 255, 255, 40); border-radius: 5px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: transparent;")
        super().leaveEvent(event)


# === HoverImage Class for Dataset Picker ===
class HoverImage(QLabel):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(path))
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: transparent; padding: 5px;")

    def enterEvent(self, event):
        self.setStyleSheet("background-color: rgba(255, 255, 255, 40); border-radius: 5px; padding: 5px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("background-color: transparent; padding: 5px;")
        super().leaveEvent(event)


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
        left_layout.setSpacing(20)
        main_layout.addLayout(left_layout, stretch=5)

        # ======= TOP BAR LAYOUT =======
        top_bar = QHBoxLayout()
        top_bar.setSpacing(0)

        # Dataset picker image and label
        picker_layout = QVBoxLayout()
        picker_layout.setSpacing(10)
        picker_layout.setContentsMargins(0, 30, 5, 60)
        picker_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        dataset_picker_img = HoverImage("images/dataset_picker.svg")
        picker_layout.addWidget(dataset_picker_img)

        dataset_label = QLabel("Current Dataset:")
        dataset_label.setStyleSheet("font-weight: bold; color: white;")
        dataset_label.setAlignment(Qt.AlignCenter)
        picker_layout.addWidget(dataset_label)

        top_bar.addLayout(picker_layout)

        # Carousel
        carousel_container = QFrame()

        carousel_container.setFixedSize(1320, 120)
        carousel_container.setStyleSheet("background-color: #1a1f3c; border-radius: 4px;")
        carousel_layout = QHBoxLayout()
        carousel_layout.setContentsMargins(5, 5, 5, 5)
        carousel_layout.setSpacing(10)
        carousel_container.setLayout(carousel_layout)

        left_arrow = QLabel("◀")
        left_arrow.setAlignment(Qt.AlignCenter)
        left_arrow.setStyleSheet("font-size: 18px; color: white;")
        carousel_layout.addWidget(left_arrow)

        scroll_area = QScrollArea()
        scroll_area.setFixedHeight(100)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")

        thumbnails_widget = QFrame()
        thumbs_layout = QHBoxLayout()
        thumbs_layout.setContentsMargins(0, 0, 0, 0)
        thumbs_layout.setSpacing(10)

        for i in range(10):
            thumb = QLabel()
            thumb.setPixmap(QPixmap("images/thumb_placeholder.jpg").scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            thumb.setFixedSize(60, 60)
            thumb.setStyleSheet("border: 2px solid #202e59;")
            thumbs_layout.addWidget(thumb)

        thumbnails_widget.setLayout(thumbs_layout)
        scroll_area.setWidget(thumbnails_widget)
        carousel_layout.addWidget(scroll_area)

        right_arrow = QLabel("▶")
        right_arrow.setAlignment(Qt.AlignCenter)
        right_arrow.setStyleSheet("font-size: 18px; color: white;")
        carousel_layout.addWidget(right_arrow)

        top_bar.addWidget(carousel_container)
        left_layout.addLayout(top_bar)

        # Horizontal Line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        left_layout.addWidget(horizontal_line)

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

        # ========== Right Sidebar ==========
        right_sidebar = QFrame()
        right_sidebar.setFixedWidth(350)
        right_sidebar.setStyleSheet("background-color: #101c3b;")

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(0)
        right_sidebar.setLayout(sidebar_layout)

        # Sidebar logos
        logo1 = QLabel()
        logo1.setPixmap(QPixmap("images/img1.svg"))
        logo1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        logo2 = QLabel()
        logo2.setPixmap(QPixmap("images/img2.svg"))
        logo2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo2.setContentsMargins(0, 20, 0, 20)
        logo2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        sidebar_layout.addWidget(logo1, alignment=Qt.AlignHCenter)
        sidebar_layout.addWidget(logo2, alignment=Qt.AlignHCenter)

        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        sidebar_layout.addWidget(line_top)

        menu_images = [
            "images/img3.svg",
            "images/img4.svg",
            "images/img5.svg",
            "images/img6.svg",
            "images/img7.svg"
        ]
        for path in menu_images:
            sidebar_layout.addWidget(HoverLabel(path))

        line_bottom = QFrame()
        line_bottom.setFrameShape(QFrame.HLine)
        line_bottom.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        sidebar_layout.addWidget(line_bottom)

        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignHCenter)
        version_label.setStyleSheet("color: white; margin-top: 10px;")
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(right_sidebar)
        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkylineGUI()
    window.show()
    sys.exit(app.exec_())
