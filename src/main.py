import sys
import os

# Path Configuration

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

if root_dir not in sys.path:
    sys.path.append(root_dir)


from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    # İnitialize the application
    app = QApplication(sys.argv)
    
    # Create and disply the main window
    window = MainWindow()
    window.show()
    
    # Execute loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
