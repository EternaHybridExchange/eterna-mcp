# Architecture

Technical overview of the Eterna MCP Gateway design.

---

## Agent Isolation

Each registered agent receives a **dedicated Bybit sub-account**. This provides strong isolation between agents:

- **Separate balances** -- funds deposited by one agent are not visible to others.
- **Separate positions** -- each agent manages its own positions independently.
- **Separate API credentials** -- the gateway holds scoped sub-account API keys that can only operate on that agent's sub-account.
- **No cross-contamination** -- one agent cannot view, modify, or interact with another agent's account in any way.

```
Agent A  -->  Gateway  -->  Bybit Sub-Account A
Agent B  -->  Gateway  -->  Bybit Sub-Account B
Agent C  -->  Gateway  -->  Bybit Sub-Account C
```

---

## Security Model

### API Key Hashing

Agent API keys are hashed using **Argon2** (the winner of the Password Hashing Competition) before storage. The gateway never persists plaintext keys. Even in the event of a database breach, API keys cannot be recovered.

### Scoped Sub-Account Keys

Each sub-account is provisioned with Bybit API keys that are scoped to that sub-account only. These keys:

- Cannot access the master account
- Cannot access other sub-accounts
- Are stored encrypted at rest

### Gateway as Proxy

The gateway acts as a secure proxy between the agent and Bybit:

1. Agent sends an MCP tool call to the gateway.
2. Gateway authenticates the agent via the Bearer token.
3. Gateway translates the MCP tool call into the appropriate Bybit API request.
4. Gateway signs the request with the agent's scoped sub-account API key.
5. Gateway returns the Bybit response as an MCP tool result.

The agent never sees or handles Bybit API keys directly.

---

## Transport Protocol

The gateway uses **MCP Streamable HTTP** as its transport layer.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/mcp` | Send MCP requests (tool calls, resource reads, prompt requests) |
| `GET` | `/mcp` | Open an SSE stream for server-initiated messages |
| `DELETE` | `/mcp` | Terminate the current session |

### Sessions

Sessions are managed via the `mcp-session-id` HTTP header:

1. The first `POST /mcp` request (with `initialize`) creates a new session.
2. The gateway returns an `mcp-session-id` header in the response.
3. All subsequent requests must include this session ID header.
4. Sessions can be terminated with `DELETE /mcp`.

### Content Type

All requests and responses use `application/json` content type following the MCP JSON-RPC 2.0 format.

---

## Market Support

The gateway currently supports:

| Property | Value |
|---|---|
| **Market type** | Linear (USDT-settled) perpetual futures |
| **Settlement currency** | USDT |
| **Margin mode** | Cross margin |
| **Position mode** | One-way (net position) |

### What This Means

- **Linear perpetual futures** -- contracts settled in USDT, not the underlying asset. PnL is always in USDT.
- **Cross margin** -- all available USDT balance is shared across positions as margin. This provides more flexibility but means a large loss on one position can affect margin available for others.
- **One-way position mode** -- each symbol has a single net position. Buying while short reduces the short; you cannot hold simultaneous long and short positions on the same symbol.

### Available Instruments

All USDT-settled perpetual futures listed on Bybit are available. Use the `get_instruments` tool to retrieve the current list with contract specifications.
