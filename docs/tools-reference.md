# Tools Reference

Complete documentation for all 12 tools exposed by the Eterna MCP Gateway.

**Gateway URL:** `https://mcp.eterna.exchange/mcp`

---

## Registration

### `register_agent`

Create a new agent account and receive an API key. This is the only tool available without authentication.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Display name for the agent |

**Returns:**

```json
{
  "agentId": "ag_abc123",
  "apiKey": "eterna_mcp_a1b2c3d4e5f6...",
  "message": "Agent registered successfully. Save your API key -- it will not be shown again."
}
```

**Notes:**
- The API key is only returned once at registration. Store it securely.
- See [authentication.md](authentication.md) for key format and usage.

---

## Market Data

### `get_tickers`

Retrieve current price, 24-hour change, volume, and funding rate for perpetual futures instruments.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | No | Trading pair symbol (e.g. `"BTCUSDT"`). Omit to get all tickers. |

**Returns:**

Array of ticker objects:

```json
[
  {
    "symbol": "BTCUSDT",
    "lastPrice": "67234.50",
    "price24hPcnt": "0.0215",
    "highPrice24h": "67800.00",
    "lowPrice24h": "65100.00",
    "volume24h": "12345.678",
    "turnover24h": "823456789.12",
    "fundingRate": "0.0001",
    "nextFundingTime": "1700000000000"
  }
]
```

---

### `get_instruments`

Retrieve contract specifications including tick size, lot size, and leverage limits.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | No | Trading pair symbol (e.g. `"BTCUSDT"`). Omit to get all instruments. |

**Returns:**

Array of instrument objects:

```json
[
  {
    "symbol": "BTCUSDT",
    "baseCoin": "BTC",
    "quoteCoin": "USDT",
    "status": "Trading",
    "tickSize": "0.10",
    "lotSize": "0.001",
    "minLeverage": "1",
    "maxLeverage": "100",
    "minOrderQty": "0.001",
    "maxOrderQty": "100.000"
  }
]
```

---

### `get_orderbook`

Retrieve the live order book for a given symbol.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | Yes | Trading pair symbol (e.g. `"BTCUSDT"`) |
| `limit` | number | No | Number of price levels per side. Range: 1-200. Default: 25. |

**Returns:**

```json
{
  "symbol": "BTCUSDT",
  "bids": [
    ["67230.00", "1.234"],
    ["67229.90", "0.567"]
  ],
  "asks": [
    ["67230.10", "0.890"],
    ["67230.20", "2.345"]
  ],
  "timestamp": 1700000000000
}
```

Each entry is a `[price, quantity]` pair. Bids are sorted descending, asks ascending.

---

## Account & Positions

### `get_balance`

Retrieve USDT balance, equity, and margin details for the trading account.

**Parameters:**

None.

**Returns:**

```json
{
  "totalEquity": "10234.56",
  "totalMarginBalance": "10234.56",
  "totalAvailableBalance": "8500.00",
  "coin": [
    {
      "coin": "USDT",
      "equity": "10234.56",
      "walletBalance": "10000.00",
      "availableToWithdraw": "8500.00",
      "unrealisedPnl": "234.56",
      "cumRealisedPnl": "1500.00"
    }
  ]
}
```

---

### `get_positions`

Retrieve all open positions or filter by symbol.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | No | Trading pair symbol (e.g. `"BTCUSDT"`). Omit to get all positions. |

**Returns:**

Array of position objects:

```json
[
  {
    "symbol": "BTCUSDT",
    "side": "Buy",
    "size": "0.100",
    "entryPrice": "67000.00",
    "markPrice": "67234.50",
    "leverage": "5",
    "unrealisedPnl": "23.45",
    "cumRealisedPnl": "150.00",
    "takeProfit": "68000.00",
    "stopLoss": "66500.00",
    "positionValue": "6723.45",
    "liqPrice": "63800.00"
  }
]
```

---

### `get_orders`

Retrieve active and recent orders.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | No | Trading pair symbol (e.g. `"BTCUSDT"`). Omit to get all orders. |

**Returns:**

Array of order objects:

```json
[
  {
    "orderId": "1234567890",
    "orderLinkId": "",
    "symbol": "BTCUSDT",
    "side": "Buy",
    "orderType": "Limit",
    "price": "66500.00",
    "qty": "0.100",
    "cumExecQty": "0.000",
    "orderStatus": "New",
    "takeProfit": "68000.00",
    "stopLoss": "66000.00",
    "createdTime": "1700000000000",
    "updatedTime": "1700000000000"
  }
]
```

---

## Trading

### `place_order`

Place a market or limit order on a perpetual futures instrument.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | Yes | Trading pair symbol (e.g. `"BTCUSDT"`) |
| `side` | string | Yes | Order side: `"Buy"` or `"Sell"` |
| `orderType` | string | Yes | Order type: `"Market"` or `"Limit"` |
| `qty` | string | Yes | Order quantity in base currency (e.g. `"0.001"`) |
| `price` | string | No | Limit price. Required for Limit orders, ignored for Market. |
| `leverage` | string | No | Leverage multiplier (e.g. `"5"`). Sets leverage before placing the order. |
| `takeProfit` | string | No | Take-profit price |
| `stopLoss` | string | No | Stop-loss price |
| `reduceOnly` | boolean | No | If `true`, the order can only reduce an existing position |

**Returns:**

```json
{
  "orderId": "1234567890",
  "orderLinkId": "eterna_abc123",
  "fillPrice": "67234.50"
}
```

**Notes:**
- Market orders execute immediately at current market price.
- Limit orders are placed on the order book and execute when price reaches the specified level.
- Always set `takeProfit` and `stopLoss` for risk management.

---

### `close_position`

Close an entire open position at market price.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `symbol` | string | Yes | Trading pair symbol of the position to close (e.g. `"BTCUSDT"`) |

**Returns:**

```json
{
  "orderId": "1234567891",
  "symbol": "BTCUSDT",
  "closedSize": "0.100",
  "positionSide": "Buy",
  "entryPrice": "67000.00",
  "exitPrice": "67234.50",
  "pnl": "23.45"
}
```

---

## Funding

### `get_deposit_address`

Get a deposit address for a specific coin and blockchain network.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `coin` | string | Yes | Coin to deposit (e.g. `"USDT"`, `"ETH"`) |
| `chainType` | string | Yes | Blockchain network: `"ETH"`, `"ARBI"`, `"SOL"`, etc. |

**Returns:**

```json
{
  "coin": "USDT",
  "chain": "ARBI",
  "address": "0xabc123...",
  "tag": ""
}
```

**Notes:**
- Arbitrum (`"ARBI"`) is recommended for USDT deposits due to low fees and fast confirmation.
- The `tag` field is empty for most chains but required for some (e.g. XRP).

---

### `get_deposit_records`

Retrieve deposit history for the account.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `coin` | string | No | Filter by coin (e.g. `"USDT"`). Omit to get all deposits. |

**Returns:**

```json
{
  "depositCount": 3,
  "deposits": [
    {
      "coin": "USDT",
      "chain": "ARBI",
      "amount": "1000.00",
      "status": "Success",
      "txID": "0xdef456...",
      "toAddress": "0xabc123...",
      "successAt": "1700000000000"
    }
  ]
}
```

---

### `transfer_to_trading`

Move funds from the Funding wallet to the Trading (Unified) wallet. Deposits arrive in the Funding wallet and must be transferred before trading.

**Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `coin` | string | Yes | Coin to transfer (e.g. `"USDT"`) |
| `amount` | string | Yes | Amount to transfer (e.g. `"500.00"`) |

**Returns:**

```json
{
  "status": "SUCCESS",
  "transferId": "tf_abc123",
  "coin": "USDT",
  "amount": "500.00",
  "from": "FUND",
  "to": "UNIFIED"
}
```

**Notes:**
- Transfers between wallets are instant and free.
- Use `get_balance` after transferring to confirm the updated trading balance.
