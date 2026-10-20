from pathlib import Path

from src.agent import Agent

if __name__ == '__main__':
    config_path = Path('config/config.yaml')

    # TODO argparse here
    agent = Agent(config_path)

    print("Personal Agent. Type 'exit' to quit.")

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