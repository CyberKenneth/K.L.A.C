from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QMessageBox
from klac_app.internal.src.core.Scripts.KLAC_Scripts.CrashCollector import CrashCollector


class CrashWindow(QDialog):
    def __init__(self, exception, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Application Crash")
        self.resize(500, 400)
        
        # Layout setup
        layout = QVBoxLayout()

        # Display crash message
        self.message_label = QLabel("The application has crashed. Below is the error report.")
        layout.addWidget(self.message_label)

        # Display the stack trace
        self.stack_trace = QTextEdit()
        self.stack_trace.setReadOnly(True)
        self.stack_trace.setText(self.format_stack_trace(exception))
        layout.addWidget(self.stack_trace)

        # Button to send the report
        self.send_button = QPushButton("Send Report")
        self.send_button.clicked.connect(self.send_report)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.crash_collector = CrashCollector()

    def format_stack_trace(self, exception):
        """Format the stack trace and error message."""
        return f"Exception Type: {type(exception).__name__}\n\n" + \
               f"Exception Message: {str(exception)}\n\n" + \
               f"Stack Trace:\n{''.join(traceback.format_exception(None, exception, exception.__traceback__))}"

    def send_report(self):
        """Send the crash report using CrashCollector and ErrorLogger."""
        # Ask if the user wants to send the report anonymously
        confirmation = QMessageBox.question(
            self,
            "Send Anonymously?",
            "Do you want to send the report anonymously?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        send_anonymously = confirmation == QMessageBox.StandardButton.Yes

        # Use CrashCollector to handle the crash and ErrorLogger to log the error
        self.crash_collector.handle_crash(
            exception=self.stack_trace.toPlainText(), 
            verbose=False, 
            send_anonymously=send_anonymously
        )

        QMessageBox.information(self, "Report Sent", "The error report has been sent.")
        self.close()
