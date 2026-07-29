# Architecture

Technical overview of the Eterna MCP Gateway design.

---

## Execution model

Agents do not call one MCP tool per exchange endpoint.

```
Agent  -->  MCP tools (search_sdk / execute_code / search_examples)
       -->  Deno sandbox + eterna.* SDK
       -->  Gateway signs Bybit requests with the agent's scoped sub-account key
```

`execute_code` runs user TypeScript in an isolated sandbox. The SDK proxy is the only path to exchange APIs.

---

## Agent Isolation

Each authenticated agent receives a **dedicated Bybit sub-account** (provisioned lazily):

- **Separate balances** — funds deposited by one agent are not visible to others.
- **Separate positions** — each agent manages its own positions independently.
- **Separate exchange credentials** — the gateway holds scoped sub-account API keys that can only operate on that agent's sub-account.
- **No cross-contamination** — one agent cannot view, modify, or interact with another agent's account.

```
Agent A  -->  Gateway  -->  Bybit Sub-Account A
Agent B  -->  Gateway  -->  Bybit Sub-Account B
Agent C  -->  Gateway  -->  Bybit Sub-Account C
```

Identity comes from OAuth (`oauthUserId`) or a legacy agent API key.

---

## Security Model

### OAuth (preferred)

Claude / Cursor connectors authenticate against `https://ai-auth.eterna.exchange` with scope `mcp:full`. The gateway validates the JWT and auto-provisions the agent record.

### Legacy API key hashing

Legacy agent API keys are hashed with **Argon2** before storage. The gateway never persists plaintext keys.

### Scoped Sub-Account Keys

Each sub-account is provisioned with Bybit API keys that are scoped to that sub-account only. These keys:

- Cannot access the master account
- Cannot access other sub-accounts
- Are stored encrypted at rest

### Gateway as Proxy

1. Agent sends an MCP tool call (`execute_code`, `search_sdk`, …).
2. Gateway authenticates the agent (OAuth JWT or legacy API key).
3. For `execute_code`, the sandbox invokes typed `eterna.*` methods.
4. Gateway signs Bybit requests with the agent's scoped sub-account key.
5. Gateway returns the result as an MCP tool response.

The agent never sees or handles Bybit API keys directly.

---

## Transport Protocol

The gateway uses **MCP Streamable HTTP**.

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

- **USDT-margined perpetual futures** (200+ pairs)
- Spot trading is on the roadmap (see [ROADMAP.md](../ROADMAP.md))
