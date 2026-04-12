#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/providers/gemini.py
Gemini AI Provider implementation.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.5
Generation Date: 07-Jan-2025
"""

import json
import base64
import asyncio
from typing import Any, Optional, AsyncIterator
from pathlib import Path
from google import genai
from google.api_core import exceptions as google_exceptions
from exonware.xwsystem import get_logger
from ..base import AAIProvider
from ..response import AIResponse
from ..defs import ResponseFormat
from ..errors import XWAIProviderError
logger = get_logger(__name__)


class GeminiProvider(AAIProvider):
    """
    Gemini AI Provider using Google's Gemini API.
    Extends AAIProvider for AI functionality.
    Usage:
        >>> provider = GeminiProvider(api_key="your_key", model="gemini-1.5-pro")
        >>> response = await provider.generate("Hello, world!")
        >>> print(response.content)
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-1.5-pro",
        version: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        """
        Initialize Gemini provider.
        Args:
            api_key: Gemini API key
            model: Model name (e.g., "gemini-1.5-pro", "gemini-1.5-flash")
            version: Optional API version
            base_url: Optional custom base URL
            timeout: Request timeout in seconds
            **kwargs: Additional configuration options
        """
        # Initialize provider
        self._api_key = api_key
        self._model = model
        self._version = version
        self._timeout = timeout
        try:
            self._client = genai.Client(api_key=api_key)
        except Exception as e:
            raise XWAIProviderError(f"Failed to initialize Gemini client: {e}") from e
        logger.info(f"Initialized GeminiProvider with model: {model}")

    async def generate(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        system_instruction: Optional[str] = None,
        response_format: Optional[ResponseFormat] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """
        Generate AI response.
        Args:
            prompt: Input prompt
            attachments: Optional list of attachments (file paths, bytes, or dicts with mime_type and data)
            system_instruction: Optional system instruction
            response_format: Optional response format (TEXT, JSON, MARKDOWN)
            temperature: Optional temperature setting
            max_tokens: Optional max tokens
            **kwargs: Additional parameters
        Returns:
            AIResponse object
        """
        try:
            # Prepare contents
            contents = self._prepare_contents(prompt, attachments)
            # Prepare config
            config = {}
            if system_instruction:
                config['system_instruction'] = system_instruction
            # Set response format
            if response_format == ResponseFormat.JSON:
                config['response_mime_type'] = 'application/json'
            elif response_format == ResponseFormat.MARKDOWN:
                config['response_mime_type'] = 'text/markdown'
            if temperature is not None:
                config['temperature'] = temperature
            if max_tokens is not None:
                config['max_output_tokens'] = max_tokens
            # Merge additional kwargs
            config.update(kwargs)
            # Generate content
            response = self._client.models.generate_content(
                model=self._model,
                config=config,
                contents=contents
            )
            # Extract response
            response_text = response.text.strip() if hasattr(response, 'text') else ""
            # Extract thinking if available (Gemini reasoning)
            thinking = None
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        if hasattr(part, 'function_call') or hasattr(part, 'reasoning'):
                            thinking = getattr(part, 'reasoning', None)
            # Parse JSON if needed
            if response_format == ResponseFormat.JSON:
                response_text = self._extract_json(response_text)
            # Extract attachments/media from response
            attachments_list = []
            media_list = []
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'inline_data'):
                                media_list.append({
                                    'mime_type': part.inline_data.mime_type,
                                    'data': part.inline_data.data,
                                    'type': 'image' if 'image' in part.inline_data.mime_type else 'media'
                                })
            # Determine format
            format_type = response_format or ResponseFormat.TEXT
            if response_format == ResponseFormat.JSON:
                format_type = ResponseFormat.JSON
            return AIResponse(
                content=response_text,
                format=format_type,
                thinking=thinking,
                metadata={
                    'model': self._model,
                    'provider': 'gemini',
                    'usage': getattr(response, 'usage_metadata', {}),
                },
                attachments=attachments_list,
                media=media_list,
            )
        except google_exceptions.GoogleAPIError as e:
            raise XWAIProviderError(f"Gemini API error: {e}") from e
        except Exception as e:
            raise XWAIProviderError(f"Failed to generate response: {e}") from e

    async def chat(
        self,
        messages: list[dict[str, str]],
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        **kwargs
    ) -> AIResponse:
        """
        Chat with AI using message history.
        Args:
            messages: List of message dicts with 'role' and 'content' keys
            attachments: Optional list of attachments
            **kwargs: Additional parameters
        Returns:
            AIResponse object
        """
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if role == 'system':
                # System messages are handled via system_instruction
                kwargs.setdefault('system_instruction', content)
            else:
                # Convert role: 'user' -> 'user', 'assistant' -> 'model'
                gemini_role = 'user' if role == 'user' else 'model'
                contents.append({
                    'role': gemini_role,
                    'parts': [{'text': content}]
                })
        # Add attachments to last user message if any
        if attachments and contents:
            last_msg = contents[-1]
            if last_msg.get('role') == 'user':
                parts = last_msg.get('parts', [])
                for att in attachments:
                    parts.append(self._prepare_attachment(att))
        # Use generate with combined contents
        combined_prompt = "\n".join([msg.get('content', '') for msg in messages if msg.get('role') != 'system'])
        return await self.generate(combined_prompt, attachments=attachments, **kwargs)

    async def stream(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None,
        system_instruction: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[AIResponse]:
        """
        Stream AI response in realtime.
        Args:
            prompt: Input prompt
            attachments: Optional list of attachments
            system_instruction: Optional system instruction
            **kwargs: Additional parameters
        Yields:
            AIResponse objects as chunks arrive
        """
        try:
            contents = self._prepare_contents(prompt, attachments)
            config = {}
            if system_instruction:
                config['system_instruction'] = system_instruction
            config.update(kwargs)
            # Stream response
            stream = self._client.models.generate_content_stream(
                model=self._model,
                config=config,
                contents=contents
            )
            accumulated_content = ""
            for chunk in stream:
                if hasattr(chunk, 'text'):
                    chunk_text = chunk.text
                    accumulated_content += chunk_text
                    # Yield control to event loop
                    await asyncio.sleep(0)
                    yield AIResponse(
                        content=chunk_text,
                        format=ResponseFormat.TEXT,
                        metadata={
                            'model': self._model,
                            'provider': 'gemini',
                            'streaming': True,
                            'accumulated': accumulated_content,
                        }
                    )
        except Exception as e:
            raise XWAIProviderError(f"Failed to stream response: {e}") from e

    def _prepare_contents(
        self,
        prompt: str,
        attachments: Optional[list[str | bytes | dict[str, Any]]] = None
    ) -> list[dict[str, Any]]:
        """Prepare contents for Gemini API."""
        parts = [{'text': prompt}]
        if attachments:
            for att in attachments:
                parts.append(self._prepare_attachment(att))
        return [{'role': 'user', 'parts': parts}]

    def _prepare_attachment(self, attachment: str | bytes | dict[str, Any]) -> dict[str, Any]:
        """Prepare attachment for Gemini API."""
        if isinstance(attachment, dict):
            # Already formatted
            if 'mime_type' in attachment and 'data' in attachment:
                return {'inline_data': attachment}
            elif 'file_path' in attachment:
                file_path = Path(attachment['file_path'])
                mime_type = attachment.get('mime_type', self._guess_mime_type(file_path))
                data = base64.b64encode(file_path.read_bytes()).decode('utf-8')
                return {
                    'inline_data': {
                        'mime_type': mime_type,
                        'data': data
                    }
                }
        elif isinstance(attachment, bytes):
            # Binary data - need mime_type
            return {
                'inline_data': {
                    'mime_type': 'application/octet-stream',
                    'data': base64.b64encode(attachment).decode('utf-8')
                }
            }
        elif isinstance(attachment, str):
            # File path
            file_path = Path(attachment)
            if not file_path.exists():
                raise XWAIProviderError(f"Attachment file not found: {attachment}")
            mime_type = self._guess_mime_type(file_path)
            data = base64.b64encode(file_path.read_bytes()).decode('utf-8')
            return {
                'inline_data': {
                    'mime_type': mime_type,
                    'data': data
                }
            }
        raise XWAIProviderError(f"Unsupported attachment type: {type(attachment)}")

    def _guess_mime_type(self, file_path: Path) -> str:
        """Guess MIME type from file extension."""
        ext = file_path.suffix.lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.json': 'application/json',
        }
        return mime_types.get(ext, 'application/octet-stream')

    def _extract_json(self, text: str) -> str:
        """Extract JSON from markdown code blocks."""
        if text.startswith('```json'):
            text = text.split('```json')[1].split('```')[0].strip()
        elif text.startswith('```'):
            text = text.split('```')[1].split('```')[0].strip()
        return text
