#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/providers_tests/test_gpt_api_level.py
API-level unit tests for GPTProvider request/response behavior.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from exonware.xwai.defs import ResponseFormat
from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.providers.gpt import GPTProvider
from exonware.xwai.response import AIResponse


def _build_gpt_provider_with_client(client: object) -> GPTProvider:
    provider = GPTProvider.__new__(GPTProvider)
    provider._client = client
    provider._model = "gpt-4"
    return provider


@pytest.mark.xwai_unit
class TestGPTProviderAPI:
    """Validate GPTProvider API behavior without network calls."""

    @pytest.mark.asyncio
    async def test_generate_uses_responses_api_and_json_format(self):
        calls: dict[str, object] = {}

        class _Responses:
            def create(self, **kwargs):
                calls["kwargs"] = kwargs
                return SimpleNamespace(output_text='```json\n{"ok": true}\n```')

        client = SimpleNamespace(responses=_Responses())
        provider = _build_gpt_provider_with_client(client)

        result = await provider.generate("hello", response_format=ResponseFormat.JSON)

        assert isinstance(result, AIResponse)
        assert result.content == '{"ok": true}'
        assert result.format == ResponseFormat.JSON
        assert calls["kwargs"]["model"] == "gpt-4"
        assert "Return the result in JSON format only." in calls["kwargs"]["input"]

    @pytest.mark.asyncio
    async def test_generate_uses_chat_completions_branch(self):
        usage = SimpleNamespace(prompt_tokens=11, completion_tokens=7, total_tokens=18)
        message = SimpleNamespace(content="done", reasoning_content="think")
        choice = SimpleNamespace(message=message)
        response = SimpleNamespace(choices=[choice], usage=usage)
        calls: dict[str, object] = {}

        class _Completions:
            def create(self, **kwargs):
                calls["kwargs"] = kwargs
                return response

        client = SimpleNamespace(chat=SimpleNamespace(completions=_Completions()))
        provider = _build_gpt_provider_with_client(client)

        result = await provider.generate("hello", temperature=0.1, max_tokens=123)

        assert result.content == "done"
        assert result.thinking == "think"
        assert result.metadata["usage"]["total_tokens"] == 18
        assert calls["kwargs"]["temperature"] == 0.1
        assert calls["kwargs"]["max_tokens"] == 123

    @pytest.mark.asyncio
    async def test_chat_formats_messages_and_returns_text(self):
        usage = SimpleNamespace(prompt_tokens=3, completion_tokens=5, total_tokens=8)
        response = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))], usage=usage)
        calls: dict[str, object] = {}

        class _Completions:
            def create(self, **kwargs):
                calls["kwargs"] = kwargs
                return response

        client = SimpleNamespace(chat=SimpleNamespace(completions=_Completions()))
        provider = _build_gpt_provider_with_client(client)

        result = await provider.chat(
            messages=[{"role": "user", "content": "hello"}],
            attachments=[{"url": "https://example.test/image.png"}],
        )

        assert result.content == "ok"
        payload_messages = calls["kwargs"]["messages"]
        assert payload_messages[0]["role"] == "user"
        assert isinstance(payload_messages[0]["content"], list)
        assert payload_messages[0]["content"][0]["text"] == "hello"

    @pytest.mark.asyncio
    async def test_stream_yields_chunked_responses(self):
        chunk1 = SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="A"))])
        chunk2 = SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="B"))])

        class _Completions:
            def create(self, **kwargs):
                return [chunk1, chunk2]

        client = SimpleNamespace(chat=SimpleNamespace(completions=_Completions()))
        provider = _build_gpt_provider_with_client(client)

        chunks = [item async for item in provider.stream("hello")]

        assert [c.content for c in chunks] == ["A", "B"]
        assert chunks[-1].metadata["accumulated"] == "AB"
        assert chunks[-1].metadata["streaming"] is True

    @pytest.mark.asyncio
    async def test_generate_wraps_unknown_errors(self):
        class _Completions:
            def create(self, **kwargs):
                raise RuntimeError("boom")

        client = SimpleNamespace(chat=SimpleNamespace(completions=_Completions()))
        provider = _build_gpt_provider_with_client(client)

        with pytest.raises(XWAIProviderError, match="Failed to generate response"):
            await provider.generate("hello")
