# Roadmap

Priorities may shift based on user feedback.

## Released

### Code execution sandbox
Shipped. Agents submit TypeScript to `execute_code`; the gateway runs it in an isolated Deno sandbox with the typed `eterna.*` SDK (no direct outbound network from user code).

### OAuth agent provisioning
Shipped. Claude / Cursor connectors authenticate via `ai-auth`; the gateway auto-provisions an isolated sub-account. Legacy API keys remain available for CLI/custom clients.

### Expanded trading SDK (29 methods)
Shipped via `execute_code` (not as 12 individual MCP tools):

- Market data + technical analysis (RSI, MACD, EMA, SMA, Bollinger, VWAP)
- Order management (cancel, cancel-all, leverage, trading stops)
- Funding / withdrawal helpers

### Meta-tools for agents
Shipped: `search_sdk`, `search_examples`, prompts (`getting_started`, `sdk_reference`, …), and `eterna://docs/*` resources.

See [CHANGELOG.md](CHANGELOG.md) for history.

## In progress / next

### Broader SDK coverage
Additional Bybit V5 surfaces beyond the current 29 methods (more market history, account logs, batch operations, etc.).

### Strategy runtime
Deploy TypeScript strategies on cron schedules. Zero LLM usage at execution time — pure code with the same sandbox guarantees.

### Backtesting engine
Replay strategies against historical market data before going live (same SDK interface as live trading).

### Spot trading
Extend beyond USDT perpetual futures to spot markets.

### More first-class client guides
Polished LangChain / CrewAI / AutoGen / ChatGPT onboarding on top of the existing Streamable HTTP + OAuth model.
