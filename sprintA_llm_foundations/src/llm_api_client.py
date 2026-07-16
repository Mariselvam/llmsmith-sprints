"""
This module provides functions to interact with the Groq API for generating responses from a language model.
"""
import requests
import json
from typing import Iterator

def get_response(prompt: str, model: str, headers: dict) -> str:
    """
    Sends a request to the Groq API and returns the response as a string.
    """

    url = get_api_url()
    payload = construct_payload(prompt, model)
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    json_response = response.json()
    return json_response["choices"][0]["message"]["content"]

def stream_response(prompt: str, model: str, headers: dict) -> Iterator[str]:
    """
    Streams the response from the Groq API, yielding chunks of text as they are received.
    """

    url = get_api_url()
    payload = construct_payload(prompt, model, streaming=True)
    with requests.post(url, headers=headers, json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            decoded_line = line.decode('utf-8')
            if decoded_line == "data: [DONE]":
                break
            if decoded_line.startswith("data: "):
                chunk = decoded_line[len("data: "):].strip()
                data_chunk = json.loads(chunk)
                delta = data_chunk["choices"][0]["delta"].get("content")
                if delta:
                    yield delta
                
def construct_payload(prompt: str, model: str , streaming: bool = False) -> dict:
    """
    Constructs the payload for the API request.
    """
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": streaming
    }
    return payload

def get_api_url() -> str:
    """
    Returns the API URL for the Groq API.
    """
    return "https://api.groq.com/openai/v1/chat/completions"    