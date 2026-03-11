# Quick Start -- Trading in 5 Minutes

This guide gets you from zero to placing your first trade with an AI agent.

## Prerequisites

- An MCP-compatible client: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Cursor](https://cursor.sh), [Claude Desktop](https://claude.ai/download), or any client supporting Streamable HTTP
- USDT for trading (you'll deposit after setup)

## Step 1: Connect (30 seconds)

Add the Eterna MCP Gateway to your client config.

**Claude Code** -- create `.mcp.json` in your project root:

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

**Cursor** -- create `.cursor/mcp.json`:

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

Restart your client to pick up the new server.

## Step 2: Register (30 seconds)

Ask your AI agent:

> "Register a new trading agent called my-first-bot"

The agent calls `register_agent` and receives an API key like `eterna_mcp_a1b2c3d4e5f6...`.

**Save this key immediately** -- it is shown only once.

## Step 3: Authenticate (30 seconds)

Update your config to include the API key:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_a1b2c3d4e5f6..."
      }
    }
  }
}
```

Restart your client again.

## Step 4: Deposit (2-3 minutes)

Ask your agent:

> "Get my deposit address for USDT on the Arbitrum One network"

The agent calls `get_deposit_address` and returns your unique deposit address. Send USDT to this address.

Once the deposit confirms, ask:

> "Transfer my USDT from the funding wallet to the trading wallet"

The agent calls `transfer_to_trading` to move funds into your trading account.

## Step 5: Trade

Ask your agent:

> "What's the current price of BTC?"

> "Show me the ETH order book"

> "Buy 0.001 BTC at market price with 2x leverage"

> "Set a stop loss at $95,000 on my BTC position"

> "Close my BTC position"

---

## What's Next?

- **[Strategies](docs/strategies.md)** -- Momentum scalping and position sizing workflows
- **[Tools Reference](docs/tools-reference.md)** -- Full parameter docs for all 12 tools
- **[Examples](examples/)** -- LangChain, AutoGen, CrewAI, and raw Python integrations
- **[Skills](skills/)** -- Give Claude Code domain-specific trading knowledge
