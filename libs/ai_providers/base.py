from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str


@dataclass
class AIResponse:
    content: str
    tokens_used: int
    model: str
    finish_reason: str
    raw_response: Dict[str, Any]


class AIProviderBase(ABC):
    def __init__(self, api_key: str, model: str, temperature: float = 0.7, max_tokens: int = 4096):
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @abstractmethod
    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate a response from the AI model.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters

        Returns:
            AIResponse object containing the generated response
        """
        pass

    @abstractmethod
    def stream_generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        """
        Generate a streaming response from the AI model.

        Args:
            messages: List of conversation messages
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters

        Yields:
            Chunks of the generated response
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the provider is accessible and healthy.

        Returns:
            True if healthy, False otherwise
        """
        pass
