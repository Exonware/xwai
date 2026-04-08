#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/response.py
AI Response implementation for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.0
Generation Date: 07-Jan-2025
"""

from typing import Any
from .base import AAIResponse
from .defs import ResponseFormat


class AIResponse(AAIResponse):
    """Concrete implementation of AI response."""

    def __init__(
        self,
        content: str,
        format: ResponseFormat = ResponseFormat.TEXT,
        thinking: str | None = None,
        metadata: dict[str, Any] | None = None,
        attachments: list[dict[str, Any]] | None = None,
        media: list[dict[str, Any]] | None = None,
    ):
        """
        Initialize AI response.
        Args:
            content: Response content text
            format: Response format (TEXT, JSON, MARKDOWN)
            thinking: Optional thinking/reasoning content
            metadata: Optional metadata dictionary
            attachments: Optional list of generated attachments
            media: Optional list of generated media
        """
        self._content = content
        self._format = format
        self._thinking = thinking
        self._metadata = metadata or {}
        self._attachments = attachments or []
        self._media = media or []
    @property

    def content(self) -> str:
        """Get response content."""
        return self._content
    @property

    def thinking(self) -> str | None:
        """Get thinking/reasoning content if available."""
        return self._thinking
    @property

    def format(self) -> ResponseFormat:
        """Get response format."""
        return self._format
    @property

    def metadata(self) -> dict[str, Any]:
        """Get response metadata."""
        return self._metadata
    @property

    def attachments(self) -> list[dict[str, Any]]:
        """Get generated attachments/media."""
        return self._attachments
    @property

    def media(self) -> list[dict[str, Any]]:
        """Get generated media (images, audio, video, etc.)."""
        return self._media

    def to_dict(self) -> dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "content": self._content,
            "thinking": self._thinking,
            "format": self._format.value,
            "metadata": self._metadata,
            "attachments": self._attachments,
            "media": self._media,
        }
