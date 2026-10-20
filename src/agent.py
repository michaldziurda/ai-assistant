import ollama

from src.config import Config
from tools.registry import TOOL_REGISTRY, TOOL_SCHEMAS

class Agent:
    def __init__(self, config_path:str):
        self.config = Config(config_path)#.get_config_dict()
        print(self.config)

        self.client = ollama.Client()
        self.model = self.config.model
        prompt = self.config.system_prompt
        self.messages = [{"role": "system", "content": prompt}] 

    def execute_tool(self, tool_name:str, arguments:dict):
        if tool_name not in TOOL_REGISTRY:
            raise ValueError(f"Unknown tool: {tool_name}")

        function = TOOL_REGISTRY[tool_name]
        return function(**arguments)

    def ask(self, user_input: str) -> str:
        self.messages.append({
            "role": "user",
            "content": user_input
        })

        for _ in range(10):
            response = self.client.chat(
                model=self.model,
                messages=self.messages,
                tools=TOOL_SCHEMAS
            )

            message = response.message
            self.messages.append(message) # This is where context is stored

            # If there is no tool calls in the message, return the final answer
            tool_calls = message.tool_calls or [] 
            if not tool_calls:
                return message.content or ""


            for call in tool_calls:
                tool_name = call.function.name
                arguments = call.function.arguments

                try:
                    result = self.execute_tool(tool_name, arguments)
                except Exception as e:
                    self.messages.append({
                        "role": "tool",
                        "content": f"Error: {e}"
                    })
                    continue

                self.messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": result

                })

        return "Reached the tool-call limit. Please try again."