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

## 🚀 v1.0 — Python Production

### Enhanced Features
- [ ] Full Canary-based PI detection
  - [ ] Semantic pattern analysis
  - [ ] Multiple injection type detection
  - [ ] Confidence scoring
- [ ] Tavily integration (src/grove_shutter/fetch.py)
  - [ ] Tavily SDK integration
  - [ ] JavaScript-rendered content handling
  - [ ] Fallback to basic fetch if Tavily unavailable
- [ ] All four model tiers
  - [ ] Fast: Cerebras/Groq fastest model
  - [ ] Accurate: DeepSeek V3.2
  - [ ] Research: Tongyi DeepResearcher (Qwen3 30B-3B)
  - [ ] Code: Minimax M2.1
- [ ] Config management improvements
  - [ ] ~/.shutter/config.toml persistent config
  - [ ] Default model preferences
  - [ ] Timeout configuration

### Distribution
- [ ] Prepare for PyPI release
  - [ ] Polish pyproject.toml metadata
  - [ ] Write comprehensive README
  - [ ] Add usage examples
  - [ ] Tag v1.0.0 release
- [ ] Publish to PyPI as `grove-shutter`
- [ ] Test uvx one-liner: `uvx grove-shutter`
- [ ] Documentation
  - [ ] API reference
  - [ ] Usage guide
  - [ ] Example integrations

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

1. ~~**v0.1 Implementation**~~ COMPLETE - All core functionality working
2. **Integration testing** - Test with real OpenRouter API calls
3. **PyPI preparation** - Polish for v1.0 release
4. **Cloudflare port** - TypeScript Workers implementation

---

*Last updated: 2026-01-13*
*Current version: v0.1 (complete)*
*v0.1 completed: 2026-01-13*
