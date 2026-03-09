# Authentication

How API keys work in the Eterna MCP Gateway.

---

## API Key Format

```
eterna_mcp_<64 hexadecimal characters>
```

Total length: **75 characters**.

Example:

```
eterna_mcp_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
```

## Key Generation

- Generated using cryptographically secure random bytes.
- The raw key is hashed with **Argon2** before storage. The gateway never stores plaintext keys.
- The key is returned **exactly once** during `register_agent`. There is no way to retrieve it later.
- Treat your API key like a password. If lost, you must register a new agent.

---

## Connection Modes

The gateway operates in two modes depending on whether an API key is provided:

### Unauthenticated Mode

When no API key is provided, only one tool is available:

| Tool | Description |
|---|---|
| `register_agent` | Create a new agent account and receive an API key |

This allows new agents to self-register without requiring out-of-band key distribution.

### Authenticated Mode

When a valid API key is provided, all 12 tools are available including market data, account management, trading, and funding operations.

---

## Providing the API Key

Pass the API key as a Bearer token in the `Authorization` HTTP header:

```
Authorization: Bearer eterna_mcp_a1b2c3d4e5f6...
```

In MCP client configuration, this is set via the `headers` field:

```json
{
  "mcpServers": {
    "eterna-trading": {
      "type": "streamable-http",
      "url": "https://mcp.eterna.exchange/mcp",
      "headers": {
        "Authorization": "Bearer eterna_mcp_your_key_here"
      }
    }
  }
}
```

---

## Error Handling

### Invalid or Missing Key

If the API key is invalid, expired, or missing when calling an authenticated tool, the gateway returns an HTTP `401 Unauthorized` response.

Common causes:

- Typo in the API key
- Key was not included in the `Authorization` header
- Using a key that was never registered
- Incorrect header format (must be `Bearer <key>`, not just the key)

### Troubleshooting

1. Verify the key starts with `eterna_mcp_` and is exactly 75 characters.
2. Confirm the `Authorization` header uses the `Bearer ` prefix (with a space).
3. Check that the header is being sent with every request (some clients may strip custom headers).
4. If the key is lost, register a new agent with `register_agent`.
