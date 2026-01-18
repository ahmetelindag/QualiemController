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
        self.resize(1200, 800) # Başlangıç boyutu
        
        # Stili uygula
        self.setStyleSheet(MAIN_STYLE)

        # --- ANA DÜZEN ---
        # Tüm pencereyi kapsayan ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Ana yatay düzen (Sol Menü | Sağ İçerik)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. SOL MENÜ (SIDEBAR) ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar") # Stil dosyasında yakalamak için ID
        self.sidebar.setFixedWidth(250)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        # Logo / Başlık
        app_title = QLabel("QualiemController")
        app_title.setObjectName("header")
        sidebar_layout.addWidget(app_title)
        
        sidebar_layout.addSpacing(30) # Biraz boşluk

        # Menü Butonları
        self.btn_dashboard = self.create_menu_btn("📊 Dashboard", checked=True)
        self.btn_inspection = self.create_menu_btn("🔍 FQC Inspection")
        self.btn_history = self.create_menu_btn("📝 History Logs")
        self.btn_settings = self.create_menu_btn("⚙️ Settings")
        self.btn_quality = self.create_menu_btn("📈 Quality Tools")

        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_inspection)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_quality)
        sidebar_layout.addStretch() # Kalan boşluğu aşağı it
        sidebar_layout.addWidget(self.btn_settings)

        # Operatör Bilgisi
        user_info = QLabel("👤 Operator: Ahmet E.")
        user_info.setStyleSheet("color: #666; font-size: 12px;")
        sidebar_layout.addWidget(user_info)

        # --- 2. SAĞ İÇERİK ALANI ---
        self.content_area = QStackedWidget()
        
        # Sayfaları Oluştur (Şimdilik boş etiketler koyuyoruz)
        self.page_dashboard = DashboardPage()
        self.page_inspection = InspectionPage()
        self.page_history = HistoryPage()
        self.page_quality = QualityPage()
        
        
        # Sayfaları Yığına Ekle
        self.content_area.addWidget(self.page_dashboard)    # Index 0
        self.content_area.addWidget(self.page_inspection)   #ındex 1
        self.content_area.addWidget(self.page_history)   # Index 2
        self.content_area.addWidget(self.page_quality)      # Index 3
        
        # --- BİRLEŞTİR ---
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

        # Buton Bağlantıları (Sinyaller)
        self.btn_dashboard.clicked.connect(lambda: self.switch_to_dashboard(0, self.btn_dashboard))
        self.btn_inspection.clicked.connect(lambda: self.switch_page(1, self.btn_inspection))
        self.btn_history.clicked.connect(lambda: self.switch_to_history(2, self.btn_history))
        self.btn_quality.clicked.connect(lambda: self.switch_to_quality(3, self.btn_quality))

    def create_menu_btn(self, text, checked=False):
        """Yardımcı fonksiyon: Menü butonu oluşturur."""
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def switch_page(self, index, active_btn):
        """Sayfa değiştirme ve buton aktifliğini ayarlama."""
        self.content_area.setCurrentIndex(index)
        
        # Tüm butonların seçimini kaldır
        self.btn_dashboard.setChecked(False)
        self.btn_inspection.setChecked(False)
        self.btn_history.setChecked(False)
        
        # Tıklananı seçili yap
        active_btn.setChecked(True)
    def switch_to_history(self, index, active_btn):
        """History sayfasına geçerken tabloyu yenile."""
        self.page_history.load_data() # Verileri tazele
        self.switch_page(index, active_btn)
    def switch_to_dashboard(self, index, active_btn):
        """Refreshes stats when switching to dashboard."""
        self.page_dashboard.refresh_stats()
        self.switch_page(index, active_btn)
    def switch_to_quality(self, index, active_btn):
        """Quality sayfasına geçerken grafiği yenile."""
        self.page_quality.refresh_chart()
        self.switch_page(index, active_btn)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()