from pathlib import Path
import argparse

from src.agent import Agent

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--model", type=str)
    parser.add_argument("--agent-name", type=str)
    #parser.add_argument("--speak", action="store_true")
    args = parser.parse_args()

    config_path = Path('config/config.yaml')
    agent = Agent(config_path)

    # If CLI args were passed, override config
    agent.config.override_config_vals(vars(args))

    while True:
        try:
            user_input = input("\n> ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input: 
                continue

            answer = agent.ask(user_input)
            print(f"\n{answer}")

        except KeyboardInterrupt:
            print("Session terminated")
            break