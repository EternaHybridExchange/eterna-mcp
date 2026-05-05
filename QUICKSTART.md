# Eterna MCP Quick Start

This quick start reflects the current Eterna AI MCP model.

The legacy `register_agent` API-key flow is stale. Use OAuth-based MCP clients and the `execute_code`, `search_sdk`, and `search_examples` tools.

## 1. Connect

Add the Eterna MCP endpoint to your MCP-compatible client:

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

For claude.ai, add `https://mcp.eterna.exchange/mcp` as a custom connector and complete the OAuth sign-in flow.

## 2. Discover Methods

Ask your agent:

> Search the Eterna SDK for balance, positions, and BTC ticker methods.

The agent should use `search_sdk`.

## 3. Execute Code

Ask your agent:

> Check my balance and show the current BTC price.

The agent should call `execute_code` with a TypeScript snippet like:

```typescript
const [balance, ticker] = await Promise.all([
  eterna.getBalance(),
  eterna.getTickers("BTCUSDT"),
]);

return {
  equity: balance.list[0].totalEquity,
  availableBalance: balance.list[0].totalAvailableBalance,
  btcPrice: ticker.list[0].lastPrice,
};
```

## 4. Deposit And Trade

Example prompts:

> Get my USDT deposit options.

> Get my USDT deposit address on Arbitrum.

> Check my deposit records.

> Transfer my USDT to the trading wallet.

> Search examples for placing a market order with stop loss and take profit.

> Propose a BTCUSDT trade, show the exact size, margin, stop loss, take profit, and ask before executing.

## Current Docs

- MCP docs: https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/mcp.md
- Sandbox SDK docs: https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/sdk.md
