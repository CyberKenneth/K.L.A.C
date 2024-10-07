import os
import subprocess
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtGui import QPalette, QBrush, QPixmap

class SkinsEngine:
    def __init__(self, preferences):
        self.preferences = preferences
        self.user_skins_path = r"C:\Users\Gaming\Desktop\K.L.A.C\klac_app\UserData\UserSkins"
        self.default_skins_path = r"C:\Users\Gaming\Desktop\K.L.A.C\klac_app\internal\gui\Gui_files\DefaultSkins"
        self.current_skin = self.preferences.get("skin", "follow_system")

    ### Theme Management ###

    def apply_skin(self, app: QApplication):
        """Apply the appropriate skin based on preferences."""
        if self.current_skin == "follow_system":
            self.apply_system_theme(app)
        elif self.current_skin == "dark":
            self.apply_dark_theme(app)
        elif self.current_skin == "light":
            self.apply_light_theme(app)
        elif self.current_skin == "high_contrast":
            self.apply_high_contrast_theme(app)
        else:
            self.load_custom_skin(self.current_skin, app)

    def apply_system_theme(self, app: QApplication):
        """Follow system dark/light mode."""
        if self.is_system_in_dark_mode():
            self.apply_dark_theme(app)
        else:
            self.apply_light_theme(app)

    def apply_dark_theme(self, app: QApplication):
        """Load a dark theme."""
        self.load_skin(os.path.join(self.default_skins_path, "dark.qss"), app)

    def apply_light_theme(self, app: QApplication):
        """Load a light theme."""
        self.load_skin(os.path.join(self.default_skins_path, "light.qss"), app)

    def apply_high_contrast_theme(self, app: QApplication):
        """Load a high contrast theme for accessibility."""
        self.load_skin(os.path.join(self.default_skins_path, "high_contrast.qss"), app)

    def load_custom_skin(self, skin_name, app: QApplication):
        """Load a custom skin from user-defined skins."""
        skin_path = os.path.join(self.user_skins_path, f"{skin_name}.qss")
        self.load_skin(skin_path, app)

    def load_skin(self, skin_path, app: QApplication):
        """Load and apply a .qss file."""
        if os.path.exists(skin_path):
            with open(skin_path, 'r') as skin_file:
                app.setStyleSheet(skin_file.read())

    ### Dark Mode Detection ###

    def is_system_in_dark_mode(self):
        """Detect if the system is in dark mode based on the operating system."""
        if os.name == 'nt':  # Windows
            return self.is_windows_dark_mode()
        elif os.name == 'posix':  # macOS or Linux
            if self.is_macos():
                return self.is_macos_dark_mode()
            return self.is_linux_dark_mode()

        return False

    def is_windows_dark_mode(self):
        """Detect if the system is in dark mode on Windows."""
        settings = QSettings("HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize", QSettings.Format.NativeFormat)
        return settings.value("AppsUseLightTheme") == 0  # 0 means dark mode

    def is_macos_dark_mode(self):
        """Detect if the system is in dark mode on macOS."""
        result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0 and 'Dark' in result.stdout.decode('utf-8')

    def is_linux_dark_mode(self):
        """Detect if the system is in dark mode on GNOME-based Linux."""
        try:
            result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], stdout=subprocess.PIPE)
            theme = result.stdout.decode('utf-8').strip().lower()
            return "dark" in theme
        except Exception:
            return False

    ### Custom Background ###

    def apply_custom_background(self, app: QApplication):
        """Allow the user to select and apply a custom background image."""
        background_image, _ = QFileDialog.getOpenFileName(None, "Select Background Image", "", "Image Files (*.png *.jpg *.bmp)")
        if background_image:
            palette = QPalette()
            pixmap = QPixmap(background_image)
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
            app.setPalette(palette)
            return background_image
        return None

    ### Saving Skins to QSS ###

    def save_custom_skin(self, background_image, primary_color, font, output_path):
        """Save a custom skin to a .qss file."""
        with open(output_path, 'w') as file:
            file.write(f"""
            * {{
                background-image: url({background_image});
                background-repeat: no-repeat;
                background-position: center;
            }}
            QLabel, QLineEdit, QPushButton {{
                color: {primary_color};
                font-family: {font};
            }}
            """)
        print(f"Custom skin saved to {output_path}")

    ### Loading QSS File ###

    def load_qss_file(self, app: QApplication, qss_file_path):
        """Load and apply a saved .qss file."""
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r') as file:
                app.setStyleSheet(file.read())
            print(f"Applied skin from {qss_file_path}")
        else:
            print(f"Skin file not found: {qss_file_path}")
