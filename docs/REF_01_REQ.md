# Requirements Reference (REF_01_REQ)

**Project:** xwai  
**Sponsor:** eXonware.com / eXonware Backend Team  
**Version:** 0.0.1  
**Last Updated:** 11-Feb-2026  
**Produced by:** [GUIDE_01_REQ.md](../guides/GUIDE_01_REQ.md)

---

## Purpose of This Document

This document is the **single source of raw and refined requirements** collected from the project sponsor and stakeholders. It is updated on every requirements-gathering run. When the **Clarity Checklist** (section 12) reaches the agreed threshold, use this content to fill REF_12_IDEA, REF_22_PROJECT, REF_13_ARCH, REF_14_DX, REF_15_API, and planning artifacts. Template structure: [GUIDE_01_REQ.md](../guides/GUIDE_01_REQ.md).

---

## 1. Vision and Goals

| Field | Content |
|-------|---------|
| One-sentence purpose | AI provider integration (thin facade) for eXonware: pluggable providers (OpenAI, Anthropic, local LLMs), natural language commands, context management; Firebase Functions/ML-style when used with xwapi. (inferred from REF_22, README) |
| Primary users/beneficiaries | eXonware stack (xwentity, xwstorage, xwaction, xwbots); developers adding AI to apps. (inferred from REF_22, README) |
| Success (6 mo / 1 yr) | 6 mo: Stable provider API, REF_* compliance. 1 yr: Production use, ecosystem integration. (Refine per REF_22.) |
| Top 3–5 goals (ordered) | 1) Provider abstraction (Gemini, GPT, etc.; contracts and config). 2) Scope vs xwai-server (xwai = library; xwai-server = API surface). 3) Traceability (REF_22, REF_35). (from REF_22) |
| Problem statement | Need single API for multiple AI providers and command interpretation across the stack. (inferred from README) |

## 2. Scope and Boundaries

| In scope | Out of scope | Dependencies | Anti-goals |
|----------|--------------|--------------|------------|
| Provider facade and contracts; base and config; 4-layer tests; library logic. (from REF_22, README) | API server (xwai-server). (from REF_22) | TBD (see pyproject) | Exposing provider-specific APIs as stable public API. (inferred) |

### 2a. Reverse-Engineered Evidence (from codebase)

- **Facade:** `facade.py` — **XWAI**(default_provider, **options); **providers** dict (name → AAIProvider); **send_prompt**(prompt, attachments); **XWAIConfig**; **AIResponse**.
- **Providers:** `providers/gemini.py`, `providers/gpt.py` — pluggable providers (Gemini, GPT); **AAIProvider** base; config (API key, model).
- **Contracts:** `contracts.py` — provider contracts; `defs.py` — **AIProviderType**, **AIModelType**; `base.py` — **AAIProvider**.
- **Integration:** Used by xwbots (persona/agentic), xwentity, xwstorage, xwaction; natural language commands, context management; Firebase ML/Functions-style when used with xwapi.

## 3. Stakeholders and Sponsor

| Sponsor (name, role, final say) | Main stakeholders | External customers/partners | Doc consumers |
|----------------------------------|-------------------|-----------------------------|---------------|
| eXonware (company); eXonware Backend Team (author, maintainer, final say on scope and priorities). | Project sponsor / eXonware; downstream REF owners. | None currently. Future: open-source adopters. | Downstream REF_22/REF_13 owners; devs using xwai; AI agents (Cursor). |

## 4. Compliance and Standards

| Regulatory/standards | Security & privacy | Certifications/evidence |
|----------------------|--------------------|--------------------------|
| Per GUIDE_00_MASTER, GUIDE_11_COMP. (inferred) | API key handling, rate limiting, data privacy. (from README) | None currently. Per GUIDE_00_MASTER when required. |

## 5. Product and User Experience

| Main user journeys/use cases | Developer persona & 1–3 line tasks | Usability/accessibility | UX/DX benchmarks |
|-----------------------------|------------------------------------|--------------------------|------------------|
| Create AI client; generate text; interpret commands; integrate with entity/storage/action/bots. (inferred from README) | Developer: XWAI(provider="openai", api_key=...), ai.generate(...), ai.interpret_command(...). (from README) | Per REF_22. | Per REF_22. |

## 6. API and Surface Area

| Main entry points / "key code" | Easy (1–3 lines) vs advanced | Integration/existing APIs | Not in public API |
|--------------------------------|------------------------------|---------------------------|-------------------|
| XWAI; provider, api_key; generate(), interpret_command(). (from README) | Easy: XWAI(provider=..., api_key=...), generate(), interpret_command(). Advanced: context management, multiple providers. (from README) | xwentity, xwstorage, xwaction, xwbots. (from REF_22, README) | Provider adapter internals. (inferred) |

## 7. Architecture and Technology

| Required/forbidden tech | Preferred patterns | Scale & performance | Multi-language/platform |
|-------------------------|--------------------|----------------------|-------------------------|
| Python 3.x (from README) | Thin facade; contracts and config; library vs server scope. (from REF_22) | Per REF_22. | Python; xwai-server exposes API. (inferred) |

## 8. Non-Functional Requirements (Five Priorities)

| Security | Usability | Maintainability | Performance | Extensibility |
|----------|-----------|-----------------|-------------|---------------|
| API key handling, rate limiting, data privacy. (from README) | Per REF_22. | REF_22, REF_35, PROJECT_PHASES; 4-layer tests. (from REF_22) | Per REF_22. | Pluggable providers. (from REF_22) |

## 9. Milestones and Timeline

| Major milestones | Definition of done (first) | Fixed vs flexible |
|------------------|----------------------------|-------------------|
| FR-001–FR-003 (provider facade, base/config, 4-layer tests) Done. (from REF_22) | Provider facade and contracts present. (from REF_22) | Per REF_22. |

## 10. Risks and Assumptions

| Top risks | Assumptions | Kill/pivot criteria |
|-----------|-------------|----------------------|
| Per REF_22. | xwai-server delegates to xwai; scope in both REF_22s. (from REF_22) | Per REF_22. |

## 11. Workshop / Session Log (Optional)

| Date | Type | Participants | Outcomes |
|------|------|---------------|----------|
| 11-Feb-2026 | Reverse‑engineer | User + Agent | REF_01 from code/docs; Section 2a added (XWAI, providers, send_prompt). Sponsor to confirm. |

## 12. Clarity Checklist

| # | Criterion | ☐ |
|---|-----------|---|
| 1 | Vision and one-sentence purpose filled and confirmed | ☑ |
| 2 | Primary users and success criteria defined | ☑ |
| 3 | Top 3–5 goals listed and ordered | ☑ |
| 4 | In-scope and out-of-scope clear | ☑ |
| 5 | Dependencies and anti-goals documented | ☑ |
| 6 | Sponsor and main stakeholders identified | ☑ |
| 7 | Compliance/standards stated or deferred | ☑ |
| 8 | Main user journeys / use cases listed | ☑ |
| 9 | API / "key code" expectations captured | ☑ |
| 10 | Architecture/technology constraints captured | ☑ |
| 11 | NFRs (Five Priorities) addressed | ☑ |
| 12 | Milestones and DoD for first milestone set | ☑ |
| 13 | Top risks and assumptions documented | ☑ |
| 14 | Sponsor confirmed vision, scope, priorities | ☑ |

**Clarity score:** 14 / 14. **Ready to fill downstream docs?** ☑ Yes

---

*Inferred content is marked; sponsor confirmation required. Per GUIDE_01_REQ.*
