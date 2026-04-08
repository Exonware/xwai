#!/usr/bin/env python3
"""
#exonware/xwai/tests/3.advance/test_usability.py
Advance usability tests for xwai.
Priority #2: Usability Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import pytest

from exonware.xwai.errors import XWAIProviderError
from exonware.xwai.facade import XWAI
from exonware.xwai.response import AIResponse


@pytest.mark.xwai_advance
@pytest.mark.xwai_usability
class TestAIUsabilityExcellence:
    """Validate developer-facing ergonomics and error clarity."""

    @pytest.mark.asyncio
    async def test_error_message_lists_available_providers(self):
        ai = XWAI()
        ai.providers["alpha"] = object()
        ai.providers["beta"] = object()

        with pytest.raises(XWAIProviderError) as exc:
            await ai.send_prompt("hello", provider="missing")

        message = str(exc.value)
        assert "missing" in message
        assert "alpha" in message
        assert "beta" in message

    def test_response_to_dict_has_stable_shape(self):
        response = AIResponse(content="ok")
        payload = response.to_dict()

        assert sorted(payload.keys()) == [
            "attachments",
            "content",
            "format",
            "media",
            "metadata",
            "thinking",
        ]
