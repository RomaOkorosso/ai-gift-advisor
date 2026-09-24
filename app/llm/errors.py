class LLMError(Exception):
    """Base error for expected LLM failures; messages must not contain secrets."""


class LLMTimeoutError(LLMError):
    """The provider did not respond within the allowed time."""


class LLMUnavailableError(LLMError):
    """The provider is temporarily unavailable."""


class LLMRateLimitError(LLMError):
    """The provider rejected a request due to rate or quota limits."""


class LLMInvalidResponseError(LLMError):
    """The response is not valid JSON or does not match the contract."""


class LLMProviderError(LLMError):
    """Other provider API failures, such as invalid credentials."""
