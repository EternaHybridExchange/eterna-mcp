---
name: open_position
description: Place trades on Eterna with proper sizing, leverage, and risk management
---

# Open Position Skill

Place trades with proper instrument checks, leverage, position sizing, and TP/SL.

## Before placing any trade

1. **Check balance** — don't trade with zero equity.
2. **Check existing positions** — avoid unintended doubling on the same symbol.
3. **Get instrument specs** — need `minOrderQty`, `qtyStep`, `tickSize` for proper rounding.
4. **Get user confirmation** — NEVER execute without explicit "yes"/"do it"/"go ahead".

## Pre-trade checks

Use `search_examples` with query `"pre-trade checks balance instruments positions specs"` to get the pattern. Replace the symbol and run via `execute_code`.

If equity < $20, suggest depositing more. If there's already a position on this symbol, warn the user.

## Present the trade proposal

Before executing, show the user exactly what you'll do:

> **Long LINKUSDT at ~$9.36**
> - Size: 5.3 LINK (~$50 notional, 2x leverage)
> - Margin used: ~$25 (50% of equity)
> - Stop loss: $9.17 (-2%)
> - Take profit: $9.69 (+3.5%)
> - Risk/reward: 1.75:1
>
> Should I place this?

**Be clear about margin vs notional.** "Size: X LINK (~$Y notional, Zx leverage)" so the user knows both the position value and how much margin is used.

## Execute the trade

Only after user confirms. Use `search_examples` with query `"place order position sizing leverage TP SL"` to get the order placement pattern. Adapt with the user's symbol, side, leverage, and risk parameters, then run via `execute_code`.

Key steps in the code:
1. Get instrument specs and current price
2. Set leverage via `setLeverage` (use `search_examples` with query `"set leverage"` if needed)
3. Calculate qty — round DOWN to `qtyStep`
4. Calculate TP/SL — round to `tickSize`
5. Place the order via `placeOrder`

## Confirm execution

After placing, verify the position. Use `search_examples` with query `"get open positions"` and run via `execute_code` to confirm the position was opened with correct TP/SL.

## Rules

- **First trade for new users:** max 2-3x leverage, 20-30% of equity, always set TP and SL.
- **Always round:** qty down to `qtyStep`, prices to `tickSize`.
- **Always set leverage** before placing the order — it's per-symbol.
- **Never skip confirmation** — present the proposal, wait for explicit yes.

## SDK reference

Use `search_sdk` with `methods: ["placeOrder", "setLeverage"]` and `detail_level: "params"` for exact parameter schemas.

| Method | Purpose |
|--------|---------|
| `getBalance()` | Check equity and available balance |
| `getPositions(symbol?)` | Check existing positions |
| `getInstruments(symbol?)` | Get minOrderQty, qtyStep, tickSize, maxLeverage |
| `getTickers(symbol?)` | Get current price (string — use parseFloat) |
| `setLeverage({ symbol, leverage })` | Set leverage before placing order |
| `placeOrder({ symbol, side, orderType, qty, leverage?, stopLoss?, takeProfit?, price?, reduceOnly? })` | Place the order |
