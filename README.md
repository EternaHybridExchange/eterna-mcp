# Eterna MCP Gateway

**The fastest, cheapest way to give your AI agent real trading capabilities.**

**No KYC. 0.014% maker fees on futures. <200ms latency. Isolated sub-accounts.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-green.svg)](https://modelcontextprotocol.io)
[![SDK Methods](https://img.shields.io/badge/SDK_Methods-29-orange.svg)](#available-tools)

---

## 30-Second Install

Add to your MCP client config and you're trading:

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

Your agent connects, authenticates via OAuth, and starts trading. See [QUICKSTART.md](QUICKSTART.md) for a 5-minute walkthrough.

---

## Why Eterna?

|                        | Eterna (managed)                          | Self-hosted MCP servers  | Direct API wrappers      |
| ---------------------- | ----------------------------------------- | ------------------------ | ------------------------ |
| **Setup time**         | 30 seconds                                | 15-30 min                | Hours                    |
| **API key management** | Auto-provisioned                          | You create & rotate      | You create & rotate      |
| **Agent isolation**    | Dedicated sub-account per agent           | Shared account           | Shared account           |
| **Risk management**    | Built-in (leverage caps, position limits) | None                     | Build your own           |
| **Key security**       | Argon2-hashed, never exposed              | Plaintext env vars       | Plaintext env vars       |
| **Transport**          | HTTP (works remotely)                     | stdio (local only)       | HTTP                     |
| **Maintenance**        | Zero -- we handle updates                 | You manage               | You manage               |
| **Multi-agent**        | Native                                    | Manual config per agent  | Manual                   |
| **Futures fees**       | 0.014% maker / 0.035% taker               | 0.02% / 0.055% (default) | 0.02% / 0.055% (default) |
| **Spot fees**          | 0.065% maker / 0.0775% taker              | 0.1% / 0.1% (default)    | 0.1% / 0.1% (default)    |

### What you don't have to build

- Sub-account provisioning and API key rotation
- Rate limiting and request validation
- Position sizing guardrails
- Deposit address management and fund routing
- Error handling for exchange API changes

---

## Works With Your Stack

No pre-existing API key needed. Your agent connects, registers itself, and starts trading.

### LangChain

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient({
    "trading": {
        "url": "https://mcp.eterna.exchange/mcp",
        "transport": "streamable_http",
    }
}) as client:
    tools = client.get_tools()
    # Use tools with any LangChain agent
```

### AutoGen

```python
from autogen_ext.tools.mcp import McpWorkbench, StreamableHttpParams

async with McpWorkbench(StreamableHttpParams(
    url="https://mcp.eterna.exchange/mcp",
)) as wb:
    tools = await wb.list_tools()  # all trading tools
```

### CrewAI

```python
from crewai_tools.mcp import MCPServerAdapter

server = MCPServerAdapter(
    server_url="https://mcp.eterna.exchange/mcp",
)
tools = server.tools
# Assign tools to any CrewAI agent
```

### Raw Python (MCP SDK)

```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async with streamablehttp_client("https://mcp.eterna.exchange/mcp") as (r, w, _):
    async with ClientSession(r, w) as session:
        await session.initialize()
        await session.call_tool("get_tickers", {"symbol": "BTCUSDT"})
```

Full working examples: [`examples/`](examples/)

---

## Available Tools

29 SDK methods are available via `execute_code`. See [docs/tools-reference.md](docs/tools-reference.md) for the full method reference.

---

## Resources & Prompts

**MCP Resources:**

| Resource URI             | Description                                                                            |
| ------------------------ | -------------------------------------------------------------------------------------- |
| `eterna://risk-rules`    | JSON document with all risk constraints (max leverage, max positions, minimum balance) |
| `eterna://api-reference` | Complete tool reference with parameters, types, and return schemas                     |

**Built-in Prompts:**

| Prompt                       | Description                                                     |
| ---------------------------- | --------------------------------------------------------------- |
| `trading_guide`              | Risk management, position sizing, deposits, and order lifecycle |
| `momentum_scalping_strategy` | Step-by-step momentum scalping with entry/exit rules            |
| `place_trade`                | Interactive prompt that walks through placing a trade safely    |

---

## Benchmarks

See [benchmarks/](benchmarks/) for detailed methodology and data.

| Metric                 | Eterna MCP      | Self-hosted Bybit MCP    | Direct Bybit API         |
| ---------------------- | --------------- | ------------------------ | ------------------------ |
| **Order placement**    | ~180ms          | ~150ms + your infra      | ~120ms                   |
| **Market data**        | ~80ms           | ~60ms + your infra       | ~40ms                    |
| **Setup time**         | 30 seconds      | 15-30 min                | 2-4 hours                |
| **Monthly infra cost** | $0              | $5-50/mo (VPS)           | $5-50/mo (VPS)           |
| **Futures fees**       | 0.014% / 0.035% | 0.02% / 0.055% (default) | 0.02% / 0.055% (default) |

Eterna agents trade on institutional-tier fee schedules through Bybit's master/sub-account structure. Self-hosted servers pay retail fees unless you independently negotiate a VIP tier.

---

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full roadmap.

**Coming soon:**

- 130+ additional Bybit API endpoints (order management, position controls, market data)
- Strategy runtime -- deploy strategies on cron schedules, zero LLM at runtime
- Backtesting engine with historical data replay

---

## Client Configuration

### Claude Code

`.mcp.json` in your project root:

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

### Cursor

`.cursor/mcp.json`:

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

### Claude Desktop

Add to your Claude Desktop `config.json`:

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

---

## Skills

Claude Code skills for trading knowledge:

- **[skills/claude-code/trading/SKILL.md](skills/claude-code/trading/SKILL.md)** -- Risk management, position sizing, deposit flow, order lifecycle
- **[skills/claude-code/scalping/SKILL.md](skills/claude-code/scalping/SKILL.md)** -- Momentum scalping strategy with entry signals and exit rules

Copy into your project's `.claude/skills/` directory.

---

## Documentation

- [QUICKSTART.md](QUICKSTART.md) -- Trading in 5 minutes
- [Tools Reference](docs/tools-reference.md) -- Full parameter and return value docs
- [Authentication](docs/authentication.md) -- API key format, security model, connection modes
- [Architecture](docs/architecture.md) -- Agent isolation, transport protocol, market support
- [Strategies](docs/strategies.md) -- Momentum scalping and position sizing workflows
- [CHANGELOG.md](CHANGELOG.md) -- Version history
- [ROADMAP.md](ROADMAP.md) -- What's coming next

---

## Ecosystem

| Repository                                                                                    | Description                                                                |
| --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [eterna-exchange/bybit-mcp-server](https://github.com/eterna-exchange/bybit-mcp-server)       | Bybit-focused managed MCP server                                           |
| [eterna-exchange/mcp-trading-agent](https://github.com/eterna-exchange/mcp-trading-agent)     | IDE configs and trading strategies for Claude Code, Cursor, Claude Desktop |
| [eterna-exchange/awesome-mcp-trading](https://github.com/eterna-exchange/awesome-mcp-trading) | Curated list of MCP trading servers and resources                          |

---

## Contact

Questions, partnerships, or support: **contact@eterna.exchange**

---

## License

[MIT](LICENSE) -- Copyright 2025 Eterna Exchange
