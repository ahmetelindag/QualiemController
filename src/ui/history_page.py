from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QPushButton, QLabel, QHBoxLayout)
from PyQt6.QtCore import Qt
from src.core.database import DatabaseManager

class HistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- HEADER ---
        header_layout = QHBoxLayout()
        title = QLabel("📋 Inspection History Logs")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ddd;")
        
        self.btn_refresh = QPushButton("🔄 Refresh Data")
        self.btn_refresh.setFixedWidth(120)
        self.btn_refresh.setStyleSheet("background-color: #007acc; color: white; font-weight: bold;")
        self.btn_refresh.clicked.connect(self.load_data)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_refresh)
        
        layout.addLayout(header_layout)

        # --- TABLE ---
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Timestamp", "Filename", "Defects", "Status"])
        
        # Tablo Tasarımı (Stil)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                color: #ddd;
                gridline-color: #444;
                border: none;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                padding: 5px;
                border: 1px solid #444;
            }
        """)
        
        # Sütunları genişliğe yay
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        
        # İlk açılışta veriyi yükle
        self.load_data()

    def load_data(self):
        """Fetches data from DB and populates the table."""
        logs = self.db.get_all_logs()
        self.table.setRowCount(0) # Tabloyu temizle
        
        for row_idx, row_data in enumerate(logs):
            self.table.insertRow(row_idx)
            # row_data formatı: (id, timestamp, filename, count, status)
            
            for col_idx, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Status sütununu renklendir (PASS=Yeşil, FAIL=Kırmızı)
                if col_idx == 4: # Status sütunu
                    if data == "PASS":
                        item.setForeground(Qt.GlobalColor.green)
                    else:
                        item.setForeground(Qt.GlobalColor.red)
                
                self.table.setItem(row_idx, col_idx, item)