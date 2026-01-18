import cv2
import os
import numpy as np
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QFileDialog, QGridLayout, QDialog, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QCursor
from src.core.image_processor import ImageProcessor
from src.core.database import DatabaseManager

# --- 1. YENİ SINIF: TAM EKRAN GÖRÜNTÜLEYİCİ ---
class ImageViewer(QDialog):
    def __init__(self, cv_image, title="Image Viewer"):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(800, 600) # Varsayılan açılış boyutu
        
        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Resmi hazırla
        self.set_image(cv_image)
        
        # Scroll Area (Resim çok büyükse kaydırmak için)
        scroll = QScrollArea()
        scroll.setWidget(self.label)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

    def set_image(self, cv_img):
        if cv_img is None: return
        
        # Renk dönüşümü
        if len(cv_img.shape) == 2:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

# --- 2. YENİ SINIF: TIKLANABİLİR ETİKET ---
class ClickableImageLabel(QLabel):
    def __init__(self, title):
        super().__init__(title)
        self.original_image = None # Orijinal yüksek çözünürlüklü resmi sakla
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #444; 
                background-color: #222; 
                color: #666;
            }
            QLabel:hover {
                border: 2px solid #00ff00; /* Üzerine gelince yeşil çerçeve */
                cursor: pointer;
            }
        """)
        self.setMinimumSize(320, 240)
        # Resim büyüyebilsin diye politika ayarı
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
    def set_cv_image(self, cv_img):
        """Resmi hem ekranda göster hem hafızada tut"""
        self.original_image = cv_img
        if cv_img is None: return

        # Ekranda göstermek için küçültülmüş/uyarlanmış halini hazırla
        if len(cv_img.shape) == 2:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
        else:
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            
        h, w, ch = rgb_img.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_img.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        
        # Etiketin boyutuna sığdır (KeepAspectRatio)
        self.setPixmap(pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def mouseDoubleClickEvent(self, event):
        """Çift tıklanınca bu çalışır"""
        if self.original_image is not None:
            # Yeni pencere aç
            viewer = ImageViewer(self.original_image, self.text())
            viewer.exec()

# --- 3. GÜNCELLENMİŞ SAYFA ---
class InspectionPage(QWidget):
    def __init__(self):
        super().__init__()
        
        self.processor = ImageProcessor()
        self.db = DatabaseManager()
        self.ref_path = None
        self.test_path = None
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # --- ÜST PANEL ---
        top_controls = QHBoxLayout()
        
        self.btn_load_ref = QPushButton("📂 Load Reference")
        self.btn_load_ref.clicked.connect(self.load_reference)
        
        self.btn_load_test = QPushButton("📂 Load Test Image")
        self.btn_load_test.clicked.connect(self.load_test)
        
        self.btn_run = QPushButton("▶ RUN INSPECTION")
        self.btn_run.setStyleSheet("background-color: #28a745; color: white; font-weight: bold; padding: 10px;")
        self.btn_run.clicked.connect(self.run_analysis)
        self.btn_run.setEnabled(False)
        
        top_controls.addWidget(self.btn_load_ref)
        top_controls.addWidget(self.btn_load_test)
        top_controls.addStretch()
        top_controls.addWidget(self.btn_run)
        
        layout.addLayout(top_controls)
        
        # --- ORTA PANEL (RESİMLER) ---
        grid = QGridLayout()
        
        # Artık normal QLabel yerine ClickableImageLabel kullanıyoruz
        self.lbl_ref = ClickableImageLabel("Reference Image")
        grid.addWidget(self.lbl_ref, 0, 0)
        
        self.lbl_test = ClickableImageLabel("Test Image (Input)")
        grid.addWidget(self.lbl_test, 0, 1)
        
        self.lbl_aligned = ClickableImageLabel("Aligned View")
        grid.addWidget(self.lbl_aligned, 1, 0)
        
        self.lbl_result = ClickableImageLabel("FINAL RESULT")
        # Final Result daha dikkat çekici olsun
        self.lbl_result.setStyleSheet("border: 2px solid #28a745; background-color: #111; color: #28a745; font-weight: bold;")
        grid.addWidget(self.lbl_result, 1, 1)
        
        layout.addLayout(grid)
        
        # --- ALT PANEL ---
        self.status_label = QLabel("Status: Waiting for images... (Double click images to zoom)")
        self.status_label.setStyleSheet("color: #aaa; font-style: italic;")
        layout.addWidget(self.status_label)

    def load_reference(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Reference", "data/images", "Images (*.png *.jpg *.jpeg *.bmp)")
        if fname:
            self.ref_path = fname
            img = cv2.imread(fname)
            self.lbl_ref.set_cv_image(img) # Yeni fonksiyonu kullanıyoruz
            self.check_ready()

    def load_test(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Test Image", "data/images", "Images (*.png *.jpg *.jpeg *.bmp)")
        if fname:
            self.test_path = fname
            img = cv2.imread(fname)
            self.lbl_test.set_cv_image(img) # Yeni fonksiyonu kullanıyoruz
            self.check_ready()
            
    def check_ready(self):
        if self.ref_path and self.test_path:
            self.btn_run.setEnabled(True)
            self.status_label.setText("Status: Ready. Double click any image to enlarge.")

    def run_analysis(self):
        self.status_label.setText("Status: Processing...")
        self.status_label.repaint()
        
        try:
            # 1. Yükle
            img_ref = self.processor.load_image(self.ref_path)
            img_test = self.processor.load_image(self.test_path)
            
            # 2. Hizala
            aligned_img = self.processor.align_images(img_test, img_ref)
            self.lbl_aligned.set_cv_image(aligned_img) # Göster
            
            # 3. Hata Bul
            result_img, thresh, count = self.processor.detect_defects(img_ref, aligned_img)
            self.lbl_result.set_cv_image(result_img) # Göster
            
            # 4. Durum
            if count == 0:
                self.status_label.setText("✅ PASS: Perfect match.")
                self.status_label.setStyleSheet("color: #4cd964; font-weight: bold;")
            else:
                self.status_label.setText(f"❌ FAIL: {count} defects detected! (Double click image to see details)")
                self.status_label.setStyleSheet("color: #ff3b30; font-weight: bold;")

            # 5. DB Kayıt
            if self.test_path:
                file_name = os.path.basename(self.test_path)
                self.db.add_log(file_name, count)
                
        except Exception as e:
            self.status_label.setText(f"ERROR: {str(e)}")
            print(e)