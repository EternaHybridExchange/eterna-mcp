# Tools Reference

Eterna MCP Gateway tool and SDK documentation.

**Gateway URL:** `https://mcp.eterna.exchange/mcp`  
**Transport:** Streamable HTTP  
**Auth:** OAuth (`mcp:full`) preferred; legacy Bearer API keys supported

---

## Architecture note

Older docs described **12 MCP tools** (`register_agent`, `get_tickers`, `place_order`, …). That model is **retired**.

Current model:

| Layer | What exists |
|---|---|
| MCP tools | `execute_code`, `search_sdk`, `search_examples` |
| Trading API surface | 29 `eterna.*` SDK methods **inside** `execute_code` |

If an agent still tries to call `register_agent` or `get_tickers` as MCP tools, it is following outdated documentation.

---

## MCP tools

### `search_sdk`

Search the SDK documentation before writing code.

Typical detail levels: `list`, `summary`, `full`, `params`, `keywords` (exact parameter names depend on the live tool schema — ask the client to introspect tools).

**When to use:** every time the agent is unsure which method exists or what arguments it takes.

---

### `execute_code`

Run TypeScript in a sandboxed Deno runtime with the `eterna.*` SDK injected.

**Code rules:**

- Code is an async function body
- Use `await` for all SDK calls
- Use `return <value>` for the result (JSON-serialized)
- Use `console.log()` for intermediate output
- Most numeric exchange fields arrive as **strings** — use `parseFloat()` for arithmetic
- Technical analysis helpers (`getRsi`, `getMacd`, …) return **numbers**

**Minimal example:**

```typescript
const balance = await eterna.getBalance();
const ticker = await eterna.getTickers("BTCUSDT");
return {
  equity: balance.totalEquity,
  available: balance.totalAvailableBalance,
  last: ticker[0]?.lastPrice,
};
```

**Deposit + transfer example:**

```typescript
const addr = await eterna.getDepositAddress("USDT", "ARBI");
// …user sends USDT …
const records = await eterna.getDepositRecords("USDT");
const transfer = await eterna.transferToTrading("USDT", "100");
return { addr, records, transfer };
```

**Trade example:**

```typescript
await eterna.setLeverage("BTCUSDT", "2");
const order = await eterna.placeOrder({
  symbol: "BTCUSDT",
  side: "Buy",
  orderType: "Market",
  qty: "0.001",
  takeProfit: "120000",
  stopLoss: "95000",
});
return order;
```

For full parameter schemas, call `search_sdk` with detail `full` / `params`, or read the `sdk_reference` prompt / `eterna://docs/sdk` resource.

---

### `search_examples`

Semantic search over curated `execute_code` snippets (deposit flow, indicators, order placement, etc.).

---

## SDK methods (via `execute_code`)

### Market data

| Method | Description |
|---|---|
| `eterna.getTickers(symbol?)` | Price, 24h change, volume, funding. Omit symbol for all pairs. |
| `eterna.getOrderbook(symbol, limit?)` | Live bids/asks (`limit` 1-200, default 25) |
| `eterna.getInstruments(symbol?)` | Contract specs: tick size, lot size, leverage limits |

### Technical analysis

| Method | Description |
|---|---|
| `eterna.getRsi(symbol, interval, period?)` | RSI (0-100) |
| `eterna.getMacd(symbol, interval, …)` | MACD line, signal, histogram |
| `eterna.getEma(symbol, interval, period?)` | EMA |
| `eterna.getSma(symbol, interval, period?)` | SMA |
| `eterna.getBollingerBands(symbol, interval, …)` | Upper / middle / lower |
| `eterna.getVwap(symbol, interval)` | VWAP |

### Trading

| Method | Description |
|---|---|
| `eterna.placeOrder(params)` | Market/limit order with optional TP/SL |
| `eterna.closePosition(symbol)` | Close entire position at market |
| `eterna.cancelOrder(…)` | Cancel a single order |
| `eterna.cancelAllOrders(symbol?)` | Cancel open orders |
| `eterna.setLeverage(symbol, leverage)` | Set leverage |
| `eterna.setTradingStop(…)` | Update TP/SL on an open position |

### Account

| Method | Description |
|---|---|
| `eterna.getBalance()` | Equity, available margin, unrealised PnL |
| `eterna.getAccountInfo()` | Account configuration / mode |
| `eterna.getAllCoinsBalance()` | Multi-coin balances |
| `eterna.getPositions(symbol?)` | Open positions |
| `eterna.getOrders(symbol?)` | Active / recent orders |

### Funding

| Method | Description |
|---|---|
| `eterna.getAllowedDepositCoins(coin?)` | Supported coins/chains and mins |
| `eterna.getDepositAddress(coin, chainType)` | Deposit address (+ tag if needed) |
| `eterna.getDepositRecords(coin?)` | Deposit history |
| `eterna.transferToTrading(coin, amount)` | Funding wallet → trading wallet |
| `eterna.swapToUsdt(…)` | Swap balances to USDT |
| `eterna.getCoinInfo(…)` | Coin metadata |
| `eterna.getWithdrawableAmount(…)` | Withdrawable amounts |
| `eterna.submitWithdrawal(…)` | Submit a withdrawal |
| `eterna.getWithdrawalStatus(…)` | Withdrawal status |

---

## Errors and rate limits

`execute_code` responses include an error category and hint when something fails. Prefer the live `error_handling` prompt and `eterna://docs/errors` resource over hard-coding recovery logic.

Common categories include validation errors, insufficient balance, exchange rejections, and infrastructure / timeout failures. Do **not** blindly retry infrastructure errors with new generated code.

---

## Deprecated MCP tool names

Do **not** document or call these as MCP tools anymore:

- `register_agent`
- `get_tickers`, `get_instruments`, `get_orderbook`
- `get_balance`, `get_positions`, `get_orders`
- `place_order`, `close_position`
- `get_deposit_address`, `get_deposit_records`, `transfer_to_trading`

Use the camelCase `eterna.*` SDK equivalents inside `execute_code` instead.
