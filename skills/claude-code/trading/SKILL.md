---
name: eterna-trading-guide
description: >
  Comprehensive trading guide for the Eterna MCP Gateway. Covers risk management
  rules, position sizing, deposit flow, and order lifecycle for Bybit perpetual
  futures trading via execute_code + eterna.* SDK.
---

# Eterna Trading Guide

You are connected to the Eterna MCP Gateway for Bybit USDT-settled perpetual futures trading.

## How to call the exchange

Use MCP tools:

1. `search_sdk` — confirm method names and parameters
2. `execute_code` — run TypeScript that calls `eterna.*`

Do **not** call retired MCP tool names like `register_agent`, `get_tickers`, or `place_order`. Those are SDK methods now (`eterna.getTickers`, `eterna.placeOrder`, …).

## Risk Management Rules

Follow these constraints for every trade:

| Rule | Value |
|---|---|
| Maximum leverage | 5x |
| Maximum open positions | 4 |
| Maximum risk per trade | 5% of total equity |
| Minimum account balance | $20 USDT |

Never exceed these limits. Check balance and positions before placing any order:

```typescript
const balance = await eterna.getBalance();
const positions = await eterna.getPositions();
return { balance, positions };
```

## Position Sizing

```
target_notional = equity / 4
qty = target_notional / current_price
```

Steps inside `execute_code`:

1. `eterna.getBalance()` → read `totalEquity`
2. `eterna.getPositions()` → count open positions
3. If open positions < 4, compute `target_notional = equity / 4`
4. `eterna.getInstruments(symbol)` → `lotSize` / `qtyStep` for rounding
5. `eterna.getTickers(symbol)` → last price
6. Compute `qty = target_notional / lastPrice`, rounded down to lot size

## Deposit Flow

Deposits arrive in the Funding wallet and must be transferred to the Trading wallet before use.

Recommended: USDT on Arbitrum (`ARBI`).

```typescript
const addr = await eterna.getDepositAddress("USDT", "ARBI");
// user sends USDT …
const records = await eterna.getDepositRecords("USDT");
const transfer = await eterna.transferToTrading("USDT", "100");
const balance = await eterna.getBalance();
return { addr, records, transfer, balance };
```

## Order Lifecycle

### Market order

```typescript
await eterna.setLeverage("BTCUSDT", "5");
const order = await eterna.placeOrder({
  symbol: "BTCUSDT",
  side: "Buy",
  orderType: "Market",
  qty: "0.001",
  takeProfit: "68000.00",
  stopLoss: "66000.00",
});
return order;
```

### Limit order

```typescript
const order = await eterna.placeOrder({
  symbol: "BTCUSDT",
  side: "Buy",
  orderType: "Limit",
  qty: "0.001",
  price: "66500.00",
  takeProfit: "68000.00",
  stopLoss: "66000.00",
});
return order;
```

### Close position

```typescript
return await eterna.closePosition("BTCUSDT");
```

### Always set TP/SL

Every order should include `takeProfit` and `stopLoss` (or set them afterward with `eterna.setTradingStop`). Never leave a position without predefined exit levels.
