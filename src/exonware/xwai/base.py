#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/base.py
Abstract base classes for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.2
Generation Date: 07-Jan-2025
"""

from abc import ABC, abstractmethod
from typing import Any, Optional

from collections.abc import AsyncIterator
from .contracts import IAIProvider, IAIResponse, IAIContext, ICommandInterpreter
from .defs import ResponseFormat


class AAIProvider(IAIProvider, ABC):
    """Abstract base class for AI providers."""
    @abstractmethod

    async def generate(
        self, 
        prompt: str, 
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs
    ) -> IAIResponse:
        """Generate AI response."""
        pass
    @abstractmethod

    async def chat(
        self, 
        messages: list[dict[str, str]], 
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        **kwargs
    ) -> IAIResponse:
        """Chat with AI."""
        pass
    @abstractmethod

    async def stream(
        self,
        prompt: str,
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs
    ) -> AsyncIterator[IAIResponse]:
        """Stream AI response in realtime."""
        pass


class AAIResponse(IAIResponse, ABC):
    """Abstract base class for AI responses."""
    @property
    @abstractmethod

    def content(self) -> str:
        """Get response content."""
        pass
    @property
    @abstractmethod

    def thinking(self) -> str | None:
        """Get thinking/reasoning content if available."""
        pass
    @property
    @abstractmethod

    def format(self) -> ResponseFormat:
        """Get response format."""
        pass
    @property
    @abstractmethod

    def metadata(self) -> dict[str, Any]:
        """Get response metadata."""
        pass
    @property
    @abstractmethod

    def attachments(self) -> list[dict[str, Any]]:
        """Get generated attachments/media."""
        pass
    @property
    @abstractmethod

    def media(self) -> list[dict[str, Any]]:
        """Get generated media (images, audio, video, etc.)."""
        pass


class AAIContext(IAIContext, ABC):
    """Abstract base class for AI context management."""
    @abstractmethod

    def add_message(self, role: str, content: str) -> None:
        """Add message to context."""
        pass
    @abstractmethod

    def get_messages(self) -> list[dict[str, str]]:
        """Get all messages in context."""
        pass
    @abstractmethod

    def clear(self) -> None:
        """Clear context."""
        pass


class ACommandInterpreter(ICommandInterpreter, ABC):
    """Abstract base class for command interpretation."""
    @abstractmethod

    async def interpret(self, command: str) -> dict[str, Any]:
        """Interpret natural language command."""
        pass
