
import os
import json
import logging

def setup_directories():
    dirs = ['libs', 'logs', 'bugs', 'data']
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def setup_logging():
    logs_dir = os.path.join('data', 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'startup.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Logging setup complete.")

def load_config():
    config_path = 'data/config.klac'
    if not os.path.exists(config_path):
        logging.info("Config file not found. Creating default config.")
        default_config = {
            "version": "1.0",
            "libraries": ["html2epub", "html2mobi"],
            "logs_path": "data/logs",
            "bugs_path": "data/bugs"
        }
        with open(config_path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
            logging.info(f"Created default configuration at {config_path}")
        return default_config
    else:
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

def setup():
    setup_directories()
    setup_logging()
    config = load_config()
    return config

if __name__ == "__main__":
    setup()

