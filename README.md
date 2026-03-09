# Eterna MCP Gateway

**Give your AI agent access to perpetual futures trading on Bybit**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-green.svg)](https://modelcontextprotocol.io)
[![Tools](https://img.shields.io/badge/Tools-12-orange.svg)](#tool-overview)

---

## What Is This?

Eterna MCP Gateway is a **hosted MCP server** that exposes Bybit perpetual futures trading to any MCP-compatible AI agent. No server to run, no API wrappers to build -- connect your agent and start trading in minutes.

## How It Works

```
AI Agent (any LLM)  <-->  MCP Gateway (hosted)  <-->  Bybit Exchange
```

Your AI agent connects to the gateway over MCP Streamable HTTP. The gateway handles authentication, sub-account isolation, and proxies all trading operations to Bybit. Each agent gets its own dedicated sub-account with isolated funds and positions.

## Quick Start

### 1. Add to Your MCP Client

Add the gateway to your MCP client configuration:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp"
    }
  }
}
```

### 2. Register Your Agent

Your agent calls the `register_agent` tool to create an account. The gateway returns a unique API key:

```
eterna_mcp_a1b2c3d4e5f6...
```

Save this key -- it is only shown once.

### 3. Reconnect with Your API Key

Update your configuration to include the API key as a Bearer token:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

### 4. Trade

Once authenticated, all 11 trading tools become available. Your agent can check balances, read market data, and place orders on Bybit perpetual futures.

---

## Tool Overview

| Category | Tool | Description |
|---|---|---|
| **Registration** | `register_agent` | Create a new agent account and receive an API key |
| **Market Data** | `get_tickers` | Current price, 24h change, volume, and funding rate |
| | `get_instruments` | Contract specifications, tick size, lot size, leverage limits |
| | `get_orderbook` | Live order book with bids and asks |
| **Account & Positions** | `get_balance` | USDT equity, available balance, and margin usage |
| | `get_positions` | Open positions with entry price, PnL, and leverage |
| | `get_orders` | Active and recent order history |
| **Trading** | `place_order` | Place market or limit orders with TP/SL |
| | `close_position` | Close an entire position at market price |
| **Funding** | `get_deposit_address` | Get deposit address for a coin and chain |
| | `get_deposit_records` | View deposit history |
| | `transfer_to_trading` | Move funds from Funding wallet to Trading wallet |

See [docs/tools-reference.md](docs/tools-reference.md) for full parameter and return value documentation.

---

## Resources

The gateway exposes two MCP resources:

| Resource URI | Description |
|---|---|
| `eterna://risk-rules` | JSON document describing all risk constraints (max leverage, max positions, minimum balance) |
| `eterna://api-reference` | Complete tool reference with parameters, types, and return schemas |

## Prompts

Three built-in MCP prompts are available:

| Prompt | Description |
|---|---|
| `trading_guide` | Comprehensive guide to risk management, position sizing, deposits, and order lifecycle |
| `momentum_scalping_strategy` | Step-by-step momentum scalping strategy with entry/exit rules |
| `place_trade` | Interactive prompt that walks through placing a trade safely |

---

## Client Configuration Examples

### Claude Code

Create `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

### Claude Desktop

Add to your Claude Desktop `config.json`:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

### Cursor

Create `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

### Python SDK

See [examples/python/basic-trading.py](examples/python/basic-trading.py) for a working example using the `mcp` Python SDK.

---

## Skills

This repository includes Claude Code skills in the `skills/` directory:

- **[skills/claude-code/trading/SKILL.md](skills/claude-code/trading/SKILL.md)** -- General trading guide covering risk management, position sizing, deposit flow, and order lifecycle.
- **[skills/claude-code/scalping/SKILL.md](skills/claude-code/scalping/SKILL.md)** -- Momentum scalping strategy with entry signals, orderbook confirmation, and exit rules.

Copy these into your project's `.claude/skills/` directory to give Claude Code domain-specific trading knowledge.

---

## Documentation

- [Tools Reference](docs/tools-reference.md) -- Full parameter and return value docs for all 12 tools
- [Authentication](docs/authentication.md) -- API key format, security model, and connection modes
- [Architecture](docs/architecture.md) -- Agent isolation, transport protocol, and market support
- [Strategies](docs/strategies.md) -- Momentum scalping strategy and position sizing workflow

---

## Compatible Clients

Any MCP-compatible client that supports Streamable HTTP transport can connect to the Eterna MCP Gateway:

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Desktop](https://claude.ai/download)
- [Cursor](https://cursor.sh)
- Custom agents using the [MCP SDK](https://modelcontextprotocol.io)

---

## Ecosystem

Eterna maintains several open-source projects for AI-powered trading:

| Repository | Description |
|---|---|
| [eterna-exchange/bybit-mcp-server](https://github.com/eterna-exchange/bybit-mcp-server) | Self-hosted Bybit MCP server |
| [eterna-exchange/mcp-trading-agent](https://github.com/eterna-exchange/mcp-trading-agent) | Reference trading agent implementation |
| [eterna-exchange/awesome-mcp-trading](https://github.com/eterna-exchange/awesome-mcp-trading) | Curated list of MCP trading resources |

---

## Contact

Questions, partnerships, or support:

**hello@eterna.exchange**

---

## License

[MIT](LICENSE) -- Copyright 2025 Eterna Exchange
