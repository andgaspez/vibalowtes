#!/usr/bin/env python3
import rospy
import sys
import os
import rospkg

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLineEdit, QFrame, QSizePolicy,
    QScrollArea, QStackedWidget, QComboBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

# === Setup ROS Package Paths ===
rospack = rospkg.RosPack()
pkg_path = rospack.get_path('skyline_gui')
image_dir = os.path.join(pkg_path, 'images')

def resource(filename):
    return os.path.join(image_dir, filename)


# === HoverImage and HoverLabel ===

class HoverLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(resource(path)))
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
        self.setPixmap(QPixmap(resource(path)))
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
            image.setPixmap(QPixmap(resource(img_path)).scaledToWidth(400))
            image.setAlignment(Qt.AlignCenter)
            image_grid.addWidget(label, row, col)
            image_grid.addWidget(image, row + 1, col)

        add_image_with_label("RAW", "raw.svg", 0, 0)
        add_image_with_label("Preprocessed", "preprocessed.svg", 0, 1)
        add_image_with_label("Skyline candidacy", "skyline_candidacy.svg", 2, 0)
        add_image_with_label("Skyline detection", "skyline_detection.svg", 2, 1)

        layout.addLayout(image_grid)

        bottom_bar = QHBoxLayout()
        bottom_bar.addWidget(QLabel("📍 Current position:"))
        bottom_bar.addWidget(QLineEdit())
        bottom_bar.addStretch()
        bottom_bar.addWidget(QPushButton("👍 Correct"))
        bottom_bar.addWidget(QPushButton("👎 Incorrect"))
        bottom_bar.addWidget(HoverImage("save.svg"))
        bottom_bar.addWidget(HoverImage("discard.svg"))

        layout.addLayout(bottom_bar)
        self.setLayout(layout)

class PreprocessingPanel(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(50)

        # === LEFT COLUMN ===
        left_column = QVBoxLayout()
        left_column.setSpacing(20)

        # Preprocessing Icon (scaled)
        icon_path = resource("img4.svg")
        renderer = QSvgRenderer(icon_path)
        default_size = renderer.defaultSize()
        scale_factor = 1.5
        scaled_width = int(default_size.width() * scale_factor)
        scaled_height = int(default_size.height() * scale_factor)

        icon = QSvgWidget(icon_path)
        icon.setFixedSize(scaled_width, scaled_height)
        icon.setStyleSheet("background: transparent;")

        icon_row = QHBoxLayout()
        icon_row.addWidget(icon)
        icon_row.addSpacing(10)
        icon_row.addStretch()

        # Dropdown controls
        control_row = QHBoxLayout()
        control_row.setSpacing(10)

        label = QLabel("Set edge detection method")
        label.setStyleSheet("color: white; font-size: 14px;")
        control_row.addWidget(label)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Canny", "Sobel"])
        self.dropdown.setStyleSheet("""
            QComboBox {
                background-color: #1a1f3c;
                color: white;
                padding: 6px;
                border: 1px solid white;
                border-radius: 4px;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox QAbstractItemView {
                background-color: #1a1f3c;
                color: white;
                selection-background-color: #2b355c;
            }
        """)
        self.dropdown.setCurrentIndex(0)
        self.dropdown.currentIndexChanged.connect(self.edge_method_changed)
        self.edge_method_changed(0)

        control_row.addWidget(self.dropdown)
        control_row.addStretch()

        # Add rows to left column
        left_column.addLayout(icon_row)
        left_column.addLayout(control_row)
        left_column.addStretch()

        # === RIGHT SIDE: OUTPUT IMAGE ===
        self.result_img = QLabel()
        self.result_img.setAlignment(Qt.AlignCenter)
        result_pixmap = QPixmap(resource("preprocessed.png")).scaled(
            800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.result_img.setPixmap(result_pixmap)
        self.result_img.setStyleSheet("background: transparent;")

        main_layout.addLayout(left_column)
        main_layout.addWidget(self.result_img, alignment=Qt.AlignTop)

        self.setLayout(main_layout)

    def edge_method_changed(self, index):
        method = self.dropdown.currentText()
        rospy.set_param("/skyline/edge_detection_method", method)
        rospy.loginfo(f"Set edge detection method to: {method}")



class SvgPanel(QWidget):
    def __init__(self, filename):
        super().__init__()
        layout = QVBoxLayout()
        svg_path = resource(filename)

        renderer = QSvgRenderer(svg_path)
        default_size = renderer.defaultSize()
        scale_factor = 1.5
        scaled_width = int(default_size.width() * scale_factor)
        scaled_height = int(default_size.height() * scale_factor)

        svg_widget = QSvgWidget(svg_path)
        svg_widget.setFixedSize(scaled_width, scaled_height)
        svg_widget.setStyleSheet("background: transparent;")

        row = QHBoxLayout()
        row.addWidget(svg_widget)
        row.addStretch()
        layout.addLayout(row)
        layout.addStretch()
        self.setLayout(layout)


class FeatureExtractionPanel(SvgPanel):
    def __init__(self):
        super().__init__("img5.svg")


class SkylineCandidacyPanel(SvgPanel):
    def __init__(self):
        super().__init__("img6.svg")


class ReportPanel(SvgPanel):
    def __init__(self):
        super().__init__("img7.svg")


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

        dataset_picker_img = HoverImage("dataset_picker.svg")
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
            thumb.setPixmap(QPixmap(resource("thumb_placeholder.jpg")).scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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

        self.stack.addWidget(HomePanel())
        self.stack.addWidget(PreprocessingPanel())
        self.stack.addWidget(FeatureExtractionPanel())
        self.stack.addWidget(SkylineCandidacyPanel())
        self.stack.addWidget(ReportPanel())

        self.stack.setCurrentIndex(0)

        # ===== Right Sidebar =====
        right_sidebar = QFrame()
        right_sidebar.setFixedWidth(350)
        right_sidebar.setStyleSheet("background-color: #101c3b;")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(0)
        right_sidebar.setLayout(sidebar_layout)

        sidebar_layout.addWidget(QLabel(pixmap=QPixmap(resource("img1.svg"))), alignment=Qt.AlignHCenter)
        logo2 = QLabel()
        logo2.setPixmap(QPixmap(resource("img2.svg")))
        logo2.setAlignment(Qt.AlignHCenter)
        logo2.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.addWidget(logo2)

        line_top = QFrame()
        line_top.setFrameShape(QFrame.HLine)
        line_top.setStyleSheet("color: white; background-color: white; max-height: 1px;")
        sidebar_layout.addWidget(line_top)

        menu_items = [
            ("img3.svg", 0),
            ("img4.svg", 1),
            ("img5.svg", 2),
            ("img6.svg", 3),
            ("img7.svg", 4)
        ]

        for path, index in menu_items:
            menu_button = HoverLabel(path)
            menu_button.clicked.connect(lambda checked=False, idx=index: self.stack.setCurrentIndex(idx))
            sidebar_layout.addWidget(menu_button)

        sidebar_layout.addWidget(QFrame(frameShape=QFrame.HLine), alignment=Qt.AlignHCenter)
        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignHCenter)
        version_label.setStyleSheet("color: white; margin-top: 10px;")
        sidebar_layout.addWidget(version_label)

        main_layout.addWidget(right_sidebar)


if __name__ == "__main__":
    rospy.init_node("skyline_gui_node", anonymous=True)
    app = QApplication(sys.argv)
    window = SkylineGUI()
    window.show()
    sys.exit(app.exec_())
