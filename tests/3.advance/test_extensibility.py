#!/usr/bin/env python3
"""
#exonware/xwai/tests/3.advance/test_extensibility.py
Advance extensibility tests for xwai.
Priority #5: Extensibility Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

from typing import Any

import pytest

from exonware.xwai.facade import XWAI
from exonware.xwai.response import AIResponse


class _CustomProvider:
    """Custom provider that demonstrates extensibility of the facade contract."""

    def __init__(self, prefix: str = "custom") -> None:
        self.prefix = prefix

    async def generate(self, prompt: str, **kwargs: Any) -> AIResponse:
        return AIResponse(content=f"{self.prefix}:{prompt}")

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> AIResponse:
        return AIResponse(content=f"{self.prefix}:chat:{len(messages)}")

    async def stream(self, prompt: str, **kwargs: Any):
        yield AIResponse(content=f"{self.prefix}:chunk:{prompt}")


@pytest.mark.xwai_advance
@pytest.mark.xwai_extensibility
class TestAIExtensibilityExcellence:
    """Validate custom provider integration without framework changes."""

    @pytest.mark.asyncio
    async def test_custom_provider_can_be_registered_and_used(self):
        ai = XWAI(default_provider="plugin")
        ai.providers["plugin"] = _CustomProvider(prefix="plugin")

        response = await ai.send_prompt("hello")

        assert response.content == "plugin:hello"

    @pytest.mark.asyncio
    async def test_custom_provider_stream_is_supported(self):
        ai = XWAI()
        ai.providers["plugin"] = _CustomProvider(prefix="plugin")

        chunks = [chunk.content async for chunk in ai.stream("go", provider="plugin")]

        assert chunks == ["plugin:chunk:go"]
