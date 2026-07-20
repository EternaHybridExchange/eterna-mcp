---
name: eterna-mcp
description: Connect AI agents to Eterna MCP — a no-KYC managed trading exchange over Model Context Protocol (Streamable HTTP). Use when setting up Claude, Cursor, or LangChain agents to trade perpetual futures, fetch market data, or run sandboxed eterna.* TypeScript SDK calls.
---

# Eterna MCP

Give an AI agent real crypto futures trading through a managed MCP server. No KYC. Isolated sub-accounts. Sandboxed TypeScript execution.

## Connect (Streamable HTTP)

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

Authenticate with a Bearer token (OAuth via `https://ai-auth.eterna.exchange` or an agent API key). Details: https://github.com/EternaHybridExchange/eterna-mcp/blob/main/docs/authentication.md

## Recommended agent workflow

1. Read the `getting_started` prompt from the server (if exposed).
2. Call `search_sdk` before writing trading code.
3. Call `execute_code` with TypeScript that uses the `eterna.*` SDK.
4. On infrastructure errors, do not retry blindly — report them.

## What the SDK covers (via `execute_code`)

- Market data: tickers, orderbook, instruments
- Technical analysis: RSI, MACD, EMA, SMA, Bollinger, VWAP
- Trading: place/cancel orders, close positions, leverage, trading stops
- Account: balances, positions, orders
- Funding: deposit address/records, transfer, swap, withdrawal

## Canonical links

- Product: https://ai.eterna.exchange
- MCP URL: https://mcp.eterna.exchange/mcp
- Quickstart: https://github.com/EternaHybridExchange/eterna-mcp/blob/main/QUICKSTART.md
- Tools reference: https://github.com/EternaHybridExchange/eterna-mcp/blob/main/docs/tools-reference.md
- Registry name: `io.github.EternaHybridExchange/eterna-mcp`

## Whitelabel / partner note

For partner or white-label agent trading rails, start from the same MCP endpoint and auth model; customize agent provisioning and branding in the host application while keeping the managed gateway.
