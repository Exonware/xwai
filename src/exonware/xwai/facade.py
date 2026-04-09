#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/facade.py
XWAI Facade - Main Public API
This module provides the main public API for xwai following GUIDE_DEV.md facade pattern.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.2
Generation Date: 07-Jan-2025
"""

from typing import Optional, Any
from .base import AAIProvider
from .response import AIResponse
from .config import XWAIConfig
from .defs import AIProviderType, AIModelType
from .errors import XWAIError, XWAIProviderError
from exonware.xwsystem import get_logger
logger = get_logger(__name__)


class XWAI:
    """
    Main XWAI class providing AI integration for the eXonware ecosystem.
    This class implements the facade pattern, providing a unified interface
    for multiple AI providers, natural language processing, and command interpretation.
    Usage:
        >>> ai_agent = XWAI()
        >>> ai_agent.providers["gemini"] = GeminiProvider("api_token", "gemini-1.5-pro")
        >>> ai_agent.providers["gpt"] = GPTProvider("api_token", "gpt-4")
        >>> answer = await ai_agent.send_prompt("Hello, world!", attachments=[...])
    """

    def __init__(
        self,
        default_provider: Optional[str] = None,
        **options
    ):
        """
        Initialize XWAI.
        Args:
            default_provider: Optional default provider name to use
            **options: Additional configuration options
        """
        self._providers: dict[str, AAIProvider] = {}
        self._default_provider = default_provider
        self._config = XWAIConfig(**options)
        logger.info("Initialized XWAI with provider management")
    @property

    def providers(self) -> dict[str, AAIProvider]:
        """
        Get providers dictionary.
        Returns:
            Dictionary of provider name to AAIProvider instance
        """
        return self._providers

    def set_default_provider(self, provider_name: str) -> None:
        """
        Set default provider.
        Args:
            provider_name: Name of the provider to use as default
        """
        if provider_name not in self._providers:
            raise XWAIProviderError(f"Provider '{provider_name}' not found")
        self._default_provider = provider_name
        logger.info(f"Set default provider to: {provider_name}")

    def get_default_provider(self) -> Optional[AAIProvider]:
        """
        Get default provider.
        Returns:
            Default AAIProvider instance or None
        """
        if self._default_provider and self._default_provider in self._providers:
            return self._providers[self._default_provider]
        elif self._providers:
            # Return first available provider
            return next(iter(self._providers.values()))
        return None

    async def send_prompt(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        provider: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Send prompt to AI provider and get response.
        Args:
            prompt: Input prompt text
            attachments: Optional list of attachments (file paths, bytes, or dicts)
            provider: Optional provider name (uses default if not specified)
            system_instruction: Optional system instruction
            **kwargs: Additional parameters to pass to provider
        Returns:
            AIResponse object with content, thinking, attachments, media, etc.
        Raises:
            XWAIProviderError: If no provider is available or provider not found
        """
        # Determine which provider to use
        provider_instance = None
        if provider:
            if provider not in self._providers:
                raise XWAIProviderError(f"Provider '{provider}' not found. Available: {list(self._providers.keys())}")
            provider_instance = self._providers[provider]
        else:
            provider_instance = self.get_default_provider()
            if not provider_instance:
                raise XWAIProviderError("No provider available. Add a provider first using providers['name'] = Provider(...)")
        logger.debug(f"Using provider: {provider or 'default'} for prompt")
        # Generate response
        try:
            response = await provider_instance.generate(
                prompt=prompt,
                attachments=attachments,
                system_instruction=system_instruction,
                **kwargs
            )
            return response
        except Exception as e:
            raise XWAIProviderError(f"Failed to send prompt: {e}") from e

    async def chat(
        self,
        messages: list[dict[str, str]],
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        provider: Optional[str] = None,
        **kwargs
    ) -> AIResponse:
        """
        Chat with AI using message history.
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            attachments: Optional list of attachments
            provider: Optional provider name (uses default if not specified)
            **kwargs: Additional parameters
        Returns:
            AIResponse object
        """
        provider_instance = None
        if provider:
            if provider not in self._providers:
                raise XWAIProviderError(f"Provider '{provider}' not found")
            provider_instance = self._providers[provider]
        else:
            provider_instance = self.get_default_provider()
            if not provider_instance:
                raise XWAIProviderError("No provider available")
        try:
            response = await provider_instance.chat(
                messages=messages,
                attachments=attachments,
                **kwargs
            )
            return response
        except Exception as e:
            raise XWAIProviderError(f"Failed to chat: {e}") from e

    async def stream(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        provider: Optional[str] = None,
        system_instruction: Optional[str] = None,
        **kwargs
    ):
        """
        Stream AI response in realtime.
        Args:
            prompt: Input prompt text
            attachments: Optional list of attachments
            provider: Optional provider name (uses default if not specified)
            system_instruction: Optional system instruction
            **kwargs: Additional parameters
        Yields:
            AIResponse objects as chunks arrive
        """
        provider_instance = None
        if provider:
            if provider not in self._providers:
                raise XWAIProviderError(f"Provider '{provider}' not found")
            provider_instance = self._providers[provider]
        else:
            provider_instance = self.get_default_provider()
            if not provider_instance:
                raise XWAIProviderError("No provider available")
        try:
            async for chunk in provider_instance.stream(
                prompt=prompt,
                attachments=attachments,
                system_instruction=system_instruction,
                **kwargs
            ):
                yield chunk
        except Exception as e:
            raise XWAIProviderError(f"Failed to stream: {e}") from e
