"""
This script demonstrates how to use the llm_api_client module to interact with the Groq API for generating responses from a language model.
It provides examples of both synchronous and streaming requests.
"""

from dotenv import load_dotenv
import os
from groq_client import stream_response, Config, trim_history

load_dotenv()


def main() -> None:
    API_KEY = os.getenv("GROQ_API_KEY")
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    config_object = Config()
    messages = [{"role": "system", "content": config_object.system_prompt}]

    while True:
        assistant_reply: str = ""
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": user_input})
        trimmed_conv_history = trim_history(
            messages=messages, max_turns=config_object.max_history_turns
        )
        for chunk in stream_response(
            trimmed_conv_history, config_object.model, headers
        ):
            print(chunk, end="", flush=True)
            assistant_reply += chunk
        print()
        messages.append({"role": "assistant", "content": assistant_reply})


if __name__ == "__main__":
    main()
