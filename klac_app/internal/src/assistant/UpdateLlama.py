import os
import requests

MODEL_PATH = r"C:\Users\tread\Downloads\New folder (3)\K.L.A.C\klac_app\assistant\Models"
LLAMA_MODEL_URL = "https://huggingface.co/models/llama/llama-7b"  # Example URL for the model

def update_llama_model():
    """Download the LLaMA model from the specified URL."""
    print("Updating LLaMA model...")
    response = requests.get(LLAMA_MODEL_URL, stream=True)
    if response.status_code == 200:
        with open(os.path.join(MODEL_PATH, "llama.bin"), "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Model downloaded successfully.")
    else:
        print(f"Failed to download the model. HTTP Status Code: {response.status_code}")

def check_model_folder():
    """Ensure the model folder exists."""
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)
        print(f"Created directory: {MODEL_PATH}")

if __name__ == '__main__':
    check_model_folder()
    update_llama_model()
