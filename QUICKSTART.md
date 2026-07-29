# Quick Start — Trading in Minutes

This guide gets you from zero to a live MCP session with an AI agent that can trade via Eterna.

## Prerequisites

- An MCP-compatible client: [claude.ai](https://claude.ai), [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.sh), [Claude Desktop](https://claude.ai/download), Openclaw, or any client supporting **Streamable HTTP**
- USDT for trading (deposit after setup)

## Important: current model

Eterna MCP exposes **3 tools**:

1. `search_sdk` — discover `eterna.*` methods
2. `execute_code` — run TypeScript in a Deno sandbox with the full SDK
3. `search_examples` — find example snippets

There is **no** `register_agent` tool and **no** per-endpoint tools like `get_tickers` / `place_order` at the MCP layer. Those are **SDK methods** inside `execute_code` (`eterna.getTickers`, `eterna.placeOrder`, …).

Auth is **OAuth-first**. The gateway auto-provisions an isolated sub-account on first successful sign-in.

---

## Claude (claude.ai)

1. Copy the MCP URL: `https://mcp.eterna.exchange/mcp`
2. Go to [claude.ai/customize/connectors](https://claude.ai/customize/connectors)
3. Click **+** then **Add custom connector**
4. Name it **Eterna**, paste the MCP URL
5. Click **Connect**
6. Complete the **OAuth sign-in** and click **Approve**

Ask Claude:

> Use search_sdk to find balance and ticker methods, then execute_code to show my equity and the BTCUSDT last price.

---

## Claude Code

Create `.mcp.json` in your project root:

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

Restart Claude Code if needed, complete OAuth when prompted, then use `search_sdk` + `execute_code`.

---

## Cursor

Create `.cursor/mcp.json`:

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

Restart Cursor if needed, complete OAuth when prompted.

---

## Openclaw

```bash
openclaw plugins install @eterna-hybrid-exchange/openclaw-plugin
npm install -g @eterna-hybrid-exchange/cli
eterna login
```

Then start the `eterna_trading` skill / onboarding flow.

Package: [@eterna-hybrid-exchange/openclaw-plugin](https://www.npmjs.com/package/@eterna-hybrid-exchange/openclaw-plugin)

---

## Deposit (after auth)

Ask your agent (it should use `execute_code`):

> Discover allowed USDT deposit chains, then give me a USDT deposit address on Arbitrum (`ARBI`).

After the deposit confirms:

> Transfer my USDT from the funding wallet to the trading wallet.

Underlying SDK calls:

```typescript
const coins = await eterna.getAllowedDepositCoins("USDT");
const addr = await eterna.getDepositAddress("USDT", "ARBI");
const transfer = await eterna.transferToTrading("USDT", "100");
return { coins, addr, transfer };
```

---

## Trade

Suggested prompts:

> What's the current BTCUSDT price and my available balance?

> Set leverage to 2x on BTCUSDT, then buy 0.001 BTC at market with a stop loss.

> Close my BTCUSDT position.

Example `execute_code` body:

```typescript
await eterna.setLeverage("BTCUSDT", "2");
const order = await eterna.placeOrder({
  symbol: "BTCUSDT",
  side: "Buy",
  orderType: "Market",
  qty: "0.001",
  stopLoss: "95000",
});
return order;
```

Always call `search_sdk` first if you are unsure about parameters.

---

## What's next?

- **[Tools Reference](docs/tools-reference.md)** — MCP tools + SDK categories
- **[Authentication](docs/authentication.md)** — OAuth and legacy API keys
- **[llms.txt](https://ai.eterna.exchange/llms.txt)** — Machine-readable product facts
- **[Video tutorials](https://ai.eterna.exchange/#videos)** — Official walkthroughs
