---
name: close_position
description: Close positions and cancel orders on Eterna
---

# Close Position Skill

Close positions and cancel orders.

## Show current positions

Use `search_examples` with query `"open positions active orders"` to get the code pattern. Run via `execute_code` to show what the user has open.

## Close a position

**Confirm with user before closing.** Show current P&L so they know what they're locking in.

Use `search_examples` with query `"close position"` to get the pattern. Replace the symbol and run via `execute_code`.

Returns `{ orderId, closedSize, side, entryPrice, markPrice, unrealisedPnl }`.

## Cancel orders

Use `search_examples` with query `"cancel order"` to find patterns for:
- **Single order:** `cancelOrder(symbol, orderId)`
- **All orders on a symbol:** `cancelAllOrders(symbol)`
- **All orders across all symbols:** `cancelAllOrders()` (no args)

Run the appropriate pattern via `execute_code`.

## Modify TP/SL on existing position

Use `search_examples` with query `"set trading stop take profit stop loss"` to get the pattern. Replace symbol and price levels, then run via `execute_code`.

## SDK reference

Use `search_sdk` with `query: "close cancel"` and `detail_level: "summary"` to discover methods if needed.

| Method | Purpose |
|--------|---------|
| `getPositions(symbol?)` | List open positions with PnL |
| `getOrders(symbol?)` | List active orders |
| `closePosition(symbol)` | Market close entire position |
| `cancelOrder(symbol, orderId)` | Cancel a specific order |
| `cancelAllOrders(symbol?)` | Cancel all orders (optionally filtered by symbol) |
| `setTradingStop({ symbol, takeProfit?, stopLoss?, trailingStop?, ... })` | Modify TP/SL on existing position |
