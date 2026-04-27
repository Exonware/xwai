#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/facade_tests/test_facade_provider_selection.py
Unit tests for XWAI provider selection logic.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

from typing import Any

import pytest

from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.facade import XWAI
from exonware.xwai.response import AIResponse


class _Provider:
    """Minimal async provider for deterministic unit tests."""

    def __init__(self, name: str) -> None:
        self.name = name

    async def generate(self, prompt: str, **kwargs: Any) -> AIResponse:
        return AIResponse(content=f"{self.name}:{prompt}")

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> AIResponse:
        return AIResponse(content=f"{self.name}:chat:{len(messages)}")

    async def stream(self, prompt: str, **kwargs: Any):
        yield AIResponse(content=f"{self.name}:stream:{prompt}")


@pytest.mark.xwai_unit
class TestFacadeProviderSelection:
    """Provider routing and default selection behavior."""

    def test_get_default_returns_first_registered_if_default_not_set(self):
        ai = XWAI()
        first = _Provider("first")
        ai.providers["first"] = first
        ai.providers["second"] = _Provider("second")

        assert ai.get_default_provider() is first

    def test_set_default_provider_requires_existing_provider(self):
        ai = XWAI()

        with pytest.raises(XWAIProviderError, match="Provider 'missing' not found"):
            ai.set_default_provider("missing")

    @pytest.mark.asyncio
    async def test_chat_raises_for_unknown_provider(self):
        ai = XWAI()
        ai.providers["known"] = _Provider("known")

        with pytest.raises(XWAIProviderError, match="Provider 'unknown' not found"):
            await ai.chat([{"role": "user", "content": "q"}], provider="unknown")

    @pytest.mark.asyncio
    async def test_stream_raises_when_no_provider_available(self):
        ai = XWAI()

        with pytest.raises(XWAIProviderError, match="No provider available"):
            async for _ in ai.stream("hello"):
                pass
