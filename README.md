# Eterna MCP Gateway

This repository is now a compatibility entry point for the Eterna AI MCP integration.

The canonical public repository is:

https://github.com/EternaHybridExchange/eterna-ai

## Current MCP Model

Eterna AI uses an OAuth-based, code-execution-first MCP model.

Agents connect to the managed Eterna MCP endpoint and use three MCP tools:

| Tool | Purpose |
| --- | --- |
| `execute_code` | Run TypeScript/JavaScript in a managed sandbox with the injected `eterna.*` SDK. |
| `search_sdk` | Search sandbox SDK documentation by method name, keyword, or detail level. |
| `search_examples` | Search curated and ingested code examples for common trading workflows. |

The old `register_agent` API-key flow and old direct-tool MCP interface are stale. New integrations should use OAuth and the `execute_code` workflow.

## MCP Configuration

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

## Example

Ask your MCP client to run:

```typescript
const [balance, ticker] = await Promise.all([
  eterna.getBalance(),
  eterna.getTickers("BTCUSDT"),
]);

return {
  equity: balance.list[0].totalEquity,
  availableBalance: balance.list[0].totalAvailableBalance,
  btc: {
    price: ticker.list[0].lastPrice,
    change24h: ticker.list[0].price24hPcnt,
    fundingRate: ticker.list[0].fundingRate,
  },
};
```

## Canonical Docs

Use the docs in `eterna-ai` as the source of truth:

- MCP: https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/mcp.md
- Sandbox SDK: https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/sdk.md
- CLI: https://github.com/EternaHybridExchange/eterna-ai/tree/main/packages/cli
- OpenClaw plugin: https://github.com/EternaHybridExchange/eterna-ai/tree/main/packages/openclaw-plugin

## What Remains Here

Historical docs and examples in this repository may refer to the old API-key/direct-tool model. Treat them as archival until they are migrated or removed.

## License

MIT
