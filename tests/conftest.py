from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path

# Monorepo checkout: add sibling package src dirs so `exonware.*` imports resolve without editable installs.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_PKG_ROOT = Path(__file__).resolve().parents[1]
_SIBLING_SRCS = (
    "xwnode",
    "xwformats",
    "xwjson",
    "xwschema",
    "xwquery",
    "xwdata",
    "xwentity",
    "xwauth",
    "xwstorage",
    "xwsystem",
    "xwaction",
    "xwai",
    "xwlazy",
)

for _name in _SIBLING_SRCS:
    _src = _REPO_ROOT / _name / "src"
    if _src.is_dir():
        _p = str(_src)
        if _p not in sys.path:
            sys.path.insert(0, _p)

_pkg_src = _PKG_ROOT / "src"
if _pkg_src.is_dir():
    _ps = str(_pkg_src)
    if _ps not in sys.path:
        sys.path.insert(0, _ps)

import pytest


def _install_optional_provider_stubs() -> None:
    """
    Install lightweight stubs for optional SDKs used by provider modules.

    WHY: xwai imports provider modules at package-import time, but developer
    and CI environments may not have heavyweight optional SDKs installed.
    """
    if importlib.util.find_spec("openai") is None and "openai" not in sys.modules:
        openai = types.ModuleType("openai")

        class _OpenAIAPIError(Exception):
            """Fallback OpenAI API error for provider import tests."""

        class _OpenAIClient:
            """Fallback OpenAI client that fails only on actual use."""

            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        openai.APIError = _OpenAIAPIError
        openai.OpenAI = _OpenAIClient
        sys.modules["openai"] = openai

    has_google_genai = (
        importlib.util.find_spec("google.genai") is not None
        if importlib.util.find_spec("google") is not None
        else False
    )
    if not has_google_genai and "google.genai" not in sys.modules:
        google = sys.modules.get("google")
        if google is None:
            google = types.ModuleType("google")
            google.__path__ = []
            sys.modules["google"] = google

        genai = types.ModuleType("google.genai")

        class _GenAIClient:
            """Fallback Gemini client used only for import safety."""

            def __init__(self, *args, **kwargs):
                self.args = args
                self.kwargs = kwargs

        genai.Client = _GenAIClient
        sys.modules["google.genai"] = genai
        google.genai = genai

        api_core = types.ModuleType("google.api_core")
        api_core.__path__ = []
        exceptions = types.ModuleType("google.api_core.exceptions")

        class _GoogleAPIError(Exception):
            """Fallback Google API error for provider import tests."""

        exceptions.GoogleAPIError = _GoogleAPIError
        api_core.exceptions = exceptions
        sys.modules["google.api_core"] = api_core
        sys.modules["google.api_core.exceptions"] = exceptions


_install_optional_provider_stubs()
