# xwai

**AI integration for eXonware.** One surface over OpenAI, Anthropic, and local models, with NLP helpers (commands, context) and hooks into xwentity, xwstorage, xwaction, and xwbots. More detail in `docs/` and [README_LONG.md](README_LONG.md).

**Company:** eXonware.com · **Author:** eXonware Backend Team · **Email:** connect@exonware.com  

[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://exonware.com)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## 📦 Install

```bash
pip install exonware-xwai
# Optional: [lazy] or [full]
pip install exonware-xwai[lazy]
pip install exonware-xwai[full]
```

---

## 🚀 Quick start

```python
from exonware.xwai import XWAI

ai = XWAI(provider="openai", api_key="your-key")
response = await ai.generate("What is eXonware?")
command = await ai.interpret_command("create a user named Alice")
```

See [docs/](docs/) for ARCHITECTURE, AI_PROVIDERS, INTEGRATION, API when those files exist.

---

## ✨ What you get

| Area | What's in it |
|------|----------------|
| **Providers** | OpenAI, Anthropic, local LLMs behind one interface. |
| **NLP** | Command interpretation and message understanding. |
| **Stack** | xwentity, xwstorage, xwaction, xwbots; conversation context. |
| **Ops** | API keys, rate limits, basic privacy guardrails. |

---

## 🌐 Ecosystem functional contributions

`xwai` handles AI-provider orchestration; sibling libraries provide execution, persistence, and domain boundaries around AI workflows.
You can use `xwai` standalone as an AI provider abstraction in existing applications.
Bringing in more XW components is optional and mostly useful for enterprise and mission-critical AI systems that require self-managed workflow, storage, and governance infrastructure.

| Supporting XW lib | What it provides to xwai | Functional requirement it satisfies |
|------|----------------|----------------|
| **XWAction** | Action/workflow invocation model for AI-triggered operations and tool-like calls. | Structured execution of AI decisions in backend workflows. |
| **XWEntity** | Domain model integration for AI-generated or AI-updated entities. | Business-object-safe AI integration instead of raw payload mutation. |
| **XWStorage** | Persistence for prompts, contexts, outputs, and operational state. | Durable AI state/history and backend portability. |
| **XWChat / XWBots** | Chat/bot transport and interaction surfaces where AI responses are delivered. | Multi-channel conversational UX and automation integration. |
| **XWSystem** | Shared runtime/security/config/serialization infrastructure. | Operational consistency, secure key/runtime handling, and reduced glue code. |
| **XWSchema** | Validation of structured AI outputs and command interpretation payloads. | Contract-safe AI outputs for downstream services. |

Competitive edge: `xwai` is not only provider SDK wrapping; it plugs AI generation into typed action/entity/storage/chat flows in the same platform.

---

## 📖 Docs and tests

- **Start:** [docs/INDEX.md](docs/INDEX.md) or [docs/](docs/).
- **Tests:** From repo root, follow this package's test layout.

---

## 📜 License and links

Apache-2.0 - see [LICENSE](LICENSE). **Homepage:** https://exonware.com · **Repository:** https://github.com/exonware/xwai  


## ⏱️ Async Support

<!-- async-support:start -->
- xwai includes asynchronous execution paths in production code.
- Source validation: 17 async def definitions and 8 await usages under src/.
- Use async APIs for I/O-heavy or concurrent workloads to improve throughput and responsiveness.
<!-- async-support:end -->
Version: 0.0.1.3 | Updated: 11-Apr-2026

*Built with ❤️ by eXonware.com - Revolutionizing Python Development Since 2025*
