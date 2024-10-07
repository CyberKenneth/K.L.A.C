import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
sys.path.insert(0, project_root)

import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenu, QFileDialog, QMessageBox, 
    QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, 
    QLabel, QCheckBox, QDialog, QDockWidget, QTabWidget, QComboBox,
    QGroupBox, QRadioButton, QGridLayout, QSpinBox, QSlider
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QDir, QTimer

# Import custom components using absolute imports
from klac_app.internal.gui.Gui_files.MainWindow import MainWindow
from klac_app.internal.gui.Gui_files.SettingsDialog import SettingsDialog
# future use 
#from klac_app.internal.gui.Gui_files.AssistantDialog import AssistantDialog
from klac_app.internal.gui.Gui_files.CrashWindow import CrashWindow
from klac_app.internal.gui.Gui_files.SkinEngine import SkinsEngine


# Other imports
from klac_app.internal.src.assistant.llama import manage_llama_model
from klac_app.internal.src.core.Scripts.KLAC_Scripts.CrashCollector import CrashCollector

class KLACGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.load_preferences()
        self.setup_skin_engine()
        self.main_window = MainWindow(self.preferences)
        self.setup_error_handling()

    def load_preferences(self):
        # Load preferences from a file or use defaults
        self.preferences = {
            "default_save_path": QDir.homePath(),
            "default_export_path": QDir.homePath(),
            "language": "English",
            "theme": "System",
            "font_size": 12,
            "reopen_windows_on_startup": True,
            "autosave_interval": 5,
            "enable_logging": False,
            "default_ai_model": "tiny-gpt",
            "max_token_limit": 500,
            "enable_ai_suggestions": True,
            "ai_response_speed": "Balanced",
            "cpu_allocation": "50%",
            "ram_allocation": "4 GB",
            "storage_allocation": "25%",
            "selected_drive": "",
            "show_tabs": True,
            "skin": "follow_system"
        }
        # TODO: Implement actual preference loading from a file

    def setup_skin_engine(self):
        self.skin_engine = SkinsEngine(self.preferences)
        self.skin_engine.apply_skin(self.app)

    def setup_error_handling(self):
        sys.excepthook = self.handle_exception

    def handle_exception(self, exc_type, exc_value, exc_traceback):
        crash_window = CrashWindow(exc_value)
        crash_window.exec()

    def run(self):
        self.main_window.show()
        return self.app.exec()

if __name__ == "__main__":
    klac_gui = KLACGUI()
    sys.exit(klac_gui.run())