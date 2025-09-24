import json
import os

class ConfigLoader:
    def __init__(self, config_file="settings.json"):
        self.config_file = config_file
        self.config_data = self.load_config()
        self._set_attributes()
    
    def load_config(self):
        """Load configuration file from disk"""
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Configuration file {self.config_file} does not exist")
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Configuration file {self.config_file} has invalid format")
    
    def _set_attributes(self):
        """Set configuration items as object attributes using setattr"""
        if self.config_data and isinstance(self.config_data, dict):
            for key, value in self.config_data.items():
                setattr(self, key, value)
    
    def get(self, key, default=None):
        """Get configuration value by key"""
        return self.config_data.get(key, default)




#parse migrated IP

