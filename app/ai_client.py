"""
AI Client Module - DeepSeek Integration

Provides a unified AI client interface using DeepSeek API (OpenAI-compatible).
"""

from openai import OpenAI
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """
    AI client using DeepSeek API.
    DeepSeek uses an OpenAI-compatible API format.
    """

    def __init__(self):
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError(
                "DEEPSEEK_API_KEY not found in environment variables. "
                "Please set it in .env file or environment."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7
    ) -> str:
        """
        Send a chat completion request to DeepSeek.

        Args:
            messages: List of message dicts with 'role' and 'content'
            system_prompt: Optional system prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            The assistant's response text
        """
        full_messages = []

        if system_prompt:
            full_messages.append({
                "role": "system",
                "content": system_prompt
            })

        full_messages.extend(messages)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"DeepSeek API error: {str(e)}")


# Singleton instance for easy import
_client_instance = None


def get_ai_client() -> AIClient:
    """Get or create the AI client singleton."""
    global _client_instance
    if _client_instance is None:
        _client_instance = AIClient()
    return _client_instance
