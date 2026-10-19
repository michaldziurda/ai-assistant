from ollama import chat

# 1. Definiujemy prostą funkcję matematyczną
def dodaj_liczby(a: int, b: int) -> int:
    return a + b

# 2. Wysyłamy zapytanie do Ollama z opisem tego narzędzia
response = chat(
    model="llama3.1:8b",  # Upewnij się, że ten model obsługuje tools (np. llama3, llama3.1, mistral)
    messages=[
        {"role": "user", "content": "Ile to jest 250 plus 370?"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "dodaj_liczby",
                "description": "Dodaje dwie liczby całkowite do siebie",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "integer", "description": "Pierwsza liczba"},
                        "b": {"type": "integer", "description": "Druga liczba"}
                    },
                    "required": ["a", "b"]
                }
            }
        }
    ]
)

# 3. Sprawdzamy wynik walidacji i reakcję modelu
print("--- PEŁNA ODPOWIEDŹ OLLAMA ---")
print(response)

print("\n--- CZY MODEL CHCE WYWOŁAĆ FUNKCJĘ? ---")
if "tool_calls" in response["message"] and response["message"]["tool_calls"]:
    for call in response["message"]["tool_calls"]:
        print(f" Sukces! Model chce wywołać funkcję: {call['function']['name']}")
        print(f" Przekazane argumenty: {call['function']['arguments']}")
else:
    print("❌ Model odpowiedział zwykłym tekstem zamiast wywołać funkcję.")

#response = chat(model="llama3.1:8b", messages=messages, tools=tools, think=True) 
#print(response)