#!/usr/bin/env python3
"""
#exonware/xwai/tests/3.advance/test_maintainability.py
Advance maintainability tests for xwai.
Priority #3: Maintainability Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import inspect

import pytest

from exonware.xwai.base import AAIProvider
from exonware.xwai.config import XWAIConfig
from exonware.xwai.facade import XWAI


@pytest.mark.xwai_advance
@pytest.mark.xwai_maintainability
class TestAIMaintainabilityExcellence:
    """Guardrails for maintainable API and class contracts."""

    def test_config_repr_is_readable_for_debugging(self):
        cfg = XWAIConfig()
        text = repr(cfg)

        assert "XWAIConfig" in text
        assert "timeout_seconds" in text
        assert "max_tokens" in text

    def test_facade_has_clear_public_methods(self):
        public = {name for name, value in inspect.getmembers(XWAI, inspect.isfunction) if not name.startswith("_")}

        assert {"send_prompt", "chat", "stream", "set_default_provider", "get_default_provider"} <= public

    def test_provider_contract_remains_abstract(self):
        with pytest.raises(TypeError):
            AAIProvider()
