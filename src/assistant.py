from src.config import Config

class Assistant:
    def __init__(self, config_path:str):
        self.config = Config(config_path).get_config_dict()
        print(self.config)