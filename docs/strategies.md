# Trading Strategies

Reference strategies for AI agents using the Eterna MCP Gateway.

---

## Momentum Scalping Strategy

A short-term strategy that identifies instruments with strong recent momentum and trades in the direction of that momentum with tight risk controls.

### Entry Signals

1. **Scan for momentum** using `get_tickers`:
   - **Long signal**: `price24hPcnt` > +0.3% (positive 24h price change)
   - **Short signal**: `price24hPcnt` < -0.3% (negative 24h price change)

2. **Confirm with orderbook** using `get_orderbook`:
   - **Long confirmation**: total bid volume >= 1.1x total ask volume (buyers dominating)
   - **Short confirmation**: total ask volume >= 1.1x total bid volume (sellers dominating)

3. If both momentum and orderbook confirmation align, enter the trade.

### Exit Rules

| Parameter | Value |
|---|---|
| **Take Profit** | 1.0% from entry price |
| **Stop Loss** | 0.6% from entry price |
| **Reward:Risk Ratio** | 1.67:1 |

Set `takeProfit` and `stopLoss` parameters when calling `place_order`. Let the exchange handle exits automatically.

### Position Limits

| Rule | Value |
|---|---|
| **Max positions per symbol** | 1 |
| **Target open positions** | 3-4 simultaneously |
| **Max open positions** | 4 |

### Workflow Cycle

1. Check current positions with `get_positions`.
2. If fewer than target positions are open, scan for new opportunities.
3. Call `get_tickers` to find momentum candidates.
4. For each candidate, call `get_orderbook` to confirm direction.
5. If confirmed and not already in that symbol, call `place_order` with TP/SL.
6. Wait and repeat the cycle.
7. Closed positions (hit TP or SL) free up slots for new trades.

---

## Position Sizing

A systematic approach to determining how much to trade per position.

### Formula

```
target_notional = equity / 4
```

Divide total equity by 4 to get the target notional value per position. This ensures no single position dominates the portfolio.

### Example

With $1,000 equity:

```
target_notional = $1,000 / 4 = $250 per position
```

At 5x leverage with BTC at $67,000:

```
qty = $250 / $67,000 = 0.00373 BTC
```

### Risk Constraints

| Constraint | Value |
|---|---|
| **Maximum leverage** | 5x |
| **Maximum positions** | 4 |
| **Maximum risk per trade** | 5% of equity |
| **Minimum account balance** | $20 USDT |

### Risk Per Trade Calculation

With a 0.6% stop loss and 5x leverage, the effective risk per trade is:

```
risk = stop_loss_pct * leverage * (position_value / equity)
risk = 0.6% * 5 * ($250 / $1,000) = 0.75% of equity
```

This is well within the 5% maximum risk per trade.

### Sizing Workflow

1. Call `get_balance` to read current equity.
2. Call `get_positions` to count open positions.
3. If open positions < 4, calculate: `target_notional = equity / 4`.
4. Look up the instrument's `lotSize` with `get_instruments` to round the quantity correctly.
5. Place the order with the calculated quantity.

---

## Deposit Flow

Before trading, funds must be deposited and transferred to the trading wallet.

### Recommended Method

Use **USDT on Arbitrum** for the lowest fees and fastest confirmation:

1. Call `get_deposit_address` with `coin: "USDT"` and `chainType: "ARBI"`.
2. Send USDT to the returned address from your external wallet.
3. Call `get_deposit_records` to monitor deposit status until it shows `"Success"`.
4. Call `transfer_to_trading` with `coin: "USDT"` and the deposited amount.
5. Call `get_balance` to confirm the trading balance is updated.

### Minimum Balance

Maintain at least **$20 USDT** in the trading wallet. Below this threshold, position sizes become too small for meaningful trading and fees have an outsized impact on returns.
