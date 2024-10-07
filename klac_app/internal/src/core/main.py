import os
import json
import sys
import traceback
from PyQt6.QtWidgets import QApplication, QMessageBox

# Get the absolute path of the current script
current_script_path = os.path.abspath(__file__)

# Set the base path to the directory containing K.L.A.C
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(current_script_path), "..", "..", "..", ".."))

# Add necessary directories to sys.path
sys.path.append(BASE_PATH)  # Add the root directory to path
sys.path.append(os.path.join(BASE_PATH, "klac_app"))  # Add klac_app to path

# Now we can import klac_app modules
from internal.src.core.Scripts.KLAC_Scripts.CrashCollector import CrashCollector
from internal.src.assistant.llama import manage_llama_model
from internal.gui.gui import KLACGUI
from internal.gui.Gui_files.CrashWindow import CrashWindow
from internal.src.core.Scripts.KLAC_Scripts.debug import Debug

# Path to the config file
CONFIG_FILE = os.path.join(BASE_PATH, "klac_app", "internal", "src", "config", "config.klac")

def load_config():
    """Load the config.klac file."""
    try:
        with open(CONFIG_FILE, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found. Please ensure the config file exists.")
        sys.exit(1)

def save_config(config):
    """Save the configuration to the config.klac file."""
    try:
        with open(CONFIG_FILE, "w") as config_file:
            json.dump(config, config_file, indent=4)
        print(f"Configuration saved to {CONFIG_FILE}.")
    except PermissionError:
        print(f"Warning: Unable to save configuration to {CONFIG_FILE} due to permission error.")
        # Optionally, you could save to a user-writable location as a fallback

def ensure_directories(config):
    """Ensure that all necessary directories exist."""
    for key, path in config.items():
        if key.endswith("_path") or key.endswith("_directory"):
            full_path = os.path.join(BASE_PATH, path)
            try:
                if not os.path.exists(full_path):
                    os.makedirs(full_path)
                    print(f"Created directory: {full_path}")
            except PermissionError:
                print(f"Warning: Unable to create directory: {full_path}. The application may have limited functionality.")

def exception_hook(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions."""
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # Initialize Debug class
    debug = Debug(BASE_PATH)
    
    # Check permission level and notify user
    if debug.check_admin_privileges():
        print("Running with elevated privileges. This is not necessary for normal operation.")
    else:
        print("Running with user-level privileges.")
    
    # Try to debug and fix the issue
    if debug.can_fix(error_msg):
        print("Attempting to fix the issue...")
        if debug.fix_issue(error_msg):
            print("Issue fixed. Resuming operation.")
            return
        else:
            print("Failed to fix the issue automatically. Proceeding with crash report.")
            suggestions = debug.suggest_manual_fix(error_msg)
            if suggestions:
                print("Suggested manual fixes:")
                for suggestion in suggestions:
                    print(f"- {suggestion}")
    else:
        print("Unable to automatically fix the issue. Proceeding with crash report.")

    # If debugging fails or can't fix, proceed with crash report
    crash_collector = CrashCollector()
    crash_collector.handle_crash(error_msg)
    
    # Show crash window to the user
    if QApplication.instance():
        crash_window = CrashWindow(exc_value)
        crash_window.exec()
    else:
        print("Unhandled exception:", error_msg)

def main():
    """Main function to run the application."""
    try:
        # Load configuration
        config = load_config()

        # Ensure all necessary directories exist
        ensure_directories(config)

        # Create QApplication instance
        app = QApplication(sys.argv)

        # Check if running with elevated privileges and warn user
        debug = Debug(BASE_PATH)
        if debug.check_admin_privileges():
            QMessageBox.warning(None, "Elevated Privileges", 
                                "The application is running with elevated privileges. " +
                                "This is not necessary for normal operation and may pose security risks.")

        # Initialize KLACGUI with the loaded config
        klac_gui = KLACGUI(config, app)

        # Load assistant model if enabled
        if config.get("assistant_enabled", False):
            manage_llama_model()

        # Run the application
        return klac_gui.run()

    except Exception as e:
        exception_hook(type(e), e, e.__traceback__)
        return 1

if __name__ == '__main__':
    # Set up global exception handling
    sys.excepthook = exception_hook

    # Run the main function
    sys.exit(main())