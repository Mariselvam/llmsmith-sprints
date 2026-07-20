"""Exception hierarchy for Groq client API errors"""


class GroqAPIError(Exception):
    """Base exception for all Groq API client errors"""


class GroqAuthError(GroqAPIError):
    """Raised on 401 - invalid or missing API key"""


class GroqBadRequestError(GroqAPIError):
    """Raised on 400 - malformed request (bad payload, invalid model, etc)"""


class GroqRateLimitError(GroqAPIError):
    """Raised on 429 - rate limit exceeded"""


class GroqServerError(GroqAPIError):
    """Raised on 5xx - Groq's server had a problem"""
