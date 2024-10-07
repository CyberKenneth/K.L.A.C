import os
import datetime
import traceback

class CrashCollector:
    def __init__(self, log_directory="klac_app/internal/resources/logs/bugs"):
        self.log_directory = log_directory
        self.ensure_log_directory()

    def ensure_log_directory(self):
        """Ensure the log directory exists."""
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def log_crash(self, exception):
        """Log the crash details to a file."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"crash_{timestamp}.log"
        log_path = os.path.join(self.log_directory, log_filename)

        # Collect crash information
        crash_details = f"Timestamp: {timestamp}\n"
        crash_details += f"Exception Type: {type(exception).__name__}\n"
        crash_details += f"Exception Message: {str(exception)}\n"
        crash_details += "Stack Trace:\n"
        crash_details += "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

        # Write crash details to the log file
        with open(log_path, "w") as log_file:
            log_file.write(crash_details)

        print(f"Crash details logged to {log_path}")

    def get_latest_crash(self):
        """Return the latest crash log file."""
        logs = [f for f in os.listdir(self.log_directory) if f.startswith("crash_")]
        if logs:
            latest_log = max(logs, key=lambda f: os.path.getmtime(os.path.join(self.log_directory, f)))
            with open(os.path.join(self.log_directory, latest_log), "r") as log_file:
                return log_file.read()
        return None
