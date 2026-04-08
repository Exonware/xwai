# Architecture Reference — exonware-xwai

**Library:** exonware-xwai  
**Version:** 0.0.1  
**Last Updated:** 11-Feb-2026  
**Requirements source:** [REF_01_REQ.md](REF_01_REQ.md) sec. 7, 6

---

## Overview

xwai provides **AI provider integration** (thin facade): pluggable providers (e.g. Gemini, GPT), base, contracts, config. **xwai-server** (stub) exposes the API surface and delegates to this library. Design: provider abstraction; chat, complete, embed semantics; Firebase Functions/ML-style when used with xwapi.

**Design philosophy:** Thin facade; no AI logic in server—library holds all provider and config logic.

---

## High-Level Structure

```
xwai/
+-- contracts.py   # Provider interfaces
+-- base.py        # Abstract provider base
+-- facade.py      # Public API (chat, complete, embed)
+-- providers/
|   +-- gemini.py
|   +-- gpt.py
+-- config.py, defs.py, errors.py, response.py, version.py
```

**Entry points:** `exonware.xwai` (facade, providers).

---

## Module Breakdown

### Contracts and base

**Purpose:** Provider interfaces and abstract bases; config and response types.

### Facade (`facade.py`)

**Purpose:** Public API for chat, completion, embedding; delegates to configured provider.

### Providers (`providers/`)

**Purpose:** Gemini, GPT (and future providers); implement provider contracts.

### Scope vs xwai-server

- **xwai (this library):** AI logic, providers, config, contracts.
- **xwai-server:** HTTP/API surface (endpoints for chat, complete, embed); delegates to xwai.

---

## Dependencies

- Provider SDKs as needed (Gemini, GPT, etc.). xwai-server depends on xwai.

---

## Related Documents

- [REF_01_REQ.md](REF_01_REQ.md) — Requirements source
- [REF_22_PROJECT.md](REF_22_PROJECT.md) — Requirements and status
- [GUIDE_13_ARCH.md](../../docs/guides/GUIDE_13_ARCH.md) — Architecture guide
- xwai-server/docs/REF_22_PROJECT.md — Server scope
