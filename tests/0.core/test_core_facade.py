#!/usr/bin/env python3
"""
#exonware/xwai/tests/0.core/test_core_facade.py
Core facade tests for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

from __future__ import annotations

from typing import Any

import pytest

from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.facade import XWAI
from exonware.xwai.response import AIResponse


class _FakeProvider:
    """Simple async provider used for facade behavior tests."""

    def __init__(self, name: str):
        self.name = name

    async def generate(
        self,
        prompt: str,
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs: Any,
    ) -> AIResponse:
        return AIResponse(
            content=f"{self.name}:{prompt}",
            metadata={
                "attachments_count": len(attachments or []),
                "system_instruction": system_instruction,
            },
        )

    async def chat(
        self,
        messages: list[dict[str, str]],
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> AIResponse:
        return AIResponse(content=f"{self.name}:chat:{len(messages)}")

    async def stream(
        self,
        prompt: str,
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs: Any,
    ):
        yield AIResponse(content=f"{self.name}:chunk-1:{prompt}")
        yield AIResponse(content=f"{self.name}:chunk-2:{prompt}")


@pytest.mark.xwai_core
class TestCoreFacade:
    """Test core facade functionality."""

    def test_xwai_initialization(self):
        """XWAI initializes with empty provider registry and config."""
        ai = XWAI()

        assert ai is not None
        assert ai.providers == {}
        assert ai.get_default_provider() is None
        assert ai._config is not None

    @pytest.mark.asyncio
    async def test_send_prompt_uses_registered_default_provider(self):
        """send_prompt should route to default provider and return AIResponse."""
        ai = XWAI()
        provider = _FakeProvider("alpha")
        ai.providers["alpha"] = provider
        ai.set_default_provider("alpha")

        response = await ai.send_prompt("hello")

        assert isinstance(response, AIResponse)
        assert response.content == "alpha:hello"

    @pytest.mark.asyncio
    async def test_send_prompt_supports_explicit_provider_override(self):
        """Explicit provider argument should override default provider routing."""
        ai = XWAI()
        ai.providers["alpha"] = _FakeProvider("alpha")
        ai.providers["beta"] = _FakeProvider("beta")
        ai.set_default_provider("alpha")

        response = await ai.send_prompt("hello", provider="beta")

        assert response.content == "beta:hello"

    @pytest.mark.asyncio
    async def test_send_prompt_without_providers_raises_provider_error(self):
        """Calling send_prompt with no configured providers should fail fast."""
        ai = XWAI()

        with pytest.raises(XWAIProviderError, match="No provider available"):
            await ai.send_prompt("hello")

    @pytest.mark.asyncio
    async def test_chat_and_stream_delegate_to_provider(self):
        """chat and stream should delegate and preserve provider output chunks."""
        ai = XWAI()
        ai.providers["alpha"] = _FakeProvider("alpha")

        chat_response = await ai.chat([{"role": "user", "content": "q"}], provider="alpha")
        chunks = [chunk async for chunk in ai.stream("hi", provider="alpha")]

        assert chat_response.content == "alpha:chat:1"
        assert [chunk.content for chunk in chunks] == ["alpha:chunk-1:hi", "alpha:chunk-2:hi"]
