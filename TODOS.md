# Shutter - Development TODOs

## ✅ v0.1 — Python Proof of Concept (COMPLETE)

### Pre-Development Research
- [x] Research extraction prompt techniques
  - [x] Check if Anthropic's web fetch prompt has leaked (Yes - documented in docs/RESEARCH.md)
  - [x] Survey Exa/Tavily/Perplexity extraction approaches (Complete - see docs/RESEARCH.md)
  - [x] Document patterns for different content types (articles, docs, pricing pages)
- [x] Catalog prompt injection patterns
  - [x] Research known web-based injection techniques (CVEs, Unicode attacks, encoding)
  - [x] Identify patterns for Canary detection logic (Regex patterns + semantic analysis)

**Research artifacts:**
- `docs/RESEARCH.md` - Comprehensive research findings
- `docs/PROMPTS.md` - Synthesized extraction prompt design

### Core Implementation (v0.1)
- [x] Implement fetch layer (src/grove_shutter/fetch.py)
  - [x] Basic httpx URL fetching
  - [x] HTML to text conversion (trafilatura)
  - [x] Timeout handling
- [x] Implement OpenRouter integration (src/grove_shutter/extraction.py)
  - [x] API client for OpenRouter
  - [x] Model tier mapping (fast/accurate/research/code)
  - [x] Token counting
- [x] Implement core shutter() function (src/grove_shutter/core.py)
  - [x] Orchestrate fetch → canary → extract flow
  - [x] Error handling and response formatting
- [x] Implement basic Canary check (src/grove_shutter/canary.py)
  - [x] Heuristic checks (15 regex patterns)
  - [x] Unicode hidden character detection
  - [x] Base64 payload detection
  - [x] LLM output analysis for hijacking indicators
  - [x] Return PromptInjectionDetails on detection
- [x] Implement SQLite offenders list (src/grove_shutter/database.py)
  - [x] Database initialization
  - [x] Add/update offender records
  - [x] Query offenders by domain
  - [x] Threshold check (≥3 detections)
- [x] Implement CLI (src/grove_shutter/cli.py)
  - [x] CLI with url and --query arguments
  - [x] Model tier selection (--model)
  - [x] JSON output formatting
  - [x] setup command for initial config
  - [x] offenders/clear-offenders commands
- [x] Implement config management (src/grove_shutter/config.py)
  - [x] TOML config file loading
  - [x] Environment variable fallback
  - [x] secrets.json support (dev mode)
  - [x] Interactive setup flow
  - [x] ~/.shutter/ directory creation

### Testing (v0.1)
- [x] Write tests for core functionality (107 tests passing)
  - [x] test_config.py - Config loading, API key priority, dry-run mode
  - [x] test_database.py - SQLite offenders CRUD, threshold logic
  - [x] test_canary.py - Heuristic patterns, Unicode detection, output analysis
  - [x] test_extraction.py - Model tier mapping, prompt construction
  - [x] test_core.py - Full shutter() flow, mocking, error handling
- [ ] Integration tests with real OpenRouter calls

### Configuration & Setup (v0.1)
- [x] Set up secrets management
  - [x] secrets_template.json created
  - [x] secrets.json support implemented
- [x] Initialize UV dependencies
  - [x] All dependencies in pyproject.toml
  - [x] trafilatura, tomli added

---

## ✅ v0.2 — JavaScript Rendering (COMPLETE)

### Smart Fetch Chain
- [x] Jina Reader integration (primary fetcher)
  - [x] Free JS rendering via `r.jina.ai/{url}`
  - [x] Returns clean markdown from rendered pages
- [x] Tavily fallback (secondary fetcher)
  - [x] Tavily SDK integration
  - [x] JavaScript-rendered content handling
- [x] Basic httpx + trafilatura (final fallback)
  - [x] For simple HTML pages that don't need JS

**Fetch priority chain:** Jina → Tavily → Basic httpx

*Tested: Stripe pricing page now returns full fee breakdown (2.9% + 30¢, etc.) instead of "rates not provided"*

---

## 🚀 v1.0 — Python Production

### Enhanced Features
- [x] Full Canary-based PI detection
  - [x] Semantic pattern analysis (17 weighted patterns)
  - [x] Multiple injection type detection (instruction_override, role_hijack, etc.)
  - [x] Confidence scoring (0.0-1.0 with multi-pattern boost)
  - [x] Config-based weight overrides ([canary.weights] in config.toml)
- [x] All four model tiers (OpenRouter)
  - [x] Fast: openai/gpt-oss-120b (Cerebras ~2000 tok/sec)
  - [x] Accurate: deepseek/deepseek-v3.2
  - [x] Research: alibaba/tongyi-deepresearch-30b-a3b
  - [x] Code: minimax/minimax-m2.1
- [x] Config management
  - [x] ~/.shutter/config.toml persistent config
  - [x] Default model preferences
  - [x] Timeout configuration
  - [x] Interactive setup (`shutter setup`)

### Distribution
- [x] Prepare for PyPI release
  - [x] Polish pyproject.toml metadata
  - [x] Write comprehensive README
  - [x] Add usage examples (docs/USAGE.md)
  - [x] Tag v1.0.0 release
- [x] Publish to PyPI as `grove-shutter`
- [x] Test uvx one-liner: `uvx --from grove-shutter shutter`
- [x] Documentation
  - [x] API reference (docs/API.md)
  - [x] Usage guide (docs/USAGE.md)
  - [x] Example integrations

---

## 🌐 v1.5 — Cloudflare Port

- [ ] Port Python implementation to TypeScript/Workers
- [ ] Set up D1 database for shared offenders list
- [ ] Implement Durable Objects rate limiting
- [ ] Create HTTP API with authentication
- [ ] Publish NPM package `@groveengine/shutter`
- [ ] Deploy to shutter.grove.place

---

## 🔍 v2.0 — Search

- [ ] Multi-URL search queries
- [ ] Additional fetch providers (Exa, Brave)
- [ ] Result aggregation and deduplication
- [ ] Source ranking

---

## 💾 v3.0 — Caching & Intelligence

- [ ] Content caching (R2 on Cloudflare)
- [ ] Smart cache invalidation
- [ ] Injection pattern learning
- [ ] Vectorize integration for pattern matching

---

## 📝 Documentation & Maintenance

- [ ] Keep docs/SPEC.md updated with design decisions
- [ ] Maintain CHANGELOG.md
- [ ] Update README.md roadmap as milestones complete
- [ ] Document Grove integration points

---

## Next Session Priorities

1. ~~**v0.1 Implementation**~~ COMPLETE
2. ~~**v0.2 JS Rendering**~~ COMPLETE
3. ~~**v1.0 Python Production**~~ COMPLETE
4. **Cloudflare port** - TypeScript Workers implementation (v1.5)

---

*Last updated: 2026-01-13*
*Current version: v1.0.0*
*v0.1 completed: 2026-01-13*
*v0.2 (Jina/Tavily JS rendering): 2026-01-13*
*v1.0.0 (PyPI release): 2026-01-13*
