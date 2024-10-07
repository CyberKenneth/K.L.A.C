import requests
import subprocess
import sys
import os

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/CyberKenneth/K.L.A.C/Main/requirements.txt'

def fetch_requirements():
    """Fetch requirements.txt from the GitHub repository."""
    try:
        response = requests.get(GITHUB_RAW_URL)
        response.raise_for_status()  # Raise an error for bad responses
        with open('requirements.txt', 'w') as f:
            f.write(response.text)
        print("Fetched requirements.txt from GitHub.")
    except requests.RequestException as e:
        print(f"Error fetching requirements.txt: {e}")

def install_requirements():
    """Install the dependencies from requirements.txt."""
    if os.path.exists('requirements.txt'):
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install dependencies: {e}")
    else:
        print("requirements.txt not found. Skipping installation.")

if __name__ == '__main__':
    fetch_requirements()  # Fetch the latest requirements.txt from GitHub
    install_requirements()  # Install the dependencies
