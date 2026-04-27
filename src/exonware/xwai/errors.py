#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/errors.py
Error classes for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.5
Generation Date: 07-Jan-2025
"""


class XWAIError(Exception):
    """Base error for xwai."""
    pass


class XWAIProviderError(XWAIError):
    """AI provider-related errors."""
    pass


class XWAIResponseError(XWAIError):
    """AI response-related errors."""
    pass


class XWAIContextError(XWAIError):
    """AI context-related errors."""
    pass
