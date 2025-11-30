import anthropic
from typing import List, Optional
from .base import AIProviderBase, Message, AIResponse
import logging

logger = logging.getLogger(__name__)


class AnthropicProvider(AIProviderBase):
    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022", temperature: float = 0.7, max_tokens: int = 4096):
        super().__init__(api_key, model, temperature, max_tokens)
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        try:
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                system=system_prompt or "",
                messages=formatted_messages,
            )

            return AIResponse(
                content=response.content[0].text,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                model=response.model,
                finish_reason=response.stop_reason,
                raw_response={
                    "id": response.id,
                    "type": response.type,
                    "role": response.role,
                    "content": [{"type": c.type, "text": c.text} for c in response.content],
                    "model": response.model,
                    "stop_reason": response.stop_reason,
                    "usage": {
                        "input_tokens": response.usage.input_tokens,
                        "output_tokens": response.usage.output_tokens
                    }
                }
            )

        except Exception as e:
            logger.error(f"Anthropic generation error: {str(e)}")
            raise

    def stream_generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        try:
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})

            with self.client.messages.stream(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                system=system_prompt or "",
                messages=formatted_messages,
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Anthropic streaming error: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        try:
            response = self.client.count_tokens(text)
            return response
        except Exception:
            return len(text.split()) * 1.3

    def health_check(self) -> bool:
        try:
            test_message = [Message(role="user", content="test")]
            self.generate(test_message, max_tokens=10)
            return True
        except Exception as e:
            logger.error(f"Anthropic health check failed: {str(e)}")
            return False
