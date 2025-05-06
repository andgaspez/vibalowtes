from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QFrame, QSizePolicy,
    QScrollArea, QStackedWidget
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import sys

# === HoverImage and HoverLabel ===

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

# === Panels for Each Tab ===

class HomePanel(QWidget):

    def __init__(self):
            super().__init__()
            layout = QVBoxLayout()

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
            bottom_bar.addWidget(HoverImage("images/save.svg"))
            bottom_bar.addWidget(HoverImage("images/discard.svg"))

            layout.addLayout(bottom_bar)

            self.setLayout(layout)

class PreprocessingPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("⚙️ Preprocessing Panel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class FeatureExtractionPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("🔍 Feature Extraction Panel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)


class SkylineCandidacyPanel(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("🛰️ Skyline Panel Placeholder")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

class ReportPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("📊 Report Generation Panel")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

# === Main GUI ===

class SkylineGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("A Vision-Based Navigation Method in Low-Textured Environments")
        self.setGeometry(100, 100, 1600, 900)
        self.setStyleSheet("background-color: #202e59; color: white;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== Left Layout =====
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)
        main_layout.addLayout(left_layout, stretch=5)

        # ===== Top Bar =====
        top_bar = QHBoxLayout()
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

        carousel_layout.addWidget(QLabel("◀", alignment=Qt.AlignCenter))
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
        carousel_layout.addWidget(QLabel("▶", alignment=Qt.AlignCenter))

        top_bar.addWidget(carousel_container)
        left_layout.addLayout(top_bar)

        # ===== Horizontal Line =====
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        left_layout.addWidget(line)

        # ===== Tabs Stack =====
        self.stack = QStackedWidget()
        left_layout.addWidget(self.stack)

        # Create and add all panels
        self.home_panel = HomePanel()
        self.preprocess_panel = PreprocessingPanel()
        self.feature_panel = FeatureExtractionPanel()
        self.skyline_panel = SkylineCandidacyPanel()
        self.report_panel = ReportPanel()

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

        # Menu items with tab indices
        menu_items = [
            ("images/img3.svg", 0),
            ("images/img4.svg", 1),
            ("images/img5.svg", 2),
            ("images/img6.svg", 3),
            ("images/img7.svg", 4)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SkylineGUI()
    window.show()
    sys.exit(app.exec_())
