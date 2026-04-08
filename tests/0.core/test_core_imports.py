#!/usr/bin/env python3
"""
#exonware/xwai/tests/0.core/test_core_imports.py
Core import tests for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

import pytest

@pytest.mark.xwai_core
class TestCoreImports:
    """Validate package-level imports and public symbols."""

    def test_import_xwai_package_exports(self):
        """Package exports should be importable from top-level module."""
        from exonware.xwai import (
            AIModelType,
            AIProviderType,
            AIResponse,
            ResponseFormat,
            XWAI,
            XWAIError,
            XWAIProviderError,
        )

        assert XWAI is not None
        assert AIResponse is not None
        assert AIProviderType.OPENAI.value == "openai"
        assert AIModelType.GPT_4.value == "gpt-4"
        assert ResponseFormat.JSON.value == "json"
        assert issubclass(XWAIProviderError, XWAIError)

    def test_import_contracts(self):
        """Protocols should remain importable for typing/runtime checks."""
        from exonware.xwai.contracts import IAIContext, IAIProvider, IAIResponse

        assert IAIProvider is not None
        assert IAIResponse is not None
        assert IAIContext is not None

    def test_import_errors(self):
        """Error hierarchy should remain importable and stable."""
        from exonware.xwai.errors import (
            XWAIContextError,
            XWAIError,
            XWAIProviderError,
            XWAIResponseError,
        )

        assert issubclass(XWAIProviderError, XWAIError)
        assert issubclass(XWAIResponseError, XWAIError)
        assert issubclass(XWAIContextError, XWAIError)
