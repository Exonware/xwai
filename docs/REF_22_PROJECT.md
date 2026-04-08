# Project Reference — xwai

**Library:** exonware-xwai  
**Last Updated:** 07-Feb-2026

Per REF_35_REVIEW.

---

## Vision

xwai provides **AI provider integration** (thin facade): providers (e.g. Gemini, GPT), base, contracts, config. It holds the library logic; **xwai-server** (stub) exposes the API surface and delegates to this library. Firebase parity: Functions/ML-style integration when used with xwapi.

---

## Goals

1. **Provider abstraction:** Pluggable AI providers (Gemini, GPT, etc.); contracts and config.
2. **Scope vs xwai-server:** xwai = library (logic, providers); xwai-server = API surface (delegates to xwai). Documented in REF_22 and xwai-server REF_22.
3. **Traceability:** REF_22_PROJECT, REF_35_REVIEW, logs.

---

## Functional Requirements (Summary)

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-001 | Provider facade and contracts | High | Done |
| FR-002 | Base and config | High | Done |
| FR-003 | 4-layer tests | Medium | Done |

---

## Project Status Overview

- **Current phase:** Alpha (Low–Medium). Thin surface; PROJECT_PHASES in docs. Scope vs xwai-server: library here, API in xwai-server.
- **Docs:** REF_22_PROJECT (this file), REF_35_REVIEW; logs/reviews/.

---

*See GUIDE_22_PROJECT.md. Review: REF_35_REVIEW.md. xwai-server: see xwai-server/docs/REF_22_PROJECT.md.*
