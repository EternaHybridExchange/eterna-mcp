# Open Position — Detailed Guide

## Mandatory sequence

1. **Pre-trade checks** — balance, existing positions, instrument specs, current price
2. **Present proposal** — show exact entry, size, leverage, margin, TP, SL, R:R
3. **Get confirmation** — NEVER execute without explicit "yes"/"do it"/"go ahead"
4. **Execute** — set leverage, place order
5. **Verify** — check position opened correctly

## Pre-trade checks
Use `search_examples` with query `"pre-trade checks balance instruments positions specs"`. Replace symbol.

- If equity < $20, suggest depositing more.
- If there's already a position on this symbol, warn the user.

## Trade proposal format

> **Long LINKUSDT at ~$9.36**
> - Size: 5.3 LINK (~$50 notional, 2x leverage)
> - Margin used: ~$25 (50% of equity)
> - Stop loss: $9.17 (-2%)
> - Take profit: $9.69 (+3.5%)
> - Risk/reward: 1.75:1
>
> Should I place this?

**Be clear about margin vs notional.** Show both position value and margin used.

## Execution steps
Use `search_examples` with query `"place order position sizing leverage TP SL"`.

1. Get instrument specs (`minOrderQty`, `qtyStep`, `tickSize`) and current price
2. Set leverage: `search_examples` with query `"set leverage"`
3. Calculate qty — round **DOWN** to `qtyStep`
4. Calculate TP/SL — round to `tickSize` (ceil for favorable, floor for stop)
5. Place order via `placeOrder`

## Sizing rules

- **First trade / new users:** max 2-3x leverage, 20-30% of equity
- **Always round:** qty down to `qtyStep`, prices to `tickSize`
- **Always set leverage** before placing — it's per-symbol
- **Always set both TP and SL**

## SDK quick reference

| Method | Purpose |
|--------|---------|
| `getBalance()` | Equity and available balance |
| `getPositions(symbol?)` | Existing positions |
| `getInstruments(symbol?)` | minOrderQty, qtyStep, tickSize, maxLeverage |
| `getTickers(symbol?)` | Current price (string — parseFloat) |
| `setLeverage({ symbol, leverage })` | Set before placing order |
| `placeOrder({ symbol, side, orderType, qty, leverage?, stopLoss?, takeProfit?, price? })` | Place the order |
