import os
from parserObj import PDFObjectParser
from KLAC_Scripts.ParserLogger import ParserLogger  # Relative import from KLAC_Scripts

class ParserLogger:
    def __init__(self, log_file="parser_log.txt"):
        self.log_file = log_file
        # Clear the log file at the start
        with open(self.log_file, 'w', encoding='utf-8') as file:
            file.write("Parser Log Initialized\n")

    def log(self, message):
        """Log a message to the log file."""
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(message + "\n")
        print(message)  # Optional: Print log messages to the console

    def save_binary_data(self, content, counter):
        """Save unknown binary content for debugging."""
        unknown_dir = "unknown_objects"
        os.makedirs(unknown_dir, exist_ok=True)
        file_path = os.path.join(unknown_dir, f"unknown_object_{counter}.bin")
        with open(file_path, 'wb') as file:
            file.write(content)
        self.log(f"Saved unknown object to {file_path}")
