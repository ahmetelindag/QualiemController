import sys
import os 

# for direct execution
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../../"))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

# Local imports
from src.ui.styles import MAIN_STYLE
from src.ui.inspection_page import InspectionPage
from src.ui.history_page import HistoryPage
from src.ui.dashboard_page import DashboardPage
from src.ui.quality_page import QualityPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QualiemController - Prototype")
        self.resize(1200, 800)
        
        # Set default background to avoid black screen on startup
        self.setStyleSheet("background-color: #f5f6fa;")
        if MAIN_STYLE:
            self.setStyleSheet(MAIN_STYLE)

        # Main Layotu
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        #  Sidebar 
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Header 
        app_title = QLabel("QualiemController")
        app_title.setObjectName("header")
        sidebar_layout.addWidget(app_title)
        
        sidebar_layout.addSpacing(30)

        # Navigation Buttons
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard", checked=True)
        self.btn_inspection = self.create_menu_btn("🔍 FQC Inspection")
        self.btn_history = self.create_menu_btn("📝 History Logs")
        self.btn_settings = self.create_menu_btn("⚙️ Settings")
        self.btn_quality = self.create_menu_btn("📈 Quality Tools")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_inspection)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_quality)
        sidebar_layout.addStretch() 
        sidebar_layout.addWidget(self.btn_settings)

        # Operator Info
        user_info = QLabel("👤 Operator: Ahmet E.")
        user_info.setStyleSheet("color: #bdc3c7; font-size: 12px;")
        sidebar_layout.addWidget(user_info)

        #  Content Area 
        self.content_area = QStackedWidget()
        
        # Initialize pages
        self.page_dashboard = DashboardPage()
        self.page_inspection = InspectionPage()
        self.page_history = HistoryPage()
        self.page_quality = QualityPage()
        
        # Add pages to stack
        self.content_area.addWidget(self.page_dashboard)    # Index 0
        self.content_area.addWidget(self.page_inspection)   # Index 1
        self.content_area.addWidget(self.page_history)      # Index 2
        self.content_area.addWidget(self.page_quality)      # Index 3
        
        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

        #  Connections 
        self.btn_dashboard.clicked.connect(lambda: self.switch_to_dashboard(0, self.btn_dashboard))
        self.btn_inspection.clicked.connect(lambda: self.switch_page(1, self.btn_inspection))
        self.btn_history.clicked.connect(lambda: self.switch_to_history(2, self.btn_history))
        self.btn_quality.clicked.connect(lambda: self.switch_to_quality(3, self.btn_quality))

    # Helpers
    
    def create_menu_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def switch_page(self, index, active_btn):
        self.content_area.setCurrentIndex(index)
        
        # Reset button states
        self.btn_dashboard.setChecked(False)
        self.btn_inspection.setChecked(False)
        self.btn_history.setChecked(False)
        self.btn_quality.setChecked(False) 
        self.btn_settings.setChecked(False)
        
        active_btn.setChecked(True)

    def switch_to_history(self, index, active_btn):
        if hasattr(self.page_history, 'load_data'):
            self.page_history.load_data()
        self.switch_page(index, active_btn)

    def switch_to_dashboard(self, index, active_btn):
        if hasattr(self.page_dashboard, 'refresh_stats'):
            self.page_dashboard.refresh_stats()
        self.switch_page(index, active_btn)

    def switch_to_quality(self, index, active_btn):
        if hasattr(self.page_quality, 'refresh_chart'):
            self.page_quality.refresh_chart()
        self.switch_page(index, active_btn)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
