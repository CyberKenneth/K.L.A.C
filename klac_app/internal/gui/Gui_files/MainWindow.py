from PyQt6.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QCheckBox, QDialog, QDockWidget, QTabWidget, QMessageBox, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt
import os

class MainWindow(QMainWindow):
    def __init__(self, preferences):
        super().__init__()
        self.preferences = preferences
        self.setWindowTitle("K.L.A.C. Code Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.current_file = None
        self.setup_menu()
        self.init_docks()


    def setup_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.create_action("Save", self.save_file))
        file_menu.addAction(self.create_action("Save As", self.save_as_file))
        file_menu.addAction(self.create_action("Export", self.export_file))
        file_menu.addAction(self.create_action("Import", self.import_file))
        file_menu.addAction(self.create_action("Exit", self.close))

        view_menu = menubar.addMenu("View")
        view_menu.addAction(self.create_action("Show/Hide Source Editor", self.toggle_source_editor))
        view_menu.addAction(self.create_action("Open Assistant", self.open_assistant_chat))

        settings_menu = menubar.addMenu("Settings")
        settings_menu.addAction(self.create_action("Open settings", self.open_settings))

        help_menu = menubar.addMenu("Help")
        help_menu.addAction(self.create_action("Licenses", self.open_HelpDialogViewer))

        about_menu = menubar.addMenu("About")
        about_menu.addAction(self.create_action("Licenses", self.open_Licenses))
        about_menu.addAction(self.create_action("App goals", self.open_missionStatement))
        about_menu.addAction(self.create_action("About Me", self.open_AboutAuthor))

    def init_docks(self):
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Create editors
        self.source_editor = QTextEdit()
        self.html_editor = QTextEdit()
        self.output_viewer = QTextEdit()
        self.output_viewer.setReadOnly(True)

        # Source Editor Dock
        self.source_dock = QDockWidget("Source Editor", self)
        self.source_dock.setWidget(self.source_editor)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.source_dock)

        # HTML/CSS Editor Dock
        self.html_dock = QDockWidget("HTML/CSS Editor", self)
        self.html_dock.setWidget(self.html_editor)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.html_dock)

        # Output Viewer Dock
        self.output_dock = QDockWidget("Output Viewer", self)
        self.output_dock.setWidget(self.output_viewer)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.output_dock)

        # Add editors to tabs
        self.tabs.addTab(self.source_editor, "Source Editor")
        self.tabs.addTab(self.html_editor, "HTML/CSS Editor")
        self.tabs.addTab(self.output_viewer, "Output Viewer")

        # Set initial visibility based on preferences
        self.show_tabs = self.preferences.get("show_tabs", True)
        self.update_ui_visibility()

    def update_ui_visibility(self):
        if self.show_tabs:
            self.tabs.setVisible(True)
            self.source_dock.hide()
            self.html_dock.hide()
            self.output_dock.hide()
        else:
            self.tabs.setVisible(False)
            self.source_dock.show()
            self.html_dock.show()
            self.output_dock.show()

    def toggle_source_editor(self):
        self.show_tabs = not self.show_tabs
        self.update_ui_visibility()

    def create_action(self, text, slot):
        action = QAction(text, self)
        action.triggered.connect(slot)
        return action

    def save_file(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            self.preferences.get("default_save_path", ""),
            "All Files (*);;Text Files (*.txt)",
        )
        if file_name:
            self._save_to_file(file_name)
            self.current_file = file_name

    def _save_to_file(self, file_name):
        try:
            with open(file_name, "w") as f:
                f.write(self.source_editor.toPlainText())
            self.setWindowTitle(f"K.L.A.C. Code Editor - {os.path.basename(file_name)}")
            QMessageBox.information(self, "Save", f"File saved: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save the file: {e}")

    def export_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export File",
            self.preferences.get("default_export_path", ""),
            "EPUB Files (*.epub);;MOBI Files (*.mobi)",
        )
        if file_name:
            try:
                with open(file_name, "w") as f:
                    f.write(self.html_editor.toPlainText())
                QMessageBox.information(self, "Export", f"File exported: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export the file: {e}")

    def import_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Import File", "", "All Files (*);;PDF Files (*.pdf)"
        )
        if file_name:
            try:
                with open(file_name, "r") as f:
                    self.source_editor.setText(f.read())
                self.current_file = file_name
                self.setWindowTitle(f"K.L.A.C. Code Editor - {os.path.basename(file_name)}")
                QMessageBox.information(self, "Import", f"File imported: {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import the file: {e}")

    def open_settings(self):
        settings_dialog = SettingsDialog(self.preferences, self)
        if settings_dialog.exec() == QDialog.DialogCode.Accepted:
            self.preferences = settings_dialog.preferences
            self.apply_preferences()

    def apply_preferences(self):
        # Apply the new preferences to the main window
        font = self.source_editor.font()
        font.setPointSize(self.preferences.get("font_size", 12))
        self.source_editor.setFont(font)
        self.html_editor.setFont(font)
        self.output_viewer.setFont(font)

        # Apply theme (you'll need to implement theme switching logic)
        theme = self.preferences.get("theme", "System")
        # self.apply_theme(theme)  # Implement this method to switch themes

        # Apply language (you'll need to implement language switching logic)
        language = self.preferences.get("language", "English")
        # self.apply_language(language)  # Implement this method to switch languages

        # Update other UI elements based on preferences
        # For example, update autosave timer, logging settings, etc.

    def open_assistant_chat(self):
        """Open the assistant chat dialog."""
        assistant_dialog = AssistantDialog(self, self.preferences)
        assistant_dialog.setWindowModality(Qt.WindowModality.NonModal)
        assistant_dialog.show()

    def open_HelpDialogViewer(self):
        # Implement Help Dialog Viewer logic here
        pass

    def open_Licenses(self):
        # Implement Licenses viewer logic here
        pass

    def open_missionStatement(self):
        # Implement Mission Statement viewer logic here
        pass

    def open_AboutAuthor(self):
        # Implement About Author viewer logic here
        pass