import os
import math
from anthropic import Anthropic
from dotenv import load_dotenv
tools = [
    {
        "name": "calculator",
        "description": "Evaluates a math expression and returns the result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A math expression to evaluate, e.g. '2 + 2', '10 * (3 + 5)', 'sqrt(16)'"
                }
            },
            "required": ["expression"]
        }
    }
]

def calculator(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

def run_agent(client, history):
    while True:
        response = client.messages.create(
            model = "claude-haiku-4-5-20251001",
            tools = tools,
            max_tokens = 1000,
            messages = history
        )
        if response.stop_reason == "tool_use":
            history.append({"role" : "assistant", "content": response.content})
            for block in response.content:
                if block.type == "tool_use":
                    expression = block.input["expression"]
                    output = calculator(expression)
                    history.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": output
                        }]
                    })
        elif response.stop_reason == "end_turn":
            reply = response.content[0].text
            history.append({"role": "assistant", "content": reply})
            print(f"Assistant: {reply}\n")
            break
def main():
    load_dotenv()
    client = Anthropic(api_key = os.getenv("api_key"))
    history = []
    while True:
        try:
            user_input = input("You: ").strip()
        except(EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if user_input.lower() == "quit":
            print("Goodbye!\n")
            break
        if user_input.lower() == "clear":
            history = []
            continue
        history.append({"role": "user", "content" : user_input})
        try:
            run_agent(client, history)
        except Exception as e:
            print(f"Error: {e}")
if __name__ == "__main__":
    main()    