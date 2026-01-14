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

## ✅ v1.5 — Cloudflare Port (COMPLETE)

### Core Implementation
- [x] Port Python implementation to TypeScript/Workers
  - [x] types.ts - All interfaces (ShutterRequest, ShutterResponse, etc.)
  - [x] database.ts - D1 offenders list operations
  - [x] fetch.ts - Jina → Tavily → fetch chain
  - [x] canary.ts - 17 regex patterns, confidence scoring, LLM canary
  - [x] extraction.ts - OpenRouter extraction with 4 model tiers
  - [x] index.ts - Worker entry point with HTTP router
- [x] Set up D1 database for shared offenders list
- [x] Create HTTP API (no auth for v1.5)
- [x] Deploy to workers.dev

### Deployed
- **URL**: https://shutter.m7jv4v7npb.workers.dev
- **Endpoints**: /fetch, /extract, /offenders, /health

### Maintenance
- [ ] **ROTATE OpenRouter API key** (exposed in chat session)
- [ ] Re-add secrets after key rotation: `wrangler secret put OPENROUTER_API_KEY`

---

## 🔐 v1.6 — Authentication & Production

### Pre-Implementation Setup
- [ ] **Rotate OpenRouter API key** (CRITICAL - do this first!)
- [ ] Re-enable worker with new secrets
- [ ] Register Shutter as OAuth client in groveauth
  - Client ID: `shutter`
  - Redirect URI: `https://shutter.grove.place/auth/callback`
  - Scopes: `openid profile`

### GroveAuth Integration

**Reference:** `/projects/groveauth/` - OAuth 2.0 + PKCE implementation

#### OAuth Flow Implementation
- [ ] Add auth routes to Worker (`cloudflare/src/auth.ts`)
  - [ ] `GET /auth/login` - Generate PKCE challenge, redirect to groveauth
  - [ ] `GET /auth/callback` - Exchange code for tokens
  - [ ] `POST /auth/refresh` - Refresh expired access tokens
  - [ ] `POST /auth/logout` - Clear session

#### PKCE Login Flow
```
1. User hits /auth/login
2. Generate code_verifier (random 43-128 chars)
3. Hash to code_challenge (SHA256 + base64url)
4. Store code_verifier in KV (keyed by state param)
5. Redirect to: groveauth.grove.place/login?
   - client_id=shutter
   - redirect_uri=https://shutter.grove.place/auth/callback
   - response_type=code
   - scope=openid profile
   - state={random}
   - code_challenge={hash}
   - code_challenge_method=S256
6. User authenticates with groveauth
7. Groveauth redirects to /auth/callback?code=XXX&state=YYY
8. Exchange code + code_verifier for tokens
9. Return access_token to client
```

#### JWT Verification Middleware
- [ ] Create auth middleware (`cloudflare/src/middleware/auth.ts`)
  - [ ] Fetch JWKS from groveauth (cache in KV)
  - [ ] Verify RS256 JWT signatures
  - [ ] Check token expiration
  - [ ] Extract user claims (sub, email, name)
- [ ] Protect routes: `/fetch`, `/extract` (require valid token)
- [ ] Keep public: `/health`, `/auth/*`

#### Token Management
- [ ] Store refresh tokens securely (encrypted in KV or D1)
- [ ] Implement automatic token refresh before expiry
- [ ] Handle token revocation gracefully

### KV Storage Setup
- [ ] Create KV namespace for auth state
  ```bash
  wrangler kv namespace create SHUTTER_AUTH
  ```
- [ ] Add to wrangler.toml
- [ ] Store: PKCE state, JWKS cache, rate limit counters

### Rate Limiting (Durable Objects)
- [ ] Create RateLimiter Durable Object class
- [ ] Implement sliding window algorithm
- [ ] Limits per user (by JWT sub claim):
  - [ ] 100 requests/minute for /fetch
  - [ ] 1000 requests/day total
- [ ] Return 429 with Retry-After header when exceeded

### Custom Domain Deployment
- [ ] Configure `shutter.grove.place` in Cloudflare DNS
- [ ] Update wrangler.toml with custom route
  ```toml
  routes = [{ pattern = "shutter.grove.place", custom_domain = true }]
  ```
- [ ] Deploy and verify SSL

### NPM Package (`@groveengine/shutter`)
- [ ] Create npm-package/ directory structure
  ```
  npm-package/
  ├── src/
  │   ├── index.ts      # Main exports
  │   ├── client.ts     # HTTP client for shutter.grove.place
  │   └── standalone.ts # Standalone mode (user's own API key)
  ├── bin/
  │   └── shutter.ts    # CLI entry point
  ├── package.json
  └── tsconfig.json
  ```
- [ ] Implement ShutterClient class with auth flow
- [ ] CLI commands: `shutter login`, `shutter fetch <url> -q <query>`
- [ ] Publish to npm with `@groveengine` scope

### Testing v1.6
- [ ] Test OAuth flow end-to-end
- [ ] Test JWT verification with expired/invalid tokens
- [ ] Test rate limiting behavior
- [ ] Test custom domain routing
- [ ] Verify NPM package works: `npx @groveengine/shutter`

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

### 🚨 IMMEDIATE (Start of Session)
1. **Rotate OpenRouter API key** - Key was exposed in chat, must rotate before re-enabling worker
2. **Re-add secrets to worker** - `wrangler secret put OPENROUTER_API_KEY` (and TAVILY_API_KEY)

### 🔐 v1.6 Implementation Order
1. **Register Shutter as groveauth client** - Coordinate with groveauth project
2. **KV namespace setup** - `wrangler kv namespace create SHUTTER_AUTH`
3. **Auth routes** - `/auth/login`, `/auth/callback`, `/auth/refresh`
4. **JWT middleware** - Protect `/fetch` and `/extract` routes
5. **Custom domain** - Deploy to `shutter.grove.place`
6. **Rate limiting** - Durable Objects per-user limits
7. **NPM package** - `@groveengine/shutter` CLI wrapper

### Completed Milestones
- ~~**v0.1 Implementation**~~ COMPLETE
- ~~**v0.2 JS Rendering**~~ COMPLETE
- ~~**v1.0 Python Production**~~ COMPLETE
- ~~**v1.5 Cloudflare port**~~ COMPLETE (worker deployed, secrets removed for security)

---

*Last updated: 2026-01-13*
*Current version: v1.5.0*
*v0.1 completed: 2026-01-13*
*v0.2 (Jina/Tavily JS rendering): 2026-01-13*
*v1.0.0 (PyPI release): 2026-01-13*
*v1.5.0 (Cloudflare Workers): 2026-01-13*

---

## Quick Reference

### GroveAuth Endpoints
- `GET /login` - OAuth login with PKCE
- `POST /token` - Exchange code for tokens
- `POST /token/refresh` - Refresh access token
- `GET /verify` - Validate JWT
- `GET /userinfo` - Get user profile
- `GET /.well-known/jwks.json` - Public keys for JWT verification

### Worker Status
- **Deployed URL**: https://shutter.m7jv4v7npb.workers.dev
- **Status**: Disabled (secrets removed)
- **D1 Database**: shutter-offenders (056aeb20-48d5-405a-bebc-e167817df0c0)
