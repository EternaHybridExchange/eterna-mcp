# Roadmap

This document outlines planned features for the Eterna MCP Gateway. Priorities may shift based on user feedback.

## In Progress

### Expanded Bybit API Coverage
Extending from 12 tools to 140+ endpoints across all Bybit V5 API categories:
- **Trade management** -- amend orders, cancel orders, batch operations
- **Position controls** -- set trading stops, switch position mode, adjust leverage
- **Market data** -- kline/candlestick data, funding rate history, open interest, insurance fund
- **Account info** -- fee rates, transaction logs, account configuration
- **Asset management** -- coin info, withdrawal flows, internal transfers

Endpoint evaluation complete (237 endpoints classified). Implementation in progress by category.

## Planned

### Code Execution Sandbox
Submit TypeScript code for execution in an isolated sandbox environment. Your agent writes trading logic; the gateway runs it securely.

- **Analysis tier** -- read-only access to market data and account state (5s timeout, 64MB memory)
- **Trade tier** -- guarded read-write access with pre-trade safety checks
- No direct network access -- all API calls via typed SDK proxy over IPC
- Static code analysis (AST) blocks unsafe patterns before execution
- Per-execution API call budgets and rate limit pre-enforcement

### Strategy Runtime
Deploy TypeScript strategies on cron schedules. Zero LLM usage at execution time -- pure code.

- Agent writes and tests strategy via the sandbox
- Deploys to a schedule (e.g., "run every 5 minutes")
- Gateway executes the strategy code with the same isolation guarantees
- Strategies can be paused, updated, or removed via MCP tools

### Backtesting Engine
Replay strategies against historical market data before deploying live.

- Historical kline data replay
- Simulated order fills with configurable slippage
- Performance metrics: PnL, Sharpe ratio, max drawdown, win rate
- Same SDK interface as live trading -- no code changes needed

### Spot Trading
Extend beyond perpetual futures to spot markets on Bybit.

## Released

See [CHANGELOG.md](CHANGELOG.md) for version history.
