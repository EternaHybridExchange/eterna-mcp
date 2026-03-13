---
name: eterna-trading-guide
description: >
  Eterna MCP Gateway trading guide for Bybit USDT perpetual futures. Use when
  the user asks to trade crypto, buy, sell, open or close a position, check
  balance, scan markets, deposit funds, transfer USDT, or interact with Eterna
  or Bybit. Covers registration, deposit flow, position sizing, order placement,
  TP/SL calculation, and market scanning.
disable-model-invocation: true
---

# Eterna Trading Guide

You are connected to the Eterna MCP Gateway — a managed HTTP bridge to Bybit
USDT-settled perpetual futures. All trading happens through MCP tool calls.

MCP endpoint: `https://mcp.eterna.exchange/mcp`
Authorization: `Bearer $ETERNA_API_KEY`

---

## Registration (First-Time Setup)

If `ETERNA_API_KEY` is not set, register first — no KYC required.

1. Connect to the MCP endpoint **without** an Authorization header.
2. Call `register_agent` with a name for this agent.
3. Save the returned API key as `ETERNA_API_KEY`.
4. Reconnect with `Authorization: Bearer <key>` — all trading tools are now available.

---

## Available Tools

| Category | Tool | What it does |
|---|---|---|
| Registration | `register_agent` | Create account, receive API key |
| Market Data | `get_tickers` | Price, 24h change, volume, funding rate |
| | `get_instruments` | Contract specs, tick size, lot size, leverage limits |
| | `get_orderbook` | Live bids and asks |
| Account | `get_balance` | USDT equity, available balance, margin usage |
| | `get_positions` | Open positions: entry price, PnL, leverage |
| | `get_orders` | Active and recent order history |
| Trading | `place_order` | Market or limit orders with TP/SL |
| | `close_position` | Close entire position at market price |
| Funding | `get_deposit_address` | Deposit address for a coin and chain |
| | `get_deposit_records` | Deposit history and status |
| | `transfer_to_trading` | Move funds from Funding wallet to Trading wallet |

---

## Risk Management Rules

Follow these constraints for every trade:

| Rule | Value |
|---|---|
| Maximum leverage | 5x |
| Maximum open positions | 4 |
| Maximum risk per trade | 5% of total equity |
| Minimum account balance | $20 USDT |

Never exceed these limits. Check `get_balance` and `get_positions` before placing any order.

---

## Position Sizing

Use this formula to determine position size:

```
target_notional = equity / 4
qty = target_notional / current_price   (round DOWN to lotSize)
```

Steps:
1. Call `get_balance` to read `totalEquity`.
2. Call `get_positions` to count current open positions.
3. If open positions < 4, compute `target_notional = equity / 4`.
4. Call `get_instruments` for the symbol to get `lotSize` for rounding.
5. Call `get_tickers` for the symbol to read `lastPrice`.
6. Compute `qty = target_notional / lastPrice`, rounded down to `lotSize`.

---

## Deposit Flow

Deposits arrive in the Funding wallet and must be transferred to the Trading wallet before use.

Recommended: USDT on Arbitrum (low fees, fast confirmation).

> **Before depositing:** You need ETH in your wallet to pay the on-chain gas fee.
> Confirm your ETH balance covers the transaction fee before sending USDT.
> Without ETH, the deposit transaction will fail.

1. `get_deposit_address` with `coin: "USDT"`, `chainType: "ARBI"` — get the deposit address.
2. Confirm ETH balance in your wallet covers the Arbitrum gas fee.
3. Send USDT from your external wallet to the returned address.
4. `get_deposit_records` with `coin: "USDT"` — poll until status is `"Success"`.
5. `transfer_to_trading` with `coin: "USDT"`, `amount: "<deposited amount>"` — move to Trading wallet.
6. `get_balance` — confirm the trading balance reflects the deposit.

---

## Order Lifecycle

### Market Orders

Execute immediately at current market price. Use for entries and exits when speed matters.

```
place_order:
  symbol: "BTCUSDT"
  side: "Buy"
  orderType: "Market"
  qty: "0.001"
  leverage: "5"
  takeProfit: "68000.00"
  stopLoss: "66000.00"
```

### Limit Orders

Placed on the order book. Execute when price reaches the specified level. Use for better entry prices.

```
place_order:
  symbol: "BTCUSDT"
  side: "Buy"
  orderType: "Limit"
  qty: "0.001"
  price: "66500.00"
  leverage: "5"
  takeProfit: "68000.00"
  stopLoss: "66000.00"
```

### Closing Positions

To close an entire position at market price:

```
close_position:
  symbol: "BTCUSDT"
```

### Always Set TP/SL

Every order must include `takeProfit` and `stopLoss` parameters. Never leave a position without predefined exit levels.

---

## TP/SL Calculation

Calculate TP/SL from the actual entry price — never use hardcoded values.

For a **long** entry at price P:
```
takeProfit = P * 1.10   (+10%)
stopLoss   = P * 0.94   (-6%)
```

For a **short** entry at price P:
```
takeProfit = P * 0.90   (-10%)
stopLoss   = P * 1.06   (+6%)
```

Reward-to-risk ratio: **1.67:1**

---

## Market Scanning

Use this to find trade candidates before placing orders.

### Step 1 — Scan for momentum

`get_tickers` (no symbol filter):
- Long candidates: `price24hPcnt` > +0.003 (more than +0.3% in 24h)
- Short candidates: `price24hPcnt` < -0.003 (more than -0.3% in 24h)

### Step 2 — Confirm with orderbook

`get_orderbook` with `limit: 50`, then:
```
total_bid_volume = sum of all bid quantities
total_ask_volume = sum of all ask quantities
```
- Long confirmed: `total_bid_volume >= 1.1 * total_ask_volume`
- Short confirmed: `total_ask_volume >= 1.1 * total_bid_volume`

Only enter if momentum direction and orderbook imbalance agree.

### Step 3 — Check position limits

- Call `get_positions` — do not enter if already holding this symbol.
- Do not enter if total open positions >= 4.
