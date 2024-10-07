import json
from src.assistant.llama import LlamaModel
from src.assistant.bloom import BloomModel
# Add imports for additional models like CodeLlama, Code-X here

# Helper function to load the configuration from preferences.klac
def load_preferences(config_file="UserData/preferences.klac"):
    """
    Loads the AI assistant configuration from the specified file.
    
    :param config_file: Path to the configuration file (default: "UserData/preferences.klac")
    :return: Dictionary containing configuration settings
    """
    with open(config_file, 'r') as f:
        return json.load(f)

# Helper function to check if assistant functionality is enabled
def is_assistant_enabled(config):
    """
    Checks whether the assistant is enabled based on the configuration.
    
    :param config: Dictionary containing configuration settings
    :return: Boolean indicating if the assistant is enabled (True/False)
    """
    return config.get('active_config', {}).get('assistant_enabled', False)

# Main class to handle AI-related tasks in the application
class AssistantHandler:
    def __init__(self, config_file="UserData/preferences.klac"):
        """
        Initializes the AssistantHandler class.
        
        :param config_file: Path to the configuration file
        """
        # Load configuration file during initialization
        self.config = load_preferences(config_file)
        self.model = None  # Placeholder for the model instance (LLaMA, BLOOM, etc.)

    def load_model(self):
        """
        Loads the appropriate AI model based on the active configuration. 
        Checks whether the assistant is enabled, and loads the correct model
        (LLaMA, BLOOM, CodeLlama, Code-X, etc.) depending on the `active_config`.
        """
        # Verify if the assistant is enabled before proceeding
        if not is_assistant_enabled(self.config):
            print("Assistant is disabled in the configuration.")
            return None
        
        # Determine the active model from the configuration
        model_name = self.config['active_config']['model']

        # Load the appropriate model based on the model name
        if "LLaMA" in model_name:
            print(f"Loading LLaMA model: {model_name}")
            self.model = LlamaModel(self.config)  # Use LLaMA-specific handler
            self.model.load_model()

        elif "BLOOM" in model_name:
            print(f"Loading BLOOM model: {model_name}")
            self.model = BloomModel(self.config)  # Use BLOOM-specific handler
            self.model.load_model()

        elif "CodeLlama" in model_name:
            print(f"Loading CodeLlama model: {model_name}")
            # Initialize and load CodeLlama handler (to be implemented)
            # self.model = CodeLlamaModel(self.config)
            # self.model.load_model()

        elif "Code-X" in model_name:
            print(f"Loading Code-X model: {model_name}")
            # Initialize and load Code-X handler (to be implemented)
            # self.model = CodeXModel(self.config)
            # self.model.load_model()

        else:
            print(f"Model '{model_name}' not recognized.")
            return None

    def perform_task(self, task_type, prompt):
        """
        Executes the specified task type (e.g., 'generate_text') using the loaded model.
        
        :param task_type: The type of task to perform (e.g., 'generate_text')
        :param prompt: The input prompt for the model
        :return: Output from the model (text generation or other task result)
        """
        # Ensure a model is loaded before attempting to perform a task
        if not self.model:
            print("No model is loaded. Please load a model first.")
            return None
        
        # Handle different task types
        if task_type == "generate_text":
            return self.model.generate_text(prompt)
        
        # Future task types (e.g., code generation, summarization) can be added here
        else:
            print(f"Task '{task_type}' is not recognized.")
            return None

# Example usage for production:
if __name__ == "__main__":
    # Initialize the assistant handler
    assistant = AssistantHandler()
    
    # Load the appropriate model based on the active configuration
    assistant.load_model()

    # Example of generating text using the loaded model
    task_output = assistant.perform_task("generate_text", "Write a Python function to add two numbers.")
    
    # Output the generated result
    print(task_output)
