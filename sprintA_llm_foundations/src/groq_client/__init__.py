""" A hand-built HTTP client for the Groq chat completions API"""

from .client import get_response, stream_response
from .util import trim_history
from .config import Config
from .exceptions import (
    GroqAPIError,
    GroqServerError, 
    GroqAuthError, 
    GroqBadRequestError, 
    GroqRateLimitError 
)

__all__ = [
    "get_response",
    "stream_response",
    "trim_history",
    "Config",
    "GroqAPIError",
    "GroqServerError", 
    "GroqAuthError", 
    "GroqBadRequestError", 
    "GroqRateLimitError"
]
