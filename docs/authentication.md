# Authentication

How agents authenticate to the Eterna MCP Gateway.

**Gateway:** `https://mcp.eterna.exchange/mcp`  
**OAuth issuer:** `https://ai-auth.eterna.exchange`  
**Scope:** `mcp:full`

---

## Preferred: OAuth

Claude connectors, Cursor MCP, and most modern MCP clients use OAuth.

1. Client reads protected-resource / authorization-server metadata.
2. User completes sign-in / consent.
3. Client calls MCP with `Authorization: Bearer <access_token>`.
4. On first successful OAuth identity, the gateway **auto-provisions** an isolated agent sub-account (lazy Bybit sub-account on first trading use).

There is **no** `register_agent` MCP tool.

### Discovery endpoints

| Resource | URL |
|---|---|
| OAuth authorization server | `https://ai-auth.eterna.exchange/.well-known/oauth-authorization-server` |
| Protected resource (AI landing) | `https://ai.eterna.exchange/.well-known/oauth-protected-resource` |
| Protected resource (MCP host) | `https://mcp.eterna.exchange/.well-known/oauth-protected-resource` |
| MCP server card | `https://ai.eterna.exchange/.well-known/mcp/server-card.json` |

Human-readable mirror: https://ai.eterna.exchange/auth.md

---

## Legacy: agent API keys

Custom clients and CLI workflows may still use long-lived agent API keys:

```
Authorization: Bearer eterna_mcp_<hex…>
```

### Security model

- Keys are generated with cryptographically secure randomness.
- The gateway stores an **Argon2** hash, never plaintext.
- Treat the key like a password. If lost, mint a new key via the supported CLI / account flow (do not expect a `register_agent` tool).

### Client config example

```json
{
  "mcpServers": {
    "eterna": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

OAuth clients should **omit** a hardcoded API key and complete the connector sign-in instead.

---

## What auth unlocks

Once authenticated, the agent can call:

- `search_sdk`
- `execute_code`
- `search_examples`

plus prompts/resources (`getting_started`, `eterna://docs/sdk`, …).

Unauthenticated trading is not supported.

---

## Common errors

### `401 Unauthorized`

- Missing `Authorization` header
- Expired OAuth access token (refresh / re-auth)
- Typo in legacy API key
- Client stripped custom headers

### Troubleshooting

1. Confirm the MCP URL is exactly `https://mcp.eterna.exchange/mcp`.
2. For OAuth clients, re-run connector sign-in.
3. For API keys, confirm `Bearer ` prefix (with a space).
4. Verify the client keeps headers on every MCP HTTP request.
