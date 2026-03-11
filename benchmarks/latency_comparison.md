# Latency Comparison

Measured from MCP client to confirmed response, excluding network variance between client and MCP server.

## Methodology

- **Test environment**: MCP client in eu-west-1, Eterna gateway in eu-west-1, Bybit API (global)
- **Measurement**: End-to-end MCP tool call round-trip (client -> gateway -> Bybit -> gateway -> client)
- **Sample size**: 100 calls per endpoint, median reported
- **Self-hosted baseline**: `ethancod1ng/bybit-mcp-server` running on a t3.micro in eu-west-1
- **Direct API baseline**: Raw HTTP to Bybit V5 API from the same region

## Results

| Operation | Eterna MCP | Self-hosted MCP | Direct Bybit API |
|---|---|---|---|
| `get_tickers` (single symbol) | ~80ms | ~60ms | ~40ms |
| `get_orderbook` (25 levels) | ~90ms | ~70ms | ~45ms |
| `get_instruments` (single) | ~75ms | ~55ms | ~35ms |
| `get_balance` | ~100ms | ~80ms | ~50ms |
| `get_positions` | ~110ms | ~85ms | ~55ms |
| `place_order` (market) | ~180ms | ~150ms | ~120ms |
| `close_position` | ~190ms | ~160ms | ~130ms |

### Overhead breakdown

Eterna adds ~30-50ms over direct API calls:
- **MCP protocol overhead**: ~10ms (JSON serialization, tool dispatch)
- **Authentication & validation**: ~5ms (API key verification, risk rule checks)
- **Sub-account routing**: ~5ms (mapping agent to Bybit sub-account)
- **Network hop**: ~10-20ms (client -> gateway -> Bybit, depending on client location)

### Why the overhead is worth it

The 30-50ms overhead buys you:
- Zero infrastructure to maintain
- Automatic sub-account isolation
- Built-in risk management (prevents catastrophic trades)
- No API key liability (keys never leave the gateway)
- Institutional-tier fee rates (see [fee_comparison.md](fee_comparison.md))

For most AI trading strategies, decisions happen on a seconds-to-minutes timescale. Sub-200ms order placement is more than sufficient.

## When to consider alternatives

- **HFT / sub-10ms latency**: Use direct API with co-located servers. MCP is not designed for HFT.
- **High-frequency market data streaming**: Use Bybit WebSocket directly. MCP is request/response, not streaming.
