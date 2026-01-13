# Shutter - Development TODOs

## 🎯 Current Focus: v0.1 — Python Proof of Concept

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
- [ ] Implement fetch layer (src/grove_shutter/fetch.py)
  - [ ] Basic httpx URL fetching
  - [ ] HTML to text conversion
  - [ ] Timeout handling
- [ ] Implement OpenRouter integration (src/grove_shutter/extraction.py)
  - [ ] API client for OpenRouter
  - [ ] Model tier mapping (fast → actual model)
  - [ ] Token counting
- [ ] Implement core shutter() function (src/grove_shutter/core.py)
  - [ ] Orchestrate fetch → canary → extract flow
  - [ ] Error handling and response formatting
- [ ] Implement basic Canary check (src/grove_shutter/canary.py)
  - [ ] Minimal extraction (100-200 tokens)
  - [ ] Basic instruction-override pattern detection
  - [ ] Return PromptInjectionDetails on detection
- [ ] Implement SQLite offenders list (src/grove_shutter/database.py)
  - [ ] Database initialization
  - [ ] Add/update offender records
  - [ ] Query offenders by domain
  - [ ] Threshold check (≥3 detections)
- [ ] Implement CLI (src/grove_shutter/cli.py)
  - [ ] Typer CLI with url and --query arguments
  - [ ] Model tier selection (--model)
  - [ ] JSON output formatting
  - [ ] --setup command for initial config
- [ ] Implement config management (src/grove_shutter/config.py)
  - [ ] TOML config file loading
  - [ ] Environment variable fallback
  - [ ] Interactive setup flow
  - [ ] ~/.shutter/ directory creation

### Testing (v0.1)
- [ ] Write tests for core functionality
  - [ ] Test basic extraction flow
  - [ ] Test Canary detection
  - [ ] Test offenders list logic
  - [ ] Test model tier mapping
- [ ] Integration tests with real OpenRouter calls (use test API key)

### Configuration & Setup (v0.1)
- [ ] Set up secrets management
  - [ ] Copy secrets_template.json to secrets.json
  - [ ] Add real OPENROUTER_API_KEY
- [ ] Initialize UV dependencies
  - [ ] Run `uv sync` to install dependencies
  - [ ] Verify all imports work

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

1. ~~**Pre-development research**~~ COMPLETE - See docs/RESEARCH.md and docs/PROMPTS.md
2. **Set up secrets** - Copy template, add real API keys
3. **Start with fetch layer** - Get basic URL fetching working
4. **Build incrementally** - Core → Canary → Extract → CLI

---

*Last updated: 2026-01-13*
*Current version: v0.1 (in development)*
*Research phase completed: 2026-01-13*
