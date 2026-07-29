# Changelog

All notable changes to the Eterna MCP Gateway will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] - 2026-07-29

### Changed
- Documentation synced to the live gateway model: **3 MCP tools** (`execute_code`, `search_sdk`, `search_examples`) plus **29 `eterna.*` SDK methods** inside the Deno sandbox
- Auth documented as **OAuth-first** via `ai-auth` (`mcp:full`), with legacy API keys still supported
- Removed / deprecated docs for `register_agent` and the old 12 per-endpoint MCP tools
- Roadmap updated: code execution sandbox marked **released**

### Notes
- Production server identity remains `eterna-trading` `1.0.0`
- Historical entries below describe the earlier individual-tools era

## [0.3.0] - 2025-03-11

### Added
- `get_deposit_address` tool -- retrieve deposit addresses for any supported coin and chain
- `get_deposit_records` tool -- view deposit transaction history with status tracking
- `transfer_to_trading` tool -- move funds from Funding wallet to Trading (Unified) wallet
- Full deposit-to-trade lifecycle support without leaving the MCP interface

## [0.2.0] - 2025-02-15

### Added
- `place_order` tool with market and limit order support, optional TP/SL, and configurable leverage
- `close_position` tool for closing entire positions at market price
- `get_orders` tool for viewing active and recent order history
- `get_positions` tool for monitoring open positions with PnL and leverage details
- `eterna://risk-rules` MCP resource exposing risk constraints as JSON
- `eterna://api-reference` MCP resource with complete tool documentation
- `trading_guide`, `momentum_scalping_strategy`, and `place_trade` MCP prompts
- Claude Code skills for trading and scalping strategies

## [0.1.0] - 2025-01-20

### Added
- Initial release of Eterna MCP Gateway
- `register_agent` tool for self-service agent registration with API key provisioning
- `get_tickers` tool for real-time price and 24h market statistics
- `get_instruments` tool for contract specifications (tick size, lot size, leverage limits)
- `get_orderbook` tool for live order book data
- `get_balance` tool for account balance and margin information
- MCP Streamable HTTP transport
- Dedicated Bybit sub-account per agent with isolated funds and positions
- Argon2-hashed API key storage
- Built-in risk management rules (leverage caps, position limits)
