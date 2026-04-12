#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/config.py
Configuration classes for xwai.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.4
Generation Date: 07-Jan-2025
"""

from dataclasses import dataclass
from typing import Optional
from .defs import AIProviderType, AIModelType
@dataclass

class XWAIConfig:
    """Configuration for XWAI."""
    provider: AIProviderType = AIProviderType.OPENAI
    model: AIModelType = AIModelType.GPT_3_5_TURBO
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout_seconds: int = 30
    max_tokens: int = 1000
    temperature: float = 0.7
    enable_context: bool = True
    enable_rate_limiting: bool = True
