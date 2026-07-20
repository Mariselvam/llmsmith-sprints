"""
This module provides functions to interact with the Groq API for generating responses from a language model.
"""

import requests
import json
from typing import Iterator
from .util import _raise_for_status


def get_response(messages: list[dict], model: str, headers: dict) -> str:
    """
    Sends a request to the Groq API and returns the response as a string.
    """

    url = get_api_url()
    payload = construct_payload(messages, model)
    response = requests.post(url, headers=headers, json=payload)
    _raise_for_status(response=response)
    json_response = response.json()
    return json_response["choices"][0]["message"]["content"]


def stream_response(messages: list[dict], model: str, headers: dict) -> Iterator[str]:
    """
    Streams the response from the Groq API, yielding chunks of text as they are received.
    """

    url = get_api_url()
    payload = construct_payload(messages, model, streaming=True)
    with requests.post(url, headers=headers, json=payload, stream=True) as response:
        _raise_for_status(response=response)
        for line in response.iter_lines():
            if not line:
                continue
            decoded_line = line.decode("utf-8")
            if decoded_line == "data: [DONE]":
                break
            if decoded_line.startswith("data: "):
                chunk = decoded_line[len("data: ") :].strip()
                data_chunk = json.loads(chunk)
                delta = data_chunk["choices"][0]["delta"].get("content")
                if delta:
                    yield delta


def construct_payload(
    messages: list[dict], model: str, streaming: bool = False
) -> dict:
    """
    Constructs the payload for the API request.
    """
    payload = {"model": model, "messages": messages, "stream": streaming}
    return payload


def get_api_url() -> str:
    """
    Returns the API URL for the Groq API.
    """
    return "https://api.groq.com/openai/v1/chat/completions"
