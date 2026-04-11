#!/usr/bin/env python3
"""
#exonware/xwai/src/exonware/xwai/providers/gpt.py
GPT (OpenAI) AI Provider implementation.
Company: eXonware.com
Author: eXonware Backend Team
Email: connect@exonware.com
Version: 0.0.1.3
Generation Date: 07-Jan-2025
"""

import json
import base64
import asyncio
from typing import Any, Optional, AsyncIterator
from pathlib import Path
from openai import OpenAI
from openai import APIError as OpenAIAPIError
from exonware.xwsystem import get_logger
from ..base import AAIProvider
from ..response import AIResponse
from ..defs import ResponseFormat
from ..errors import XWAIProviderError
logger = get_logger(__name__)


class GPTProvider(AAIProvider):
    """
    GPT (OpenAI) AI Provider using OpenAI API.
    Extends AAIProvider for AI functionality.
    Usage:
        >>> provider = GPTProvider(api_key="your_key", model="gpt-4")
        >>> response = await provider.generate("Hello, world!")
        >>> print(response.content)
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        version: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 30,
        **kwargs
    ):
        """
        Initialize GPT provider.
        Args:
            api_key: OpenAI API key
            model: Model name (e.g., "gpt-4", "gpt-3.5-turbo", "gpt-4-turbo")
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
            client_kwargs = {"api_key": api_key}
            if base_url:
                client_kwargs["base_url"] = base_url
            self._client = OpenAI(**client_kwargs)
        except Exception as e:
            raise XWAIProviderError(f"Failed to initialize OpenAI client: {e}") from e
        logger.info(f"Initialized GPTProvider with model: {model}")

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
            # Prepare messages
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            # Prepare user message with prompt and attachments
            user_content = []
            user_content.append({"type": "text", "text": prompt})
            # Add attachments as image_url or file content
            if attachments:
                for att in self._prepare_attachments(attachments):
                    user_content.append(att)
            messages.append({"role": "user", "content": user_content})
            # Prepare request parameters
            request_params = {
                "model": self._model,
                "messages": messages,
            }
            # Set response format
            if response_format == ResponseFormat.JSON:
                request_params["response_format"] = {"type": "json_object"}
            if temperature is not None:
                request_params["temperature"] = temperature
            if max_tokens is not None:
                request_params["max_tokens"] = max_tokens
            # Merge additional kwargs
            request_params.update(kwargs)
            # Check if using responses API (newer) or chat.completions (standard)
            if hasattr(self._client, 'responses') and hasattr(self._client.responses, 'create'):
                # Use responses API (as in user's example)
                response = self._client.responses.create(
                    model=self._model,
                    instructions=system_instruction or "",
                    input="Return the result in JSON format only.\n\n" + prompt if response_format == ResponseFormat.JSON else prompt,
                    text={'format': {'type': 'json_object'}} if response_format == ResponseFormat.JSON else {}
                )
                response_text = response.output_text.strip() if hasattr(response, 'output_text') else ""
                thinking = None
                usage = {}
            else:
                # Use standard chat.completions API
                response = self._client.chat.completions.create(**request_params)
                response_text = response.choices[0].message.content if response.choices else ""
                thinking = None
                # Extract thinking from reasoning_content if available
                if hasattr(response.choices[0].message, 'reasoning_content'):
                    thinking = response.choices[0].message.reasoning_content
                usage = {
                    'prompt_tokens': response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                    'completion_tokens': response.usage.completion_tokens if hasattr(response, 'usage') else 0,
                    'total_tokens': response.usage.total_tokens if hasattr(response, 'usage') else 0,
                }
            # Parse JSON if needed
            if response_format == ResponseFormat.JSON:
                response_text = self._extract_json(response_text)
            # Extract attachments/media from response
            attachments_list = []
            media_list = []
            # Check for generated images or other media
            if hasattr(response, 'data') and isinstance(response.data, list):
                for item in response.data:
                    if hasattr(item, 'url'):
                        media_list.append({
                            'url': item.url,
                            'type': 'image' if 'image' in str(item.url) else 'media'
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
                    'provider': 'openai',
                    'usage': usage,
                },
                attachments=attachments_list,
                media=media_list,
            )
        except OpenAIAPIError as e:
            raise XWAIProviderError(f"OpenAI API error: {e}") from e
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
        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            # Add attachments to last user message if any
            if role == 'user' and attachments and msg == messages[-1]:
                content_list = [{"type": "text", "text": content}]
                for att in self._prepare_attachments(attachments):
                    content_list.append(att)
                openai_messages.append({"role": role, "content": content_list})
            else:
                openai_messages.append({"role": role, "content": content})
        # Use chat completions
        try:
            request_params = {
                "model": self._model,
                "messages": openai_messages,
            }
            request_params.update(kwargs)
            response = self._client.chat.completions.create(**request_params)
            response_text = response.choices[0].message.content if response.choices else ""
            thinking = None
            if hasattr(response.choices[0].message, 'reasoning_content'):
                thinking = response.choices[0].message.reasoning_content
            usage = {
                'prompt_tokens': response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                'completion_tokens': response.usage.completion_tokens if hasattr(response, 'usage') else 0,
                'total_tokens': response.usage.total_tokens if hasattr(response, 'usage') else 0,
            }
            return AIResponse(
                content=response_text,
                format=ResponseFormat.TEXT,
                thinking=thinking,
                metadata={
                    'model': self._model,
                    'provider': 'openai',
                    'usage': usage,
                },
            )
        except Exception as e:
            raise XWAIProviderError(f"Failed to chat: {e}") from e

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
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            user_content = [{"type": "text", "text": prompt}]
            if attachments:
                for att in self._prepare_attachments(attachments):
                    user_content.append(att)
            messages.append({"role": "user", "content": user_content})
            request_params = {
                "model": self._model,
                "messages": messages,
                "stream": True,
            }
            request_params.update(kwargs)
            accumulated_content = ""
            stream = self._client.chat.completions.create(**request_params)
            # Convert synchronous stream to async generator
            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    chunk_text = chunk.choices[0].delta.content
                    accumulated_content += chunk_text
                    # Yield control to event loop
                    await asyncio.sleep(0)
                    yield AIResponse(
                        content=chunk_text,
                        format=ResponseFormat.TEXT,
                        metadata={
                            'model': self._model,
                            'provider': 'openai',
                            'streaming': True,
                            'accumulated': accumulated_content,
                        }
                    )
        except Exception as e:
            raise XWAIProviderError(f"Failed to stream response: {e}") from e

    def _prepare_attachments(
        self,
        attachments: list[str | bytes | dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Prepare attachments for OpenAI API."""
        prepared = []
        for att in attachments:
            if isinstance(att, dict):
                if 'url' in att:
                    prepared.append({
                        "type": "image_url",
                        "image_url": {"url": att['url']}
                    })
                elif 'file_path' in att:
                    file_path = Path(att['file_path'])
                    if not file_path.exists():
                        raise XWAIProviderError(f"Attachment file not found: {att['file_path']}")
                    # For images, use image_url format
                    mime_type = att.get('mime_type', self._guess_mime_type(file_path))
                    if mime_type.startswith('image/'):
                        # Convert to base64 data URL
                        data = base64.b64encode(file_path.read_bytes()).decode('utf-8')
                        data_url = f"data:{mime_type};base64,{data}"
                        prepared.append({
                            "type": "image_url",
                            "image_url": {"url": data_url}
                        })
                    else:
                        # For other files, might need file API
                        prepared.append({
                            "type": "text",
                            "text": f"File: {file_path.name}"
                        })
            elif isinstance(att, bytes):
                # Binary data - assume image
                data = base64.b64encode(att).decode('utf-8')
                data_url = f"data:image/png;base64,{data}"
                prepared.append({
                    "type": "image_url",
                    "image_url": {"url": data_url}
                })
            elif isinstance(att, str):
                # File path
                file_path = Path(att)
                if not file_path.exists():
                    raise XWAIProviderError(f"Attachment file not found: {att}")
                mime_type = self._guess_mime_type(file_path)
                if mime_type.startswith('image/'):
                    data = base64.b64encode(file_path.read_bytes()).decode('utf-8')
                    data_url = f"data:{mime_type};base64,{data}"
                    prepared.append({
                        "type": "image_url",
                        "image_url": {"url": data_url}
                    })
                else:
                    prepared.append({
                        "type": "text",
                        "text": f"File: {file_path.name}"
                    })
        return prepared

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
