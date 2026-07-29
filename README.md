# Eterna MCP Gateway

**The fastest way to give your AI agent real trading capabilities.**

**No KYC. Sandboxed TypeScript SDK. Isolated sub-accounts. 0.014% maker fees on futures.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP Protocol](https://img.shields.io/badge/MCP-Streamable_HTTP-green.svg)](https://modelcontextprotocol.io)
[![Tools](https://img.shields.io/badge/Tools-3-orange.svg)](#mcp-tools)
[![SDK](https://img.shields.io/badge/SDK_methods-29-blue.svg)](#sdk-methods-via-execute_code)

---

## 30-Second Install

Add to your MCP client and complete OAuth when prompted:

```json
{
  "mcpServers": {
    "eterna": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp"
    }
  }
}
```

Your agent is auto-provisioned on first sign-in. There is **no** `register_agent` tool.

See [QUICKSTART.md](QUICKSTART.md) for Claude, Cursor, and Openclaw walkthroughs.

Product site: [ai.eterna.exchange](https://ai.eterna.exchange)

---

## How it works

Eterna is **not** a one-MCP-tool-per-exchange-endpoint server.

1. Agent calls **`search_sdk`** to find the right `eterna.*` method.
2. Agent calls **`execute_code`** with TypeScript that uses the full SDK in one round-trip.
3. Code runs in a sandboxed Deno runtime. Result is returned as JSON.

That model uses ~**90% fewer tokens** than wrapping every Bybit call as a separate MCP tool.

---

## MCP tools

| Tool | Description |
|---|---|
| `execute_code` | Run TypeScript in a Deno sandbox with the `eterna.*` trading SDK |
| `search_sdk` | Search SDK docs (`list` / `summary` / `full` / `params` / `keywords`) |
| `search_examples` | Semantic search over curated trading examples |

### Prompts

| Prompt | Description |
|---|---|
| `getting_started` | How to use `execute_code`, deposit flow, sandbox rules |
| `sdk_reference` | Full `eterna.*` method signatures and response shapes |
| `error_handling` | Error categories and recovery |
| `technical_analysis` | RSI, MACD, EMA, SMA, Bollinger, VWAP |
| `strategy_momentum_scalping` | Optional strategy template |
| `strategy_mean_reversion` | Optional strategy template |
| `strategy_funding_rate_arbitrage` | Optional strategy template |

### Resources

| URI | Description |
|---|---|
| `eterna://docs/sdk` | Complete SDK reference |
| `eterna://docs/errors` | Error reference |
| `eterna://docs/examples` | Example snippets |

Full parameter docs: [docs/tools-reference.md](docs/tools-reference.md)

---

## SDK methods (via `execute_code`)

29 methods on the `eterna` object inside the sandbox:

| Category | Methods |
|---|---|
| **Market data** | `getTickers`, `getOrderbook`, `getInstruments` |
| **Technical analysis** | `getRsi`, `getMacd`, `getEma`, `getSma`, `getBollingerBands`, `getVwap` |
| **Trading** | `placeOrder`, `closePosition`, `cancelOrder`, `cancelAllOrders`, `setLeverage`, `setTradingStop` |
| **Account** | `getBalance`, `getAccountInfo`, `getAllCoinsBalance`, `getPositions`, `getOrders` |
| **Funding** | `getDepositAddress`, `getDepositRecords`, `getAllowedDepositCoins`, `transferToTrading`, `swapToUsdt`, `getCoinInfo`, `getWithdrawableAmount`, `submitWithdrawal`, `getWithdrawalStatus` |

Example:

```typescript
const balance = await eterna.getBalance();
const ticker = await eterna.getTickers("BTCUSDT");
return { equity: balance.totalEquity, last: ticker[0]?.lastPrice };
```

---

## Why Eterna?

| | Eterna (managed) | Self-hosted MCP servers | Direct API wrappers |
|---|---|---|---|
| **Setup time** | ~30 seconds | 15-30 min | Hours |
| **Auth** | OAuth (or legacy API key) | You create & rotate keys | You create & rotate keys |
| **Agent isolation** | Dedicated sub-account per agent | Shared account | Shared account |
| **Execution model** | Sandboxed TypeScript SDK | Usually one tool per endpoint | Custom code |
| **Transport** | Streamable HTTP (remote) | Often stdio (local only) | HTTP |
| **Maintenance** | Zero — we handle updates | You manage | You manage |
| **Futures fees** | 0.014% maker / 0.035% taker | Retail unless you negotiate VIP | Retail unless you negotiate VIP |

### What you don't have to build

- Sub-account provisioning
- Rate limiting and request validation
- Deposit address management and fund routing
- Error handling for exchange API changes
- A Deno sandbox + typed trading SDK

---

## Works with your stack

### Claude (claude.ai)

Add a custom connector with URL `https://mcp.eterna.exchange/mcp`, complete OAuth, Approve.

### Claude Code / Cursor

Use the JSON config above (Claude Code: `.mcp.json`, Cursor: `.cursor/mcp.json`). Complete OAuth when prompted.

### Openclaw

```bash
openclaw plugins install @eterna-hybrid-exchange/openclaw-plugin
npm install -g @eterna-hybrid-exchange/cli
eterna login
```

### Any Streamable HTTP MCP client

Point the client at `https://mcp.eterna.exchange/mcp` and authenticate with OAuth (`mcp:full`) or a legacy Bearer API key. Polished guides for LangChain / CrewAI / AutoGen / ChatGPT are expanding.

---

## Authentication

**Preferred:** OAuth via [`https://ai-auth.eterna.exchange`](https://ai-auth.eterna.exchange) with scope `mcp:full`.

**Legacy:** long-lived agent API keys as `Authorization: Bearer …` (Argon2 hashed at rest).

Details: [docs/authentication.md](docs/authentication.md)

---

## Markets

- **USDT-margined perpetual futures** (200+ pairs)
- Spot trading is on the roadmap

---

## Roadmap

See [ROADMAP.md](ROADMAP.md).

**Shipped:** code execution sandbox, OAuth agent provisioning, 29 SDK methods, technical analysis, funding/withdrawal flows.

**Next:** broader SDK coverage, cron strategy runtime, backtesting, spot.

---

## Skills

Claude Code skills for trading knowledge:

- **[skills/claude-code/trading/SKILL.md](skills/claude-code/trading/SKILL.md)** — Risk management, position sizing, deposit flow, order lifecycle
- **[skills/claude-code/scalping/SKILL.md](skills/claude-code/scalping/SKILL.md)** — Momentum scalping strategy

Or grab the latest bundle: https://ai.eterna.exchange/claude-skills

---

## Documentation

- [QUICKSTART.md](QUICKSTART.md) — Connect and trade
- [Tools Reference](docs/tools-reference.md) — MCP tools + SDK overview
- [Authentication](docs/authentication.md) — OAuth and API keys
- [Architecture](docs/architecture.md) — Isolation and transport
- [CHANGELOG.md](CHANGELOG.md) — Version history
- [ROADMAP.md](ROADMAP.md) — What's next

Machine-readable product facts: https://ai.eterna.exchange/llms.txt

---

## Contact

Questions, partnerships, or support: **contact@eterna.exchange**

---

## License

[MIT](LICENSE) — Copyright 2025-2026 Eterna Exchange
