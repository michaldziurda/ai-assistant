from pathlib import Path

from src.assistant import Assistant

if __name__ == '__main__':
    config_path = Path('config/config.yaml')

    # TODO argparse here
    assistant = Assistant(config_path)
    print(assistant.config)