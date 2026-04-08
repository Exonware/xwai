#!/usr/bin/env python3
"""
#exonware/xwai/tests/3.advance/test_security.py
Advance security tests for xwai.
Priority #1: Security Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.facade import XWAI
from exonware.xwai.providers.gpt import GPTProvider


@pytest.mark.xwai_advance
@pytest.mark.xwai_security
class TestAISecurityExcellence:
    """Security-oriented tests that validate safe failure behavior."""

    def test_api_key_not_leaked_via_repr_or_str(self):
        """Facade stringification should not expose API credentials."""
        secret = "sk-test-key-12345"
        ai = XWAI(api_key=secret)
        merged = f"{ai!r}::{ai}"

        assert secret not in merged

    @pytest.mark.asyncio
    async def test_provider_not_found_error_does_not_include_secrets(self):
        """Provider lookup errors should stay scoped to routing details."""
        ai = XWAI(api_key="top-secret")

        with pytest.raises(XWAIProviderError) as exc:
            await ai.send_prompt("hello", provider="missing-provider")

        assert "missing-provider" in str(exc.value)
        assert "top-secret" not in str(exc.value)

    def test_missing_attachment_path_fails_fast(self):
        """Nonexistent attachment paths should raise deterministic provider errors."""
        provider = GPTProvider.__new__(GPTProvider)

        with pytest.raises(XWAIProviderError, match="Attachment file not found"):
            provider._prepare_attachments(["D:/does/not/exist/file.png"])

    def test_binary_attachment_is_encoded_without_plaintext_exposure(self):
        """Binary attachments should be converted to data URLs, not raw bytes."""
        provider = GPTProvider.__new__(GPTProvider)
        prepared = provider._prepare_attachments([b"\x89PNG\r\n\x1a\nfake"])

        assert prepared[0]["type"] == "image_url"
        assert prepared[0]["image_url"]["url"].startswith("data:image/png;base64,")

    def test_file_attachment_uses_filename_only_for_non_images(self):
        """Non-image files should only expose filename reference in text payload."""
        provider = GPTProvider.__new__(GPTProvider)
        with tempfile.TemporaryDirectory() as tmp:
            file_path = Path(tmp) / "secret.txt"
            file_path.write_text("sensitive payload", encoding="utf-8")

            prepared = provider._prepare_attachments([str(file_path)])

        assert prepared[0]["type"] == "text"
        assert prepared[0]["text"] == "File: secret.txt"

    def test_rate_limiting_flag_defaults_enabled(self):
        """Security baseline keeps rate limiting enabled by default."""
        ai = XWAI()

        assert ai._config.enable_rate_limiting is True
