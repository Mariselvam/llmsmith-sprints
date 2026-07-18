# llmsmith-sprints

A 2-week, hands-on deep dive into building software **with** and **on top of** LLM APIs — from a hand-rolled HTTP client through to AI-assisted developer tooling. Everything here is written by hand, tested, linted, and shipped incrementally, one day at a time.

## What this repo demonstrates

- **Python fundamentals done properly** — type hints, docstrings, small single-responsibility functions, dataclasses over raw dicts, `src/`-layout packaging, and a `ruff`/`black`/`mypy`-clean codebase throughout.
- **Real LLM API integration, from the ground up** — a hand-built HTTP client (not a vendor SDK) that handles authentication, Server-Sent Event streaming, custom exception hierarchies mapped to HTTP status codes, retry-with-backoff, and input validation.
- **AI-assisted software development, applied to itself** — tooling that uses an LLM to generate tests and review code, then gets run against this very repo's own diffs.

## Why a hand-built HTTP client, not an SDK

Every provider (Groq, OpenAI, Anthropic, and most others) exposes essentially the same JSON-over-HTTP chat completions shape. Rather than reach for `pip install groq`, this project builds the client layer directly on `requests` — auth headers, JSON payloads, SSE stream parsing, and error handling included — because that's the transferable skill: understanding what an SDK is actually doing underneath, not just calling one.

**Provider:** [Groq](https://console.groq.com) — free tier, no credit card, OpenAI-compatible REST API. See [`llmsmith_2week_sprint_plan.md`](./llmsmith_2week_sprint_plan.md) for the full rationale and day-by-day plan this repo follows.

## Structure

```
llmsmith-sprints/
├── sprintA_llm_foundations/   # Week 1 — hand-built HTTP client + CLI chatbot
├── sprintB_ai_devtools/        # Week 2 — prompt eval harness + AI-powered dev tools
├── LOG.md                      # Daily build log: what shipped, what broke, what I learned
└── llmsmith_2week_sprint_plan.md
```

## Sprint A — LLM API Foundations

A tested, installable package wrapping a from-scratch HTTP client for Groq's chat completions API, plus a CLI chatbot built on top of it.

| Day | Focus | Ships |
|---|---|---|
| 1 | Core HTTP calls | Non-streaming + streaming (SSE, parsed by hand) requests |
| 2 | Conversation state | Multi-turn memory, system prompts, bounded history (token-budget aware) |
| 3 | Packaging | Installable `src/`-layout package, custom exception hierarchy |
| 4 | Resilience | Retry-with-backoff, input validation, 80%+ test coverage |
| 5 | Integration | End-to-end CLI chatbot, AI-reviewed diff, tagged release |

## Sprint B — AI-Assisted Dev Workflow

Tooling that uses the Sprint A client to make the development process itself faster and safer — the most direct proof of "AI in the SDLC."

| Day | Focus | Ships |
|---|---|---|
| 1–2 | Prompt evaluation | A harness comparing prompt/model variants with automated scoring |
| 3 | Test generation | `ai-test-gen` — generates pytest tests for a given source file |
| 4 | Code review | `ai-review` — reviews a `git diff`, returns structured, typed feedback |
| 5 | Integration | Unified CLI, tested end-to-end, used on this repo's own weekly diff |

## Engineering practices applied throughout

- Every HTTP call has an explicit `timeout`; retries are restricted to genuinely retryable errors (429/5xx), never blindly applied to 4xx client errors
- Secrets never touch source control — `.env`-based config, `.gitignore`'d from commit one
- Tests never hit the real network — all HTTP calls are mocked, keeping the suite fast and deterministic
- Every function is typed and documented; `ruff`, `black`, and `mypy` run clean before each weekly tag
- Daily progress and debugging notes are logged in [`LOG.md`](./LOG.md) as the work happens, not reconstructed after the fact

## Running this project

```bash
git clone <this-repo>
cd llmsmith-sprints
uv sync
cp .env.example .env   # add your free Groq API key — console.groq.com, no card required
uv run pytest
```

See each sprint's own `README.md` for usage instructions specific to that week's tools.

---

*Built as a structured, daily-practice project — see [`llmsmith_2week_sprint_plan.md`](./llmsmith_2week_sprint_plan.md) for the complete plan this repo follows day by day.*