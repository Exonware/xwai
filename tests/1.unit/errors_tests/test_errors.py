#!/usr/bin/env python3
"""
#exonware/xwai/tests/1.unit/errors_tests/test_errors.py
Unit tests for xwai error hierarchy.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 24-Mar-2026
"""

from __future__ import annotations

import pytest

from exonware.xwai.errors import (
    XWAIContextError,
    XWAIError,
    XWAIProviderError,
    XWAIResponseError,
)


@pytest.mark.xwai_unit
class TestErrors:
    """Ensure custom errors maintain inheritance contracts."""

    def test_error_inheritance(self):
        assert issubclass(XWAIProviderError, XWAIError)
        assert issubclass(XWAIResponseError, XWAIError)
        assert issubclass(XWAIContextError, XWAIError)

    def test_error_messages(self):
        error = XWAIProviderError("provider failed")
        assert str(error) == "provider failed"
