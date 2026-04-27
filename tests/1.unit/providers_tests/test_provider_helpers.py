#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/providers_tests/test_provider_helpers.py
Unit tests for provider helper methods that do not require network calls.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

from pathlib import Path

import pytest

from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.providers.gemini import GeminiProvider
from exonware.xwai.providers.gpt import GPTProvider


@pytest.mark.xwai_unit
class TestProviderHelperMethods:
    """Covers pure helper functions to reduce regression risk."""

    def test_gpt_guess_mime_type(self):
        provider = GPTProvider.__new__(GPTProvider)

        assert provider._guess_mime_type(Path("photo.png")) == "image/png"
        assert provider._guess_mime_type(Path("doc.pdf")) == "application/pdf"
        assert provider._guess_mime_type(Path("unknown.bin")) == "application/octet-stream"

    def test_gemini_guess_mime_type(self):
        provider = GeminiProvider.__new__(GeminiProvider)

        assert provider._guess_mime_type(Path("photo.jpg")) == "image/jpeg"
        assert provider._guess_mime_type(Path("data.json")) == "application/json"
        assert provider._guess_mime_type(Path("unknown.xyz")) == "application/octet-stream"

    def test_extract_json_from_markdown_blocks(self):
        gpt = GPTProvider.__new__(GPTProvider)
        gemini = GeminiProvider.__new__(GeminiProvider)
        payload = '{"ok": true}'

        assert gpt._extract_json(f"```json\n{payload}\n```") == payload
        assert gemini._extract_json(f"```\n{payload}\n```") == payload

    def test_gpt_prepare_attachments_missing_file_raises(self):
        provider = GPTProvider.__new__(GPTProvider)

        with pytest.raises(XWAIProviderError, match="Attachment file not found"):
            provider._prepare_attachments(["D:/does/not/exist.png"])

    def test_gemini_prepare_attachment_missing_file_raises(self):
        provider = GeminiProvider.__new__(GeminiProvider)

        with pytest.raises(XWAIProviderError, match="Attachment file not found"):
            provider._prepare_attachment("D:/does/not/exist.png")
