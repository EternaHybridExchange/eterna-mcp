# Authentication

How authentication works in the Eterna MCP Gateway.

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

## OAuth Authentication

Agents authenticate via the MCP protocol's built-in OAuth flow. When your client connects to the gateway for the first time, the OAuth handshake is triggered automatically -- no manual header configuration required.

### How It Works

1. Your MCP client connects to `https://mcp.eterna.exchange/mcp`.
2. The gateway initiates the OAuth flow through the MCP protocol.
3. After successful authentication, all 29 SDK methods are available via `execute_code`.

### Client Configuration

Your client config only needs the server URL:

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

No `headers` field is needed. Authentication is handled automatically by the MCP protocol's OAuth flow.

---

## Error Handling

### Authentication Failures

If authentication fails, the gateway returns an error through the MCP protocol.

Common causes:

- Network connectivity issues preventing the OAuth handshake
- Expired or revoked credentials
- Client does not support the MCP OAuth flow

### Troubleshooting

1. Verify your MCP client supports Streamable HTTP transport with OAuth.
2. Check network connectivity to `https://mcp.eterna.exchange`.
3. Restart your MCP client to re-trigger the OAuth flow.
4. If problems persist, contact **contact@eterna.exchange**.
