#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/providers_tests/test_gemini_api_level.py
API-level unit tests for GeminiProvider request/response behavior.
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
from exonware.xwai.providers.gemini import GeminiProvider
from exonware.xwai.response import AIResponse


def _build_gemini_provider_with_client(client: object) -> GeminiProvider:
    provider = GeminiProvider.__new__(GeminiProvider)
    provider._client = client
    provider._model = "gemini-1.5-pro"
    return provider


@pytest.mark.xwai_unit
class TestGeminiProviderAPI:
    """Validate GeminiProvider API behavior without real SDK calls."""

    @pytest.mark.asyncio
    async def test_generate_sets_json_config_and_extracts_json(self):
        calls: dict[str, object] = {}
        candidate = SimpleNamespace(content=SimpleNamespace(parts=[]))
        response = SimpleNamespace(text='```json\n{"ok": true}\n```', candidates=[candidate], usage_metadata={"tokens": 9})

        class _Models:
            def generate_content(self, **kwargs):
                calls["kwargs"] = kwargs
                return response

        client = SimpleNamespace(models=_Models())
        provider = _build_gemini_provider_with_client(client)

        result = await provider.generate("hello", response_format=ResponseFormat.JSON, temperature=0.3, max_tokens=120)

        assert isinstance(result, AIResponse)
        assert result.content == '{"ok": true}'
        assert result.format == ResponseFormat.JSON
        assert calls["kwargs"]["config"]["response_mime_type"] == "application/json"
        assert calls["kwargs"]["config"]["temperature"] == 0.3
        assert calls["kwargs"]["config"]["max_output_tokens"] == 120

    @pytest.mark.asyncio
    async def test_generate_extracts_inline_media(self):
        inline = SimpleNamespace(mime_type="image/png", data="abc")
        part = SimpleNamespace(inline_data=inline)
        candidate = SimpleNamespace(content=SimpleNamespace(parts=[part]))
        response = SimpleNamespace(text="image generated", candidates=[candidate], usage_metadata={})

        class _Models:
            def generate_content(self, **kwargs):
                return response

        client = SimpleNamespace(models=_Models())
        provider = _build_gemini_provider_with_client(client)

        result = await provider.generate("draw")

        assert result.content == "image generated"
        assert result.media == [{"mime_type": "image/png", "data": "abc", "type": "image"}]

    @pytest.mark.asyncio
    async def test_chat_delegates_to_generate_with_combined_prompt(self, monkeypatch):
        provider = _build_gemini_provider_with_client(client=SimpleNamespace(models=SimpleNamespace()))
        observed: dict[str, object] = {}

        async def _fake_generate(prompt: str, attachments=None, **kwargs):
            observed["prompt"] = prompt
            observed["attachments"] = attachments
            observed["kwargs"] = kwargs
            return AIResponse(content="ok")

        monkeypatch.setattr(provider, "generate", _fake_generate)

        result = await provider.chat(
            [
                {"role": "system", "content": "be concise"},
                {"role": "user", "content": "first"},
                {"role": "assistant", "content": "second"},
                {"role": "user", "content": "third"},
            ],
            attachments=[{"mime_type": "image/png", "data": "raw"}],
        )

        assert result.content == "ok"
        assert observed["prompt"] == "first\nsecond\nthird"
        assert observed["attachments"] == [{"mime_type": "image/png", "data": "raw"}]
        assert observed["kwargs"]["system_instruction"] == "be concise"

    @pytest.mark.asyncio
    async def test_stream_yields_chunks_with_accumulated_content(self):
        class _Models:
            def generate_content_stream(self, **kwargs):
                return [SimpleNamespace(text="A"), SimpleNamespace(text="B")]

        client = SimpleNamespace(models=_Models())
        provider = _build_gemini_provider_with_client(client)

        chunks = [item async for item in provider.stream("hello")]

        assert [c.content for c in chunks] == ["A", "B"]
        assert chunks[-1].metadata["accumulated"] == "AB"
        assert chunks[-1].metadata["provider"] == "gemini"

    @pytest.mark.asyncio
    async def test_generate_wraps_unknown_errors(self):
        class _Models:
            def generate_content(self, **kwargs):
                raise RuntimeError("boom")

        client = SimpleNamespace(models=_Models())
        provider = _build_gemini_provider_with_client(client)

        with pytest.raises(XWAIProviderError, match="Failed to generate response"):
            await provider.generate("hello")
