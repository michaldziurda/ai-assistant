import yaml
from pathlib import Path

class Config:
    def __init__(self, config_file=None, data=None):
        self.config_dict = dict()
        self.config_file_path = config_file
        
        if config_file is not None:
            self.from_yaml(config_file)
        elif data is not None:
            self.from_dict(data)

    def from_yaml(self, config_file: str):
        with open(Path(config_file), "r", encoding="utf-8") as f:
            yml = yaml.safe_load(f)
        self.config_dict = yml
        self.update_attrs(yml)

    def from_dict(self, data: dict):
        self.config_dict = data
        self.update_attrs(data)

    def update_attrs(self, data: dict):
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively create Config for nested dicts
                setattr(self, key, Config(data=value))
            elif isinstance(value, list):
                # Convert dicts inside list to Config objects
                processed = [
                    Config(data=item) if isinstance(item, dict) else item
                    for item in value
                ]
                setattr(self, key, processed)
            else:
                setattr(self, key, value)

    def override_config_vals(self, new_data:dict):
        self.config_dict.update({k: v for k, v in new_data.items() if v is not None})

    def get_config_dict(self):
        return self.config_dict
    