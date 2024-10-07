import os
import re
import traceback
import subprocess
from pathlib import Path

class Debug:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.known_issues = {
            "FileNotFoundError": self.fix_file_not_found,
            "PermissionError": self.fix_permission_error,
            # Add more known issues and corresponding fix methods
        }

    def can_fix(self, error_msg):
        """
        Determine if the error can be fixed automatically by matching it to known issues.
        
        :param error_msg: The error message to analyze
        :return: True if the error can be fixed, False otherwise
        """
        for issue in self.known_issues:
            if issue in error_msg:
                return True
        return False

    def fix_issue(self, error_msg):
        """
        Attempt to fix the issue automatically by invoking a fix method based on the error message.
        
        :param error_msg: The error message to analyze and fix
        :return: True if the fix was successful, False otherwise
        """
        for issue, fix_method in self.known_issues.items():
            if issue in error_msg:
                return fix_method(error_msg)
        return False

    def recursive_dir_build(self):
        """
        Perform a recursive directory scan starting from the root directory to build a guidebook.
        
        :return: List of all files found in the directory
        """
        file_list = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                file_path = Path(root) / file
                file_list.append(file_path)

        # Optionally save the file list as a "guidebook"
        guidebook_path = self.root_dir / 'guidebook.txt'
        with open(guidebook_path, 'w') as guidebook:
            for file_path in file_list:
                guidebook.write(str(file_path) + '\n')

        return file_list

    def find_missing_file(self, file_name):
        """
        Attempt to find a file that has been moved by searching the directory structure recursively.
        
        :param file_name: The name of the file to search for
        :return: The path to the file if found, or None
        """
        for root, dirs, files in os.walk(self.root_dir):
            if file_name in files:
                return Path(root) / file_name
        return None

    def fix_file_not_found(self, error_msg):
        """
        Attempt to fix FileNotFoundError issues by searching for the file recursively in the root directory.
        
        :param error_msg: The error message to analyze
        :return: True if the file was found and the issue was resolved, False otherwise
        """
        file_path = self.extract_file_path(error_msg)
        if file_path:
            missing_file = file_path.name
            new_location = self.find_missing_file(missing_file)
            if new_location:
                self.notify_user(f"File {missing_file} was found at {new_location}.")
                # Perform any action needed with the found file, e.g., move it back or relink
                return True
        self.notify_user(f"File not found: {file_path}. Unable to fix automatically.")
        return False

    def fix_permission_error(self, error_msg):
        """
        Attempt to fix PermissionError issues by modifying file permissions if needed.
        
        :param error_msg: The error message to analyze
        :return: True if the fix was successful, False otherwise
        """
        file_path = self.extract_file_path(error_msg)
        if file_path:
            try:
                os.chmod(file_path, 0o777)  # Grant full permissions
                self.notify_user(f"Permissions for {file_path} changed successfully.")
                return True
            except Exception as e:
                self.notify_user(f"Failed to change permissions for {file_path}. Error: {str(e)}")
        return False

    def extract_file_path(self, error_msg):
        """
        Extract the file path from an error message.
        
        :param error_msg: The error message to parse
        :return: The extracted file path, or None if not found
        """
        match = re.search(r"'(.+)'", error_msg)
        if match:
            return Path(match.group(1))
        return None

    def notify_user(self, message):
        """
        Notify the user about the status of the error and its resolution attempt.
        
        :param message: The message to display to the user
        """
        print(message)

    def check_admin_privileges(self):
        """
        Check if the script is running with administrative privileges.
        :return: True if the script is running as admin, False otherwise
        """
        try:
            is_admin = os.getuid() == 0
        except AttributeError:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return is_admin

    def run_in_user_mode(self):
        """
        Ensure the script can run in user mode, even if admin privileges are not available.
        """
        if not self.check_admin_privileges():
            self.notify_user("Running in user mode. Admin privileges not detected.")
        else:
            self.notify_user("Running with admin privileges.")

    def suggest_manual_fix(self, error_msg):
        """
        Suggest possible manual fixes for errors that cannot be automatically resolved.
        
        :param error_msg: The error message to analyze
        :return: A list of suggested fixes
        """
        suggestions = []
        if "MemoryError" in error_msg:
            suggestions.append("Consider freeing up system memory or increasing swap size.")
        if "ImportError" in error_msg:
            suggestions.append("Check if the required module is installed.")
        return suggestions

