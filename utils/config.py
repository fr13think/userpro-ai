import yaml
import os

def load_config():
    config_path = os.environ.get('CONFIG_PATH', 'config.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)