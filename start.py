import os
import json
import logging
import traceback

# Setup debugging (logs to both console and file)
def setup_logging():
    logs_dir = os.path.join('logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'debug.log')

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    logging.info("Logging setup complete.")

def setup_directories():
    dirs = ['libs', 'logs', 'bugs', 'data']
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"Created directory: {directory}")

def load_config():
    config_path = 'data/config.klac'
    if not os.path.exists(config_path):
        logging.info("Config file not found. Creating default config.")
        default_config = {
            "version": "1.0",
            "libraries": ["html2epub", "html2mobi"],
            "logs_path": "logs/",
            "bugs_path": "bugs/"
        }
        with open(config_path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
            logging.info(f"Created default configuration at {config_path}")
        return default_config
    else:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

def main():
    try:
        setup_logging()
        logging.info("Starting setup...")
        setup_directories()

        config = load_config()
        logging.info(f"Config loaded: {config}")

        # You can insert more steps here for other application logic
        logging.info("Setup complete.")

    except Exception as e:
        logging.error("An error occurred during the setup process.")
        logging.error(traceback.format_exc())  # Detailed stack trace

if __name__ == "__main__":
    main()
