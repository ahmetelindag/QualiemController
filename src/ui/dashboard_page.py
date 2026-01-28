from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QSizePolicy)
from PyQt6.QtCore import Qt
from src.core.database import DatabaseManager

# Graphics Lib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.chart_container = None # Layout
        self.init_ui()

    def init_ui(self):
        # main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # --- 1. title---
        header = QLabel("📊 System Overview")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(header)

        # --- 2. boards ---
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        self.card_total = self.create_card("Total Inspections", "0", "#007acc") # blue
        self.card_pass = self.create_card("Pass Rate", "0%", "#28a745")        # green
        self.card_defects = self.create_card("Total Defects", "0", "#dc3545")  # red

        cards_layout.addWidget(self.card_total)
        cards_layout.addWidget(self.card_pass)
        cards_layout.addWidget(self.card_defects)

        layout.addLayout(cards_layout)

        # --- 3. GRAPHICS AREA ---
        # frame
        chart_frame = QFrame()
        chart_frame.setStyleSheet("background-color: #252526; border-radius: 10px;")
        chart_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Graph Layout
        self.chart_container = QVBoxLayout(chart_frame)
        self.chart_container.setContentsMargins(10, 10, 10, 10) # inner space
        
        layout.addWidget(chart_frame, stretch=1) 
        
        # Load data on first startup.
        self.refresh_stats()

    def create_card(self, title, value, color):
        """ creates flashcards"""
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
        
        
        card.value_label = lbl_value
        return card

    def create_pie_chart(self, pass_count, fail_count):
       
        
        # 1.Figure Settings
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#252526') # Background color (Dark Gray)
        
        ax = fig.add_subplot(111)
        
        # 2. Data and Colors
        sizes = [pass_count, fail_count]
        labels = ['PASS', 'FAIL']
        
        
        # pass_count -> green (#28a745)
        # fail_count -> red (#dc3545)
        colors = ['#28a745', '#dc3545'] 
        
        # 3. Draw the graph
        if sum(sizes) == 0:
            # If there is no data
            ax.text(0.5, 0.5, "No Data", ha='center', va='center', color='#888', fontsize=14)
            ax.axis('off')
        else:
            wedges, texts, autotexts = ax.pie(
                sizes, 
                labels=labels, 
                colors=colors, 
                autopct='%1.1f%%',      
                startangle=140,          
                textprops=dict(color="white", fontsize=10, weight='bold') 
            )
            
            
            ax.axis('equal')  

        # 4. Heading and Layout Arrangement 
        ax.set_title("Inspection Results Distribution", color='white', fontsize=12, pad=10)
        fig.tight_layout() 

        canvas = FigureCanvas(fig)
        return canvas

    def refresh_stats(self):
        
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

        # Update Cards
        self.card_total.value_label.setText(str(total))
        self.card_pass.value_label.setText(f"%{pass_rate}")
        self.card_defects.value_label.setText(str(defects))

        # update graph
        
        if self.chart_container is not None:
            for i in reversed(range(self.chart_container.count())): 
                widget = self.chart_container.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            # add new graph
            chart_canvas = self.create_pie_chart(pass_count, fail_count)
            self.chart_container.addWidget(chart_canvas)
