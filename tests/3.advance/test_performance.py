#!/usr/bin/env python3
"""
#exonware/xwai/tests/3.advance/test_performance.py
Advance performance tests for xwai.
Priority #4: Performance Excellence
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1
Generation Date: 07-Jan-2025
"""

from __future__ import annotations

from typing import Any

import pytest
import time

from exonware.xwai.facade import XWAI
from exonware.xwai.response import AIResponse


class _FastProvider:
    async def generate(self, prompt: str, **kwargs: Any) -> AIResponse:
        return AIResponse(content=prompt)

    async def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> AIResponse:
        return AIResponse(content=messages[-1]["content"] if messages else "")

    async def stream(self, prompt: str, **kwargs: Any):
        yield AIResponse(content=prompt)


@pytest.mark.xwai_advance
@pytest.mark.xwai_performance
class TestAIPerformanceExcellence:
    """Performance guardrails for local, no-network code paths."""

    def test_initialization_performance(self):
        """XWAI initialization should remain lightweight."""
        start = time.perf_counter()
        _ = XWAI()
        elapsed = time.perf_counter() - start

        assert elapsed < 0.1

    def test_bulk_initialization_average_time(self):
        """Bulk instance creation should stay comfortably under milliseconds."""
        start = time.perf_counter()
        _instances = [XWAI(model="gpt-3.5-turbo") for _ in range(200)]
        elapsed = time.perf_counter() - start
        avg = elapsed / 200

        assert len(_instances) == 200
        assert avg < 0.005

    @pytest.mark.asyncio
    async def test_send_prompt_dispatch_performance(self):
        """Facade dispatch overhead for in-memory provider should be very low."""
        ai = XWAI()
        ai.providers["fast"] = _FastProvider()

        start = time.perf_counter()
        for _ in range(200):
            response = await ai.send_prompt("ping", provider="fast")
            assert response.content == "ping"
        elapsed = time.perf_counter() - start

        assert elapsed < 1.0
