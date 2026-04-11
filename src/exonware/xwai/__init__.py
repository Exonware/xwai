#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/__init__.py
XWAI Package Initialization
This module provides AI integration platform for the eXonware ecosystem.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.3
Generation Date: 07-Jan-2025
"""
# =============================================================================
# XWLAZY INTEGRATION - Auto-install missing dependencies silently (EARLY)
# =============================================================================
# Activate xwlazy BEFORE other imports to enable auto-installation of missing dependencies
# This enables silent auto-installation of missing libraries when they are imported

try:
    from exonware.xwlazy import auto_enable_lazy
    auto_enable_lazy(__package__ or "exonware.xwai", mode="smart")
except ImportError:
    # xwlazy not installed - lazy mode simply stays disabled (normal behavior)
    pass
from .version import __version__, __author__, __email__
# Standard imports - NO try/except!
from exonware.xwsystem import get_logger
from exonware.xwentity import XWEntity
from exonware.xwstorage import XWStorage
from exonware.xwaction import XWAction
# Core exports
from .facade import XWAI
from .contracts import (
    IAIProvider, IAIResponse, IAIContext, ICommandInterpreter
)
from .base import (
    AAIProvider, AAIResponse, AAIContext, ACommandInterpreter
)
from .response import AIResponse
from .defs import (
    AIProviderType, AIModelType, ResponseFormat
)
from .errors import (
    XWAIError, XWAIProviderError, XWAIResponseError, XWAIContextError
)
# Provider exports (may be None if dependencies not installed)
from .providers import GeminiProvider, GPTProvider
__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Main classes
    "XWAI",
    # Response classes
    "AIResponse",
    # Interfaces
    "IAIProvider",
    "IAIResponse",
    "IAIContext",
    "ICommandInterpreter",
    # Abstract classes
    "AAIProvider",
    "AAIResponse",
    "AAIContext",
    "ACommandInterpreter",
    # Providers
    "GeminiProvider",
    "GPTProvider",
    # Definitions
    "AIProviderType",
    "AIModelType",
    "ResponseFormat",
    # Errors
    "XWAIError",
    "XWAIProviderError",
    "XWAIResponseError",
    "XWAIContextError",
]
