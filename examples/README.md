# Examples

> **Status (2026-07):** The Python examples in this folder still show the **retired** 12-tool MCP surface (`register_agent`, `get_tickers`, `place_order`, …).
>
> **Do not copy them against production.** Current gateway tools are `search_sdk`, `execute_code`, and `search_examples`. Auth is OAuth-first (or a legacy Bearer API key). See [QUICKSTART.md](../QUICKSTART.md) and [docs/tools-reference.md](../docs/tools-reference.md).

## Correct pattern today

```typescript
// inside execute_code
const balance = await eterna.getBalance();
const ticker = await eterna.getTickers("BTCUSDT");
return { balance, ticker };
```

For client setup (Claude / Cursor / Openclaw), follow the quickstart. Framework adapters (LangChain, CrewAI, AutoGen) should:

1. Connect to `https://mcp.eterna.exchange/mcp` with Streamable HTTP
2. Authenticate with OAuth (`mcp:full`) or a legacy API key header
3. Call `search_sdk` / `execute_code` instead of per-endpoint MCP tools

Updated end-to-end framework examples will replace the files in this directory.
