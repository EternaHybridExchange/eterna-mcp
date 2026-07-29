---
name: eterna-momentum-scalping
description: >
  Momentum scalping strategy for the Eterna MCP Gateway. Identifies instruments
  with strong 24h momentum, confirms with orderbook imbalance, and trades with
  tight take-profit and stop-loss levels via execute_code + eterna.* SDK.
---

# Momentum Scalping Strategy

A short-term trading strategy that rides existing momentum with tight risk controls.

Use `search_sdk` then `execute_code`. Do not call retired MCP tool names (`get_tickers`, `place_order`, …).

## Entry Criteria

### Step 1: Scan for Momentum

```typescript
const tickers = await eterna.getTickers();
const longs = tickers.filter((t) => parseFloat(t.price24hPcnt) > 0.003);
const shorts = tickers.filter((t) => parseFloat(t.price24hPcnt) < -0.003);
return { longs: longs.slice(0, 10), shorts: shorts.slice(0, 10) };
```

- **Long candidates**: `price24hPcnt` > +0.003 (+0.3% in 24h)
- **Short candidates**: `price24hPcnt` < -0.003 (-0.3% in 24h)

### Step 2: Confirm with Orderbook

```typescript
const book = await eterna.getOrderbook(symbol, 50);
const bidVol = book.bids.reduce((s, [, q]) => s + parseFloat(q), 0);
const askVol = book.asks.reduce((s, [, q]) => s + parseFloat(q), 0);
return { bidVol, askVol, longOk: bidVol >= 1.1 * askVol, shortOk: askVol >= 1.1 * bidVol };
```

- **Long confirmation**: bid volume >= 1.1 × ask volume
- **Short confirmation**: ask volume >= 1.1 × bid volume

### Step 3: Check Position Limits

```typescript
const positions = await eterna.getPositions();
return {
  count: positions.length,
  hasSymbol: positions.some((p) => p.symbol === symbol),
};
```

- Do NOT enter if already holding this symbol (max 1 per symbol)
- Do NOT enter if total open positions >= 4

## Exit Rules

Set these on every `eterna.placeOrder` call:

| Parameter | Value |
|---|---|
| `takeProfit` | 1.0% from entry price |
| `stopLoss` | 0.6% from entry price |
| Leverage | <= 5x via `eterna.setLeverage` |

## Example entry

```typescript
await eterna.setLeverage(symbol, "3");
const order = await eterna.placeOrder({
  symbol,
  side: "Buy", // or "Sell"
  orderType: "Market",
  qty,
  takeProfit,
  stopLoss,
});
return order;
```

## Cycle workflow

Prefer one `execute_code` call per cycle: scan → confirm → size → place (or skip) → return a structured summary.
