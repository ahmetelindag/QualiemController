# src/ui/styles.py

# Modern Dark Theme Color Palette
COLORS = {
    "background": "#1e1e1e",      # Main background (Dark Grey)
    "sidebar": "#252526",         # Sidebar color
    "button": "#333333",          # Button normal color
    "button_hover": "#3e3e42",    # Button hover state
    "accent": "#007acc",          # Accent color (Blue - VS Code blue)
    "text": "#ffffff",            # Text color
    "text_dim": "#cccccc",        # Dimmed text
    "border": "#3e3e42"           # Borders
}

# QSS (Qt Style Sheets) - The CSS of the UI
MAIN_STYLE = f"""
    QMainWindow {{
        background-color: {COLORS['background']};
    }}
    QWidget {{
        font-family: 'Segoe UI', 'Helvetica', sans-serif;
        font-size: 14px;
        color: {COLORS['text']};
    }}
    /* Sidebar Panel */
    QFrame#sidebar {{
        background-color: {COLORS['sidebar']};
        border-right: 1px solid {COLORS['border']};
    }}
    /* Menu Buttons */
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
    /* Action Buttons (The blue ones) */
    QPushButton#action_btn {{
        background-color: {COLORS['accent']};
        color: white;
        border-radius: 4px;
        font-weight: bold;
    }}
    QPushButton#action_btn:hover {{
        background-color: #0098ff;
    }}
    /* Cards / Panels */
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