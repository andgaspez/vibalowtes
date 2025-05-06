from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QFrame, QSizePolicy,
    QScrollArea, QStackedWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import sys


class HoverLabel(QLabel):
    clicked = pyqtSignal()

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

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


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
        self.setWindowTitle("A Vision-Based Navigation Method in Low-Textured Environments")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #202e59; color: white;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ========== Left Layout ==========
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)
        main_layout.addLayout(left_layout, stretch=5)

        # ===== Top Bar (Dataset Picker + Carousel) =====
        top_bar = QHBoxLayout()
        top_bar.setSpacing(0)

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
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        left_layout.addWidget(line)

        # ===== Tabs Stack =====
        self.stack = QStackedWidget()
        left_layout.addWidget(self.stack)

        # ====== Define panels ======
        self.home_panel = QLabel("Home Panel", alignment=Qt.AlignCenter)
        self.preprocess_panel = QLabel("Preprocessing Panel", alignment=Qt.AlignCenter)
        self.feature_panel = QLabel("Feature Extraction Panel", alignment=Qt.AlignCenter)
        self.skyline_panel = self.create_skyline_panel()
        self.report_panel = QLabel("Report Generation Panel", alignment=Qt.AlignCenter)

        # Add panels to stack
        self.stack.addWidget(self.home_panel)
        self.stack.addWidget(self.preprocess_panel)
        self.stack.addWidget(self.feature_panel)
        self.stack.addWidget(self.skyline_panel)
        self.stack.addWidget(self.report_panel)

        self.stack.setCurrentIndex(0)

        # ===== Right Sidebar =====
        right_sidebar = QFrame()
        right_sidebar.setFixedWidth(350)
        right_sidebar.setStyleSheet("background-color: #101c3b;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(0)
        right_sidebar.setLayout(sidebar_layout)

        logo1 = QLabel()
        logo1.setPixmap(QPixmap("images/img1.svg"))
        logo1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        logo2 = QLabel()
        logo2.setPixmap(QPixmap("images/img2.svg"))
        logo2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        logo2.setContentsMargins(0, 20, 0, 20)

        sidebar_layout.addWidget(logo1, alignment=Qt.AlignHCenter)
        sidebar_layout.addWidget(logo2, alignment=Qt.AlignHCenter)

        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        sidebar_layout.addWidget(line_top)

        # ===== Menu with Clickable Labels =====
        menu_items = [
            ("images/img3.svg", 0),  # Home
            ("images/img4.svg", 1),  # Preprocessing
            ("images/img5.svg", 2),  # Feature Extraction
            ("images/img6.svg", 3),  # Skyline Candidacy
            ("images/img7.svg", 4)   # Report Generation
        ]

        for path, index in menu_items:
            menu_button = HoverLabel(path)
            menu_button.clicked.connect(lambda checked=False, idx=index: self.stack.setCurrentIndex(idx))
            sidebar_layout.addWidget(menu_button)

        line_bottom = QFrame()
        line_bottom.setFrameShape(QFrame.HLine)
        line_bottom.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        sidebar_layout.addWidget(line_bottom)

        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignHCenter)
        version_label.setStyleSheet("color: white; margin-top: 10px;")
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(right_sidebar)

    def create_skyline_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        image_grid = QGridLayout()
        image_grid.setSpacing(20)

        def add_image_with_label(label_text, img_path, row, col):
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignCenter)
            image = QLabel()
            image.setPixmap(QPixmap(img_path).scaledToWidth(400))
            image.setAlignment(Qt.AlignCenter)
            image_grid.addWidget(label, row, col)
            image_grid.addWidget(image, row + 1, col)

        add_image_with_label("RAW", "images/raw.svg", 0, 0)
        add_image_with_label("Preprocessed", "images/preprocessed.svg", 0, 1)
        add_image_with_label("Skyline candidacy", "images/skyline_candidacy.svg", 2, 0)
        add_image_with_label("Skyline detection", "images/skyline_detection.svg", 2, 1)

        layout.addLayout(image_grid)

        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(QLabel("📍 Current position:"))
        bottom_bar.addWidget(QLineEdit())
        bottom_bar.addStretch()
        bottom_bar.addWidget(QPushButton("👍 Correct"))
        bottom_bar.addWidget(QPushButton("👎 Incorrect"))

        save_label = HoverImage("images/save.svg")
        bottom_bar.addWidget(save_label)

        discard_label = HoverImage("images/discard.svg")
        bottom_bar.addWidget(discard_label)

        layout.addLayout(bottom_bar)

        return panel


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkylineGUI()
    window.show()
    sys.exit(app.exec_())
