# xwai (long version)

Long-form features and examples. Short overview: [README.md](README.md).

---

**Company:** eXonware.com  
**Author:** eXonware Backend Team  
**Email:** connect@exonware.com  
**Version:** 0.0.1.0

---

## What it does

**xwai** is the AI layer for the eXonware stack: one API over OpenAI, Anthropic, and local models, plus NLP helpers (command interpretation, message understanding) and integration points for xwentity, xwstorage, xwaction, xwbots, and related packages.

---

## Installation

```bash
# Basic
pip install exonware-xwai

# With lazy auto-install
pip install exonware-xwai[lazy]

# Full (all features)
pip install exonware-xwai[full]
```

---

## Quick start

```python
from exonware.xwai import XWAI

# Initialize xwai
ai = XWAI(provider="openai", api_key="your-key")

# Generate response
response = await ai.generate("What is eXonware?")

# Natural language command interpretation
command = await ai.interpret_command("create a user named Alice")
```

---

## Features

### Unified AI provider interface

```python
from exonware.xwai import XWAI

# OpenAI
ai = XWAI(provider="openai", api_key="sk-...")

# Anthropic
ai = XWAI(provider="anthropic", api_key="sk-ant-...")

# Local LLM
ai = XWAI(provider="local", model_path="/path/to/model")
```

### Natural language command interpretation

```python
# Interpret natural language commands
command = await ai.interpret_command("create a user named Alice with email alice@example.com")
# Returns: {"action": "create_user", "params": {"name": "Alice", "email": "alice@example.com"}}
```

### Context management

```python
# Maintain conversation context
context = ai.create_context()
response1 = await ai.generate("What is Python?", context=context)
response2 = await ai.generate("Tell me more", context=context)  # Uses previous context
```

### Ecosystem integration

```python
# Integration with xwentity
from exonware.xwentity import XWEntity

class User(XWEntity):
    name: str
    email: str

# AI can work with entities
user_data = await ai.generate_entity("Create a user entity", entity_class=User)
```

---

## Works with

- **xwentity** - entity-shaped data and validation
- **xwstorage** - persistence
- **xwaction** - actions
- **xwbots** - bot responses
- **xwquery** - natural language query interpretation (when wired up)

---

## Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) (if present)
- [AI Provider Guide](docs/AI_PROVIDERS.md)
- [Integration Guide](docs/INTEGRATION.md)
- [API Reference](docs/API.md)
- [README.md](README.md) - short overview

---

## Compared to LiteLLM

LiteLLM is the obvious peer: multi-provider routing in one place. xwai is built to sit next to eXonware entities, storage, and actions, and to leave room for provider-specific behavior (e.g. extended reasoning) instead of forcing everything through one lowest-common-denominator shape.

---

## License

MIT - see [LICENSE](LICENSE).

---

**Company:** eXonware.com  
**Author:** eXonware Backend Team  
**Email:** connect@exonware.com
