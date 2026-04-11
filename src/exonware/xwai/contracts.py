#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/contracts.py
Protocol interfaces for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.3
Generation Date: 07-Jan-2025
"""

from __future__ import annotations
from typing import Any, Optional, Protocol, runtime_checkable, AsyncIterator
from .defs import ResponseFormat
@runtime_checkable

class IAIProvider(Protocol):
    """Interface for AI providers."""

    async def generate(
        self, 
        prompt: str, 
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> IAIResponse:
        """Generate AI response."""
        ...

    async def chat(
        self, 
        messages: list[dict[str, str]], 
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        **kwargs
    ) -> IAIResponse:
        """Chat with AI."""
        ...

    async def stream(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator['IAIResponse']:
        """Stream AI response in realtime."""
        ...
@runtime_checkable

class IAIResponse(Protocol):
    """Interface for AI responses."""
    @property

    def content(self) -> str:
        """Get response content."""
        ...
    @property

    def thinking(self) -> Optional[str]:
        """Get thinking/reasoning content if available."""
        ...
    @property

    def format(self) -> ResponseFormat:
        """Get response format."""
        ...
    @property

    def metadata(self) -> dict[str, Any]:
        """Get response metadata."""
        ...
    @property

    def attachments(self) -> list[dict[str, Any]]:
        """Get generated attachments/media."""
        ...
    @property

    def media(self) -> list[dict[str, Any]]:
        """Get generated media (images, audio, video, etc.)."""
        ...
@runtime_checkable

class IAIContext(Protocol):
    """Interface for AI context management."""

    def add_message(self, role: str, content: str) -> None:
        """Add message to context."""
        ...

    def get_messages(self) -> list[dict[str, str]]:
        """Get all messages in context."""
        ...

    def clear(self) -> None:
        """Clear context."""
        ...
@runtime_checkable

class ICommandInterpreter(Protocol):
    """Interface for command interpretation."""

    async def interpret(self, command: str) -> dict[str, Any]:
        """Interpret natural language command."""
        ...
