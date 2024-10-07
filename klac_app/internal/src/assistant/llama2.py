import os
import json
from transformers import pipeline

MODEL_PATH = r".\K.L.A.C\klac_app\assistant\Models"
CONFIG_FILE = "data/klac/config.klac"

def check_and_fetch_klac():
    """Check if the assistant.klac file exists. If not, disable assistant."""
    if not os.path.exists(CONFIG_FILE):
        print(f"{CONFIG_FILE} not found.")
        return False
    return True

def load_preferences():
    """Load user preferences from a .klac file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "assistant_enabled": False,
            "max_model_size_mb": 500,
            "allow_custom_training": False,
        }

def check_model_availability():
    """Check if the LLaMA model is present in the Models directory."""
    model_file_path = os.path.join(MODEL_PATH, "llama.bin")
    return os.path.exists(model_file_path)

def load_llama_model():
    """Load the LLaMA model into memory if available."""
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
