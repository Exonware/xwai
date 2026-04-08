#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/config_tests/test_config.py
Unit tests for xwai configuration dataclass.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import pytest

from exonware.xwai.config import XWAIConfig
from exonware.xwai.defs import AIModelType, AIProviderType


@pytest.mark.xwai_unit
class TestXWAIConfig:
    """Validate dataclass defaults and overrides."""

    def test_defaults(self):
        """Default config should match published baseline values."""
        cfg = XWAIConfig()

        assert cfg.provider == AIProviderType.OPENAI
        assert cfg.model == AIModelType.GPT_3_5_TURBO
        assert cfg.timeout_seconds == 30
        assert cfg.max_tokens == 1000
        assert cfg.temperature == 0.7
        assert cfg.enable_context is True
        assert cfg.enable_rate_limiting is True

    def test_custom_values(self):
        """Custom constructor values should override defaults predictably."""
        cfg = XWAIConfig(
            provider=AIProviderType.GEMINI,
            model=AIModelType.GPT_4,
            api_key="key",
            base_url="https://example.test",
            timeout_seconds=90,
            max_tokens=2048,
            temperature=0.2,
            enable_context=False,
            enable_rate_limiting=False,
        )

        assert cfg.provider == AIProviderType.GEMINI
        assert cfg.model == AIModelType.GPT_4
        assert cfg.api_key == "key"
        assert cfg.base_url == "https://example.test"
        assert cfg.timeout_seconds == 90
        assert cfg.max_tokens == 2048
        assert cfg.temperature == 0.2
        assert cfg.enable_context is False
        assert cfg.enable_rate_limiting is False
