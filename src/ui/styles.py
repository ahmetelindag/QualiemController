# src/ui/styles.py

# Modern Dark Theme Renk Paleti
COLORS = {
    "background": "#1e1e1e",      # Ana arka plan (Koyu Gri)
    "sidebar": "#252526",         # Sol menü rengi
    "button": "#333333",          # Buton normal rengi
    "button_hover": "#3e3e42",    # Buton üzerine gelince
    "accent": "#007acc",          # Vurgu rengi (Mavi - VS Code mavisi)
    "text": "#ffffff",            # Yazı rengi
    "text_dim": "#cccccc",        # Sönük yazı
    "border": "#3e3e42"           # Kenarlıklar
}

# QSS (Qt Style Sheets) - Arayüzün CSS'i
MAIN_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    QWidget {{
        font-family: 'Segoe UI', 'Helvetica', sans-serif;
        font-size: 14px;
        color: {COLORS['text']};
    }}
    /* Sol Menü Paneli */
    QFrame#sidebar {{
        background-color: {COLORS['sidebar']};
        border-right: 1px solid {COLORS['border']};
    }}
    /* Menü Butonları */
    QPushButton {{
        background-color: transparent;
        border: none;
        border-radius: 5px;
        color: {COLORS['text_dim']};
        padding: 10px;
        text-align: left;
    }}
    QPushButton:hover {{
        background-color: {COLORS['button_hover']};
        color: {COLORS['text']};
    }}
    QPushButton:checked {{
        background-color: {COLORS['button']};
        color: {COLORS['accent']};
        border-left: 3px solid {COLORS['accent']};
    }}
    /* Aksiyon Butonları (Mavi olanlar) */
    QPushButton#action_btn {{
        background-color: {COLORS['accent']};
        color: white;
        border-radius: 4px;
        font-weight: bold;
    }}
    QPushButton#action_btn:hover {{
        background-color: #0098ff;
    }}
    /* Kartlar / Paneller */
    QFrame#panel {{
        background-color: {COLORS['sidebar']};
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
    }}
    QLabel#header {{
        font-size: 22px;
        font-weight: bold;
        color: {COLORS['text']};
    }}
"""