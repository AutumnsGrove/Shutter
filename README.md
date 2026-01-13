# Shutter

**Web Content Distillation Service**

> *Open. Capture. Close.*

---

## Overview

Shutter is a web content distillation layer that sits between LLM agents and raw web pages. It fetches URLs, uses a cheap/fast LLM to extract only the relevant content based on a query, and returns clean, focused results.

**Two key benefits:**

1. **Token efficiency** — Agents get 200 tokens instead of 20,000
2. **Prompt injection defense** — Raw page content never reaches the driver model; injections never make it past the aperture

## Quick Start

### Installation

```bash
# Install via UV (recommended)
uv add grove-shutter

# Or via pip
pip install grove-shutter
```

### CLI Usage

```bash
# After installation
shutter "https://example.com/pricing" --query "extract pricing tiers"

# Or via uvx (no install required)
uvx grove-shutter "https://example.com/pricing" --query "extract pricing tiers"
```

### Programmatic Usage

```python
from grove_shutter import shutter

result = await shutter(
    url="https://example.com/pricing",
    query="extract pricing tiers",
    model="fast",
    max_tokens=500
)

print(result.extracted)
# Output: "Basic: $9/mo (1 user, 5GB). Pro: $29/mo (5 users, 50GB)..."
```

## Configuration

### First Run Setup

```bash
# Interactive setup
shutter --setup

# Or set environment variables
export OPENROUTER_API_KEY="sk-or-v1-..."
export TAVILY_API_KEY="tvly-..."  # optional, for enhanced fetching
```

### Configuration File

Shutter stores configuration at `~/.shutter/config.toml`:

```toml
[api]
openrouter_key = "sk-or-v1-..."
tavily_key = "tvly-..."  # optional

[defaults]
model = "fast"
max_tokens = 500
timeout = 30000
```

## Response Format

### Clean Extraction

```json
{
  "url": "https://example.com/pricing",
  "extracted": "Basic: $9/mo (1 user, 5GB). Pro: $29/mo (5 users, 50GB). Enterprise: custom pricing, contact sales.",
  "tokens_input": 24500,
  "tokens_output": 42,
  "model_used": "deepseek/deepseek-chat",
  "prompt_injection": null
}
```

### Prompt Injection Detected

```json
{
  "url": "https://malicious.example.com",
  "extracted": null,
  "tokens_input": 8200,
  "tokens_output": 0,
  "model_used": "deepseek/deepseek-chat",
  "prompt_injection": {
    "detected": true,
    "type": "instruction_override",
    "snippet": "IGNORE ALL PREVIOUS INSTRUCTIONS...",
    "domain_flagged": true
  }
}
```

The `prompt_injection` object gives your agent enough information to decide how to proceed. The domain gets added to an offenders list for future reference.

## Model Preferences

| Value | Use Case | Model |
|-------|----------|-------|
| `fast` | Quick extractions, simple queries | Cerebras or Groq (fastest available) |
| `accurate` | Complex extraction, nuanced content | DeepSeek V3.2 |
| `research` | Web-optimized, longer analysis | Tongyi DeepResearcher (Qwen3 30B-3B) |
| `code` | Technical docs, code extraction | Minimax M2.1 |

## How It Works

Shutter uses a **2-phase Canary approach** for prompt injection defense:

**Phase 1: Canary Check**
- Run extraction with minimal tokens (100-200)
- Check for instruction-override patterns in output
- Cost: ~$0.001

**Phase 2: Full Extraction** (only if Phase 1 passes)
- Run full extraction with requested token limit
- Cost: varies by model and content

If Canary detects injection patterns, the request is halted and the domain is flagged.

### Offenders List

Shutter maintains a persistent list of domains where prompt injections have been detected:

- **Location**: `~/.shutter/offenders.db` (SQLite)
- **Not on list**: Proceed normally
- **On list, < 3 detections**: Proceed with warning in response
- **On list, ≥ 3 detections**: Return early with warning, skip fetch entirely

This creates trial-and-error defense that improves over time.

## Development Roadmap

### v0.1 — Python Proof of Concept
- [ ] Core fetch + summarization logic
- [ ] OpenRouter integration
- [ ] Basic prompt injection detection
- [ ] CLI with Typer
- [ ] Local SQLite offenders list

### v1.0 — Python Production
- [ ] Full Canary-based PI detection
- [ ] Tavily integration for enhanced fetching
- [ ] All four model tiers (fast/accurate/research/code)
- [ ] PyPI release (`grove-shutter`)
- [ ] uvx one-liner support
- [ ] Config management (~/.shutter/)

### v1.5 — Cloudflare Port
- [ ] Worker implementation (port from Python)
- [ ] D1 shared offenders list
- [ ] Durable Objects rate limiting
- [ ] HTTP API with Heartwood auth
- [ ] NPM package (`@groveengine/shutter`)
- [ ] npx one-liner support

### v2.0 — Search
- [ ] Multi-URL search queries
- [ ] Additional providers (Exa, Brave, etc.)
- [ ] Result aggregation and deduplication

### v3.0 — Caching & Intelligence
- [ ] Content caching
- [ ] Smart cache invalidation
- [ ] Injection pattern learning

## Contributing

This is a Grove Engine project in early development. See [`docs/SPEC.md`](docs/SPEC.md) for the full specification and design decisions.

For development setup:

```bash
# Clone the repository
git clone https://github.com/AutumnsGrove/Shutter.git
cd Shutter

# Install dependencies with UV
uv sync --dev

# Run tests
pytest

# Format code
black src/ tests/
ruff check src/ tests/
```

## License

MIT

## Links

- **Repository**: [github.com/AutumnsGrove/Shutter](https://github.com/AutumnsGrove/Shutter)
- **Documentation**: [docs/SPEC.md](docs/SPEC.md)
- **Issues**: [github.com/AutumnsGrove/Shutter/issues](https://github.com/AutumnsGrove/Shutter/issues)

---

*A shutter controls what reaches the lens. Open it, and light floods in—everything, all at once, overwhelming. But a photographer doesn't want everything. They want the shot. The shutter opens precisely when needed, captures exactly what's in frame, and closes before the noise can follow.*
