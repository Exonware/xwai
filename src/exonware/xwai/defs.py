#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/defs.py
Type definitions and enums for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.4
Generation Date: 07-Jan-2025
"""

from enum import Enum
from typing import Any


class AIProviderType(Enum):
    """AI provider types."""
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    CUSTOM = "custom"


class AIModelType(Enum):
    """AI model types."""
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    CLAUDE_3_OPUS = "claude-3-opus"
    CLAUDE_3_SONNET = "claude-3-sonnet"
    CLAUDE_3_HAIKU = "claude-3-haiku"
    LOCAL_LLM = "local-llm"


class ResponseFormat(Enum):
    """Response formats."""
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"
