import requests
from typing import List, Optional
from .base import AIProviderBase, Message, AIResponse
import logging

logger = logging.getLogger(__name__)


class OllamaProvider(AIProviderBase):
    def __init__(
        self,
        api_key: str = "",
        model: str = "llama2",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        api_url: str = "http://localhost:11434"
    ):
        super().__init__(api_key, model, temperature, max_tokens)
        self.api_url = api_url.rstrip('/')

    def generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        try:
            formatted_messages = []

            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})

            for msg in messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})

            response = requests.post(
                f"{self.api_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": formatted_messages,
                    "stream": False,
                    "options": {
                        "temperature": kwargs.get('temperature', self.temperature),
                        "num_predict": kwargs.get('max_tokens', self.max_tokens),
                    }
                },
                timeout=120
            )

            response.raise_for_status()
            data = response.json()

            return AIResponse(
                content=data['message']['content'],
                tokens_used=data.get('prompt_eval_count', 0) + data.get('eval_count', 0),
                model=self.model,
                finish_reason=data.get('done_reason', 'stop'),
                raw_response=data
            )

        except Exception as e:
            logger.error(f"Ollama generation error: {str(e)}")
            raise

    def stream_generate(
        self,
        messages: List[Message],
        system_prompt: Optional[str] = None,
        **kwargs
    ):
        try:
            formatted_messages = []

            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})

            for msg in messages:
                formatted_messages.append({"role": msg.role, "content": msg.content})

            response = requests.post(
                f"{self.api_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": formatted_messages,
                    "stream": True,
                    "options": {
                        "temperature": kwargs.get('temperature', self.temperature),
                        "num_predict": kwargs.get('max_tokens', self.max_tokens),
                    }
                },
                stream=True,
                timeout=120
            )

            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    if 'message' in data and 'content' in data['message']:
                        yield data['message']['content']

        except Exception as e:
            logger.error(f"Ollama streaming error: {str(e)}")
            raise

    def count_tokens(self, text: str) -> int:
        return len(text.split()) * 1.3

    def health_check(self) -> bool:
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return False
