#!/usr/bin/env python3
"""
#exonware/xwai/tests/2.integration/test_integration_facade_workflow.py
Integration tests for end-to-end XWAI facade workflows with in-memory providers.
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


class _ScenarioProvider:
    """Stateful provider used to validate realistic multi-call flow."""

    def __init__(self, name: str):
        self.name = name
        self.history: list[str] = []

    async def generate(
        self,
        prompt: str,
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs: Any,
    ) -> AIResponse:
        self.history.append(f"generate:{prompt}")
        return AIResponse(
            content=f"{self.name}:gen:{prompt}",
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
        self.history.append(f"chat:{len(messages)}")
        return AIResponse(content=f"{self.name}:chat:{messages[-1]['content']}")

    async def stream(
        self,
        prompt: str,
        attachments: list[str | bytes | dict[str, Any]] | None = None,
        system_instruction: str | None = None,
        **kwargs: Any,
    ):
        self.history.append(f"stream:{prompt}")
        yield AIResponse(content=f"{self.name}:stream:1")
        yield AIResponse(content=f"{self.name}:stream:2")


@pytest.mark.xwai_integration
class TestFacadeIntegrationWorkflow:
    """Cross-method facade behavior with provider state."""

    @pytest.mark.asyncio
    async def test_send_chat_stream_workflow(self):
        ai = XWAI(default_provider="alpha")
        provider = _ScenarioProvider("alpha")
        ai.providers["alpha"] = provider

        send = await ai.send_prompt(
            "summarize",
            attachments=[{"url": "https://example.test/image.png"}],
            system_instruction="be concise",
        )
        chat = await ai.chat(
            [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "hi"},
                {"role": "user", "content": "status?"},
            ]
        )
        chunks = [chunk async for chunk in ai.stream("stream please")]

        assert send.content == "alpha:gen:summarize"
        assert send.metadata["attachments_count"] == 1
        assert send.metadata["system_instruction"] == "be concise"
        assert chat.content == "alpha:chat:status?"
        assert [c.content for c in chunks] == ["alpha:stream:1", "alpha:stream:2"]
        assert provider.history == ["generate:summarize", "chat:3", "stream:stream please"]

    @pytest.mark.asyncio
    async def test_multi_provider_override_routing(self):
        ai = XWAI(default_provider="alpha")
        alpha = _ScenarioProvider("alpha")
        beta = _ScenarioProvider("beta")
        ai.providers["alpha"] = alpha
        ai.providers["beta"] = beta

        default_response = await ai.send_prompt("one")
        override_response = await ai.send_prompt("two", provider="beta")

        assert default_response.content == "alpha:gen:one"
        assert override_response.content == "beta:gen:two"
        assert alpha.history == ["generate:one"]
        assert beta.history == ["generate:two"]
