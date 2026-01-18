import sys
from src.ui.inspection_page import InspectionPage
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from src.ui.styles import MAIN_STYLE
from src.ui.history_page import HistoryPage
from src.ui.dashboard_page import DashboardPage
from src.ui.quality_page import QualityPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QualiemController - Prototype")
        self.resize(1200, 800) # Initial size
        
        # Apply style
        self.setStyleSheet(MAIN_STYLE)

        # MAIN LAYOUT 
        # Main widget covering the entire window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main horizontal layout (Left Menu | Right Content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. (SIDEBAR)
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar") # ID to target in style file
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Logo / Title
        app_title = QLabel("QualiemController")
        app_title.setObjectName("header")
        sidebar_layout.addWidget(app_title)
        
        sidebar_layout.addSpacing(30) # Add a little spacing

        # Menu Buttons
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard", checked=True)
        self.btn_inspection = self.create_menu_btn("🔍 FQC Inspection")
        self.btn_history = self.create_menu_btn("📝 History Logs")
        self.btn_settings = self.create_menu_btn("⚙️ Settings")
        self.btn_quality = self.create_menu_btn("📈 Quality Tools")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_inspection)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_quality)
        sidebar_layout.addStretch() # Push remaining space down
        sidebar_layout.addWidget(self.btn_settings)