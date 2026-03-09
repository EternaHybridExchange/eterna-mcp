---
name: eterna-trading-guide
description: >
  Comprehensive trading guide for the Eterna MCP Gateway. Covers risk management
  rules, position sizing, deposit flow, and order lifecycle for Bybit perpetual
  futures trading.
---

# Eterna Trading Guide

You are connected to the Eterna MCP Gateway for Bybit USDT-settled perpetual futures trading.

## Risk Management Rules

Follow these constraints for every trade:

| Rule | Value |
|---|---|
| Maximum leverage | 5x |
| Maximum open positions | 4 |
| Maximum risk per trade | 5% of total equity |
| Minimum account balance | $20 USDT |

Never exceed these limits. Check `get_balance` and `get_positions` before placing any order.

## Position Sizing

Use this formula to determine position size:

```
target_notional = equity / 4
qty = target_notional / current_price
```

Steps:
1. Call `get_balance` to read `totalEquity`.
2. Call `get_positions` to count current open positions.
3. If open positions < 4, compute `target_notional = equity / 4`.
4. Call `get_instruments` for the symbol to get `lotSize` for rounding.
5. Compute `qty = target_notional / lastPrice`, rounded down to `lotSize`.

## Deposit Flow

Deposits arrive in the Funding wallet and must be transferred to the Trading wallet before use.

Recommended: USDT on Arbitrum (low fees, fast confirmation).

1. `get_deposit_address` with `coin: "USDT"`, `chainType: "ARBI"` -- get the deposit address.
2. Send USDT from an external wallet to the returned address.
3. `get_deposit_records` with `coin: "USDT"` -- poll until status is `"Success"`.
4. `transfer_to_trading` with `coin: "USDT"`, `amount: "<deposited amount>"` -- move to Trading wallet.
5. `get_balance` -- confirm the trading balance reflects the deposit.

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
