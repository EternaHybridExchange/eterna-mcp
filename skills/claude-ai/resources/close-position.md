# Close Position — Detailed Guide

## Show current positions
Use `search_examples` with query `"open positions active orders"`.

## Close a position
**Confirm with user before closing.** Show current P&L so they know what they're locking in.

Use `search_examples` with query `"close position"`. Replace symbol.

Returns `{ orderId, closedSize, side, entryPrice, markPrice, unrealisedPnl }`.

## Cancel orders
Use `search_examples` with query `"cancel order"`:
- **Single order:** `cancelOrder(symbol, orderId)`
- **All on a symbol:** `cancelAllOrders(symbol)`
- **All symbols:** `cancelAllOrders()` (no args)

## Modify TP/SL
Use `search_examples` with query `"set trading stop take profit stop loss"`. Replace symbol and price levels.

## SDK quick reference

| Method | Purpose |
|--------|---------|
| `getPositions(symbol?)` | Open positions with PnL |
| `getOrders(symbol?)` | Active orders |
| `closePosition(symbol)` | Market close entire position |
| `cancelOrder(symbol, orderId)` | Cancel specific order |
| `cancelAllOrders(symbol?)` | Cancel all orders |
| `setTradingStop({ symbol, takeProfit?, stopLoss? })` | Modify TP/SL on existing position |
