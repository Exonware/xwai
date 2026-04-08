#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/response_tests/test_response.py
Unit tests for AIResponse behavior.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import pytest

from exonware.xwai.defs import ResponseFormat
from exonware.xwai.response import AIResponse


@pytest.mark.xwai_unit
class TestAIResponse:
    """Validate response accessors and serialization format."""

    def test_properties(self):
        response = AIResponse(
            content="hello",
            format=ResponseFormat.MARKDOWN,
            thinking="reasoning",
            metadata={"latency_ms": 12},
            attachments=[{"name": "a.txt"}],
            media=[{"type": "image"}],
        )

        assert response.content == "hello"
        assert response.format == ResponseFormat.MARKDOWN
        assert response.thinking == "reasoning"
        assert response.metadata == {"latency_ms": 12}
        assert response.attachments == [{"name": "a.txt"}]
        assert response.media == [{"type": "image"}]

    def test_to_dict(self):
        response = AIResponse(content="hello", format=ResponseFormat.JSON)
        payload = response.to_dict()

        assert payload["content"] == "hello"
        assert payload["format"] == "json"
        assert payload["thinking"] is None
        assert payload["metadata"] == {}
        assert payload["attachments"] == []
        assert payload["media"] == []
