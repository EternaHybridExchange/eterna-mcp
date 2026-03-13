---
name: eterna-trading
description: >
  Connects to the Eterna MCP Gateway to trade Bybit USDT perpetual futures.
  Covers registration, deposit flow, position sizing, market and limit orders,
  take-profit and stop-loss management, and momentum scalping. Use when the user
  asks to trade crypto, place an order, check balance, scan markets, deposit
  funds, or interact with Eterna or Bybit.
primaryEnv: ETERNA_API_KEY
requires:
  env:
    - ETERNA_API_KEY
---

# Eterna MCP Trading Guide

You are connected to the Eterna MCP Gateway — a managed HTTP bridge to Bybit
USDT-settled perpetual futures. All trading happens through MCP tool calls.

MCP endpoint: `https://mcp.eterna.exchange/mcp`
Authorization: `Bearer $ETERNA_API_KEY`
usefull skills:
  - lunarpulse/openclaw-mcp-plugin - interaction with Eterna MCP
  - surfer77/evm-wallet - for wallet operations

---

## Registration (First-Time Setup)

If `ETERNA_API_KEY` is not set, register first — no KYC required.

1. Connect to the MCP endpoint **without** an Authorization header.
2. Call `register_agent` with your name for this agent.
3. Save the returned API key as `ETERNA_API_KEY`.
4. Reconnect with `Authorization: Bearer <key>` — all trading tools are now available.

---

## Risk Management Rules

**Check these before every order — no exceptions.**

| Rule | Limit |
|---|---|
| Minimum leverage | 1x |
| Maximum leverage | 100x |

```
get_balance    → check totalEquity and availableBalance
get_positions  → count open positions before entering

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

## Deposit Flow

Deposits land in the **Funding wallet** first. Move them before trading.

Recommended: USDT on Arbitrum (low fees, fast confirmation).

> **Before depositing:** You need ETH in your wallet to pay the on-chain gas fee.
> Use the `evm-wallet` skill to check your ETH balance and ensure it covers the
> transaction fee before sending USDT. Without ETH, the deposit transaction will fail.

1. `get_deposit_address` — `coin: "USDT"`, `chainType: "ARBI"`
2. Verify ETH balance in your EVM wallet covers the gas fee (via `evm-wallet` skill).
3. Send USDT to the returned address from your EVM wallet.
4. `get_deposit_records` — `coin: "USDT"` — poll until `status: "Success"`.
5. `transfer_to_trading` — `coin: "USDT"`, `amount: "<deposited amount>"`
6. `get_balance` — confirm trading balance reflects the deposit.

---

## Position Sizing

```
target_notional = totalEquity / 4
qty = target_notional / lastPrice   (round DOWN to lotSize)
```

Steps:
1. `get_balance` → read `totalEquity`
2. `get_positions` → count open positions 
3. `get_instruments` for the symbol → read `lotSize`
4. `get_tickers` for the symbol → read `lastPrice`
5. Compute qty, round down to `lotSize`

---

## Placing Orders

### Market Order (immediate execution)

```
place_order:
  symbol:      "BTCUSDT"
  side:        "Buy"          # or "Sell"
  orderType:   "Market"
  qty:         "0.001"
  leverage:    "5"
  takeProfit:  "68000.00"
  stopLoss:    "66000.00"
```

### Limit Order (executes at target price)

```
place_order:
  symbol:      "BTCUSDT"
  side:        "Buy"
  orderType:   "Limit"
  price:       "66500.00"
  qty:         "0.001"
  leverage:    "5"
  takeProfit:  "68000.00"
  stopLoss:    "66000.00"
```

### Close a Position

```
close_position:
  symbol: "BTCUSDT"
```

**Always include `takeProfit` and `stopLoss` on every `place_order` call.**
Never leave a position open without predefined exit levels, unless your human asks you to.

---

## TP/SL Calculation

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

## Momentum Scalping Workflow

Use this when scanning markets for trade opportunities.

### Step 1 — Scan for momentum

`get_tickers` (no symbol filter):
- Long candidates: `price24hPcnt` > +0.003
- Short candidates: `price24hPcnt` < -0.003

### Step 2 — Confirm with orderbook

`get_orderbook` with `limit: 50`, then:
```
total_bid_volume = sum of all bid quantities
total_ask_volume = sum of all ask quantities
```
- Long confirmed: `total_bid_volume >= 1.1 * total_ask_volume`
- Short confirmed: `total_ask_volume >= 1.1 * total_bid_volume`

Only enter if momentum and orderbook imbalance agree.

### Step 3 — Full cycle

1. `get_balance` — verify equity >= $20
2. `get_positions` — verify open positions < 4
3. `get_tickers` — find momentum candidates
4. For each candidate not already in portfolio:
   - `get_orderbook` — confirm imbalance
   - Calculate qty (position sizing formula above)
   - Calculate TP/SL prices
   - `place_order` with `orderType: "Market"`, leverage <= 5x
5. Let TP/SL execute automatically — do not manually close unless required.
6. Repeat from step 1.

---

## Key Rules

- Never hold more than 1 position per symbol.
- Always set both `takeProfit` and `stopLoss` on every order.
- Always check balance and positions before placing any order.
- Minimum $20 USDT equity to trade.
