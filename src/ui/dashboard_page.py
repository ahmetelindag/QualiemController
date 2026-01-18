from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from src.core.database import DatabaseManager

# Grafik Kütüphanesi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.chart_container = None # Grafik layout referansı
        self.init_ui()

    def init_ui(self):
        # Ana Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # --- 1. BAŞLIK ---
        header = QLabel("📊 System Overview")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        # --- 2. KARTLAR (İSTATİSTİKLER) ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_total = self.create_card("Total Inspections", "0", "#007acc") # Mavi
        self.card_pass = self.create_card("Pass Rate", "0%", "#28a745")        # Yeşil
        self.card_defects = self.create_card("Total Defects", "0", "#dc3545")  # Kırmızı

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_pass)
        cards_layout.addWidget(self.card_defects)

        layout.addLayout(cards_layout)

        # --- 3. GRAFİK ALANI ---
        # Grafiği tutacak şık bir çerçeve
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: #252526; border-radius: 10px;")
        chart_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Grafik Layout'u
        self.chart_container = QVBoxLayout(chart_frame)
        self.chart_container.setContentsMargins(10, 10, 10, 10) # İç boşluk
        
        layout.addWidget(chart_frame, stretch=1) 
        
        # İlk açılışta verileri yükle
        self.refresh_stats()

    def create_card(self, title, value, color):
        """Bilgi kartlarını oluşturur."""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
            }}
        """)
        card.setFixedSize(250, 120)
        
        card_layout = QVBoxLayout(card)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: rgba(255,255,255,0.8); font-size: 14px;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet("color: white; font-size: 36px; font-weight: bold;")
        lbl_value.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_value)
        
        # Sonradan güncellemek için etiketi sakla
        card.value_label = lbl_value
        return card

    def create_pie_chart(self, pass_count, fail_count):
        """PASS (Yeşil) ve FAIL (Kırmızı) Pasta Grafiği oluşturur."""
        
        # 1. Figür Ayarları
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#252526') # Arka plan rengi (Koyu Gri)
        
        ax = fig.add_subplot(111)
        
        # 2. Veriler ve Renkler
        sizes = [pass_count, fail_count]
        labels = ['PASS', 'FAIL']
        
        # BURASI ÖNEMLİ: Sıra sizes listesiyle aynı olmalı
        # pass_count -> Yeşil (#28a745)
        # fail_count -> Kırmızı (#dc3545)
        colors = ['#28a745', '#dc3545'] 
        
        # 3. Grafiği Çiz
        if sum(sizes) == 0:
            # Hiç veri yoksa
            ax.text(0.5, 0.5, "No Data", ha='center', va='center', color='#888', fontsize=14)
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=colors, 
                autopct='%1.1f%%',       # Yüzde formatı
                startangle=140,          # Başlangıç açısı (Görsellik için)
                textprops=dict(color="white", fontsize=10, weight='bold') # Yazı ayarları
            )
            
            # Tam yuvarlak olması için (Ovalleşmeyi önler)
            ax.axis('equal')  

        # 4. Başlık ve Yerleşim Düzenleme (Kaymayı önler)
        ax.set_title("Inspection Results Distribution", color='white', fontsize=12, pad=10)
        fig.tight_layout() # <-- KAYMAYI ÖNLEYEN SİHİRLİ KOD BU

        canvas = FigureCanvas(fig)
        return canvas

    def refresh_stats(self):
        """Verileri çeker ve grafiği yeniler."""
        logs = self.db.get_all_logs()
        
        total = len(logs)
        defects = sum([row[3] for row in logs])
        
        pass_count = 0
        if total > 0:
            pass_count = len([row for row in logs if row[4] == "PASS"])
            pass_rate = int((pass_count / total) * 100)
        else:
            pass_rate = 0
            
        fail_count = total - pass_count

        # Kartları Güncelle
        self.card_total.value_label.setText(str(total))
        self.card_pass.value_label.setText(f"%{pass_rate}")
        self.card_defects.value_label.setText(str(defects))

        # Grafiği Güncelle
        # Önce eski grafiği temizle
        if self.chart_container is not None:
            for i in reversed(range(self.chart_container.count())): 
                widget = self.chart_container.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # Yeni grafiği ekle
            chart_canvas = self.create_pie_chart(pass_count, fail_count)
            self.chart_container.addWidget(chart_canvas)