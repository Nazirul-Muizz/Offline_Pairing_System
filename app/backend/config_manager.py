import os

class ConfigManager:
    def __init__(self, config_file='manual_config.txt'):
        self.config_file = config_file
        self.config_data = {
            'project': None,
            'line': None,
            'station': None,
        }
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config not found: {self.config_file}")
        
        with open(self.config_file, 'r', encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split('=', 1)
                self.config_data[key] = value

DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")
CONFIG_PATH = os.path.join(DESKTOP, "Offline_Pairing", "manual_config.txt")