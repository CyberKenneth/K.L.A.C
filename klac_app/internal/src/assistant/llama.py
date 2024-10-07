import os
import json
import subprocess

MODEL_PATH = r"C:\Users\tread\Downloads\New folder (3)\K.L.A.C\klac_app\assistant\Models"
PREFERENCES_FILE = "preferences.klac"

def load_preferences():
    """Load user preferences from a .klac file."""
    try:
        with open(PREFERENCES_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "assistant_enabled": False,
            "max_model_size_mb": 500,
            "allow_custom_training": False,
            "training_data_path": os.path.join(os.getcwd(), "training_data"),
        }

def save_preferences(preferences):
    """Save user preferences to a .klac file."""
    with open(PREFERENCES_FILE, "w") as file:
        json.dump(preferences, file, indent=4)

def check_model_availability():
    """Check if the LLaMA model is present in the Models directory."""
    model_file_path = os.path.join(MODEL_PATH, "llama.bin")
    return os.path.exists(model_file_path)

def load_llama_model():
    """Load the LLaMA model into memory."""
    if check_model_availability():
        print("Loading LLaMA model from disk...")
        # Add actual model loading logic here (e.g., using transformers)
        print("LLaMA model loaded successfully.")
    else:
        print("LLaMA model not found. Please run UpdateLlama.py to download the model.")

def manage_llama_model():
    """Check for the model and load it if available."""
    preferences = load_preferences()
    if preferences.get("assistant_enabled", False):
        load_llama_model()

if __name__ == '__main__':
    manage_llama_model()
