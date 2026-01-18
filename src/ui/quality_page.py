from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QSizePolicy, QGridLayout)
from PyQt6.QtCore import Qt
from src.core.database import DatabaseManager
import numpy as np  # İstatistik hesabı için (Yoksa: pip install numpy)

# Grafik Kütüphanesi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class QualityPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.chart_layout = None 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # --- 1. BAŞLIK VE ÖZET KARTLARI ---
        top_section = QHBoxLayout()
        
        # Başlık
        title_box = QVBoxLayout()
        header = QLabel("📈 Quality Control Center")
        header.setStyleSheet("font-size: 22px; font-weight: bold; color: white;")
        desc = QLabel("Statistical Process Control (SPC) & Frequency Analysis")
        desc.setStyleSheet("color: #aaa; font-size: 13px;")
        title_box.addWidget(header)
        title_box.addWidget(desc)
        
        top_section.addLayout(title_box)
        top_section.addStretch()
        
        # İstatistik Kutucukları (Mean, Max vs.)
        self.lbl_stats = QLabel("Avg: 0 | Max: 0 | StdDev: 0.0")
        self.lbl_stats.setStyleSheet("""
            background-color: #333; color: #4cd964; 
            padding: 8px; border-radius: 5px; font-weight: bold;
            border: 1px solid #555;
        """)
        top_section.addWidget(self.lbl_stats)
        
        layout.addLayout(top_section)

        # --- 2. GRAFİK ALANI (Tek Canvas içinde 2 Grafik) ---
        self.chart_frame = QFrame()
        self.chart_frame.setStyleSheet("background-color: #252526; border-radius: 10px;")
        self.chart_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.chart_layout = QVBoxLayout(self.chart_frame)
        layout.addWidget(self.chart_frame)

        # İlk açılış
        self.refresh_chart()

    def refresh_chart(self):
        """Verileri çeker, istatistikleri hesaplar ve 2 grafik çizer."""
        logs = self.db.get_all_logs()
        logs.reverse() # Eskiden yeniye sırala

        ids = [row[0] for row in logs]
        defects = [row[3] for row in logs]

        # --- İSTATİSTİK HESAPLAMA ---
        if len(defects) > 0:
            avg_defect = np.mean(defects)
            max_defect = np.max(defects)
            std_dev = np.std(defects)
            stats_text = f"Average Defects: {avg_defect:.2f}  |  Max Spike: {max_defect}  |  Stability (σ): {std_dev:.2f}"
        else:
            stats_text = "No Data Available"
        
        self.lbl_stats.setText(stats_text)

        # --- MATPLOTLIB GRAFİKLERİ ---
        # 2 Satır, 1 Sütunluk bir figür oluşturuyoruz
        fig = Figure(figsize=(8, 8), dpi=100)
        fig.patch.set_facecolor('#252526')
        fig.subplots_adjust(hspace=0.4) # İki grafik arası boşluk

        # GRAFİK 1: SPC Trend (Çizgi)
        ax1 = fig.add_subplot(211) # 2 satır, 1 sütun, 1. grafik
        ax1.set_facecolor('#1e1e1e')
        
        if len(ids) > 0:
            ax1.plot(ids, defects, color='#0098ff', marker='o', markersize=4, label='Defects')
            ax1.axhline(y=5, color='#dc3545', linestyle='--', alpha=0.8, label='Upper Limit (UCL)')
            ax1.set_title("Process Stability Trend (SPC)", color='white', fontsize=10)
            ax1.set_ylabel("Defect Count", color='#ccc')
            ax1.grid(True, color='#333', linestyle=':')
            ax1.tick_params(colors='#ccc')
            ax1.legend(facecolor='#252526', edgecolor='#444', labelcolor='white', fontsize=8)
        else:
            ax1.text(0.5, 0.5, "Waiting for data...", ha='center', color='#666')

        # GRAFİK 2: Histogram (Çubuk)
        ax2 = fig.add_subplot(212) # 2 satır, 1 sütun, 2. grafik
        ax2.set_facecolor('#1e1e1e')

        if len(defects) > 0:
            # Histogram verisi: Hataların dağılımı
            counts, bins, patches = ax2.hist(defects, bins=range(min(defects), max(defects) + 2), 
                                             color='#28a745', alpha=0.7, rwidth=0.8, align='left')
            ax2.set_title("Defect Frequency Distribution", color='white', fontsize=10)
            ax2.set_xlabel("Defect Count (Severity)", color='#ccc')
            ax2.set_ylabel("Frequency", color='#ccc')
            ax2.set_xticks(bins[:-1]) # X eksenine tam sayıları yaz
            ax2.grid(axis='y', color='#333', linestyle=':')
            ax2.tick_params(colors='#ccc')
        else:
            ax2.text(0.5, 0.5, "Waiting for data...", ha='center', color='#666')

        # Grafiği Ekrana Bas
        canvas = FigureCanvas(fig)
        
        if self.chart_layout.count() > 0:
            self.chart_layout.itemAt(0).widget().setParent(None)
            
        self.chart_layout.addWidget(canvas)