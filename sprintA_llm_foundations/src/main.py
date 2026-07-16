"""
This script demonstrates how to use the llm_api_client module to interact with the Groq API for generating responses from a language model. 
It provides examples of both synchronous and streaming requests.
"""
from dotenv import load_dotenv
import os
from llm_api_client import get_response, stream_response

load_dotenv()

def main():
    API_KEY = os.getenv('GROQ_API_KEY')
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"      
    }
    prompt_sync_request = "Write a short story about a cat"
    prompt_stream_request = "Write a short story about a dog"
    model = "llama-3.1-8b-instant"
    print("Starting the request...")
    sync_response = get_response(prompt_sync_request, model, headers)
    print("Synchronous response:")
    print(sync_response)
    print("\nStreaming response:")
    for chunk in stream_response(prompt_stream_request, model, headers):
        print(chunk, end="", flush=True)
    print()

if __name__ == "__main__":
    main() 