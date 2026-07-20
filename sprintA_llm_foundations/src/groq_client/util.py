import requests
from .exceptions import GroqAuthError, GroqBadRequestError, GroqRateLimitError, GroqServerError

def trim_history(messages: list[dict], max_turns:int) -> list[dict]:
    """Keep only the system message plus only the most recent max_turn user assistant pairs"""
    system_messages: list[dict] = [m for m in messages if m["role"] == "system"]
    conversations: list[dict] = [m for m in messages if m["role"] != "system"]
    trimmed_conversations: list[dict] = conversations[-(max_turns * 2):]
    return system_messages + trimmed_conversations

def _raise_for_status(response: requests.Response) -> None:
    """Translate an HTTP error status into a specific GroqAPIError subclass"""
    status = response.status_code
    if status == 401:
        raise GroqAuthError(response.text)
    if status == 400:
        raise GroqBadRequestError(response.text)
    if status == 429:
        raise GroqRateLimitError(response.text)
    if status >= 500:
        raise GroqServerError(response.text)
    response.raise_for_status()