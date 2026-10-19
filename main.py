import os
import argparse
import json
import sys

from dotenv import load_dotenv
from openai import OpenAI
from functions.prompts import system_prompt
from functions.call_function import available_functions, call_function
from config import LOOP_ITERATIONS

def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    verbose = args.verbose

    for _ in range(LOOP_ITERATIONS):
        try:
            is_final_response = generate_content(client, messages, verbose)
            if is_final_response:
                return None
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"No result after maximum {LOOP_ITERATIONS} loop iterations")
    sys.exit(1)

def generate_content(client: OpenAI, messages: list, verbose: bool) -> bool:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("Error in generating response")

    if verbose:
        print(f"User prompt: {messages[-1]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print("Response:")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        print(message.content)
        return True

    else:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name} "
                  f"({function_args})")
            result_message = call_function(tool_call, verbose)
            messages.append(result_message)
            if result_message["content"] is None:
                raise Exception()
            if verbose:
                print(f"-> {result_message['content']}")
        return False

if __name__ == "__main__":
    main()
