---
name: eterna-momentum-scalping
description: >
  Momentum scalping strategy for the Eterna MCP Gateway. Identifies instruments
  with strong 24h momentum, confirms with orderbook imbalance, and trades with
  tight take-profit and stop-loss levels.
---

# Momentum Scalping Strategy

A short-term trading strategy that rides existing momentum with tight risk controls.

## Entry Criteria

### Step 1: Scan for Momentum

Call `get_tickers` (no symbol filter) and scan for candidates:

- **Long candidates**: `price24hPcnt` > +0.003 (more than +0.3% in 24h)
- **Short candidates**: `price24hPcnt` < -0.003 (more than -0.3% in 24h)

### Step 2: Confirm with Orderbook

For each candidate, call `get_orderbook` with `limit: 50` and calculate:

```
total_bid_volume = sum of all bid quantities
total_ask_volume = sum of all ask quantities
```

- **Long confirmation**: `total_bid_volume >= 1.1 * total_ask_volume`
- **Short confirmation**: `total_ask_volume >= 1.1 * total_bid_volume`

Only enter if momentum direction and orderbook imbalance agree.

### Step 3: Check Position Limits

Before entering:
- Call `get_positions` to check current open positions.
- Do NOT enter if already holding a position in this symbol (max 1 per symbol).
- Do NOT enter if total open positions >= 4 (target 3-4 total).

## Exit Rules

Set these on every `place_order` call:

| Parameter | Value |
|---|---|
| `takeProfit` | 1.0% from entry price |
| `stopLoss` | 0.6% from entry price |

This gives a **1.67:1 reward-to-risk ratio**.

### Calculating TP/SL Prices

For a **long** entry at price P:
```
takeProfit = P * 1.010
stopLoss   = P * 0.994
```

For a **short** entry at price P:
```
takeProfit = P * 0.990
stopLoss   = P * 1.006
```

## Position Sizing

Use the standard formula:
```
target_notional = equity / 4
qty = target_notional / current_price
```

Round `qty` down to the instrument's `lotSize` (from `get_instruments`).

## Full Cycle Workflow

1. `get_balance` -- check equity meets $20 minimum.
2. `get_positions` -- count open positions.
3. If open positions < 4:
   a. `get_tickers` -- find momentum candidates.
   b. For each candidate not already in portfolio:
      - `get_orderbook` -- confirm imbalance.
      - If confirmed, calculate qty and TP/SL prices.
      - `place_order` with `orderType: "Market"`, TP, SL, and leverage <= 5x.
4. Wait for positions to hit TP or SL (the exchange handles this automatically).
5. Repeat from step 1.

## Key Rules

- Never hold more than 1 position per symbol.
- Target 3-4 open positions at any time.
- Maximum 4 open positions.
- Maximum 5x leverage.
- Always set both take-profit and stop-loss.
- Let TP/SL execute automatically -- do not manually close unless strategy logic requires it.
