#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/defs_tests/test_defs.py
Unit tests for xwai enums and definitions.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import pytest

from exonware.xwai.defs import AIModelType, AIProviderType, ResponseFormat


@pytest.mark.xwai_unit
class TestDefinitions:
    """Verify enum members and stable public values."""

    def test_provider_type_values(self):
        assert AIProviderType.OPENAI.value == "openai"
        assert AIProviderType.GEMINI.value == "gemini"
        assert AIProviderType.ANTHROPIC.value == "anthropic"
        assert AIProviderType.LOCAL.value == "local"
        assert AIProviderType.CUSTOM.value == "custom"

    def test_model_type_values(self):
        assert AIModelType.GPT_4.value == "gpt-4"
        assert AIModelType.GPT_3_5_TURBO.value == "gpt-3.5-turbo"
        assert AIModelType.LOCAL_LLM.value == "local-llm"

    def test_response_format_values(self):
        assert ResponseFormat.TEXT.value == "text"
        assert ResponseFormat.JSON.value == "json"
        assert ResponseFormat.MARKDOWN.value == "markdown"
