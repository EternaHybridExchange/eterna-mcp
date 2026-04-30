---
name: market_scan
description: Live market scanning, technical analysis, and trade idea generation
---

# Market Scan Skill

Scan live markets and generate trade ideas using the Eterna MCP tools.

## Quick market briefing

Use `search_examples` with query `"market briefing BTC ETH RSI MACD Bollinger top movers"` to get the code pattern. Adapt and run it via `execute_code`.

**Present as a market briefing, not raw data.** Example tone:

> BTC at $94,200 — up 1.3%. RSI 62 on the hourly, MACD flipping bullish. Bollinger Bands tight (1.8%) — a move is brewing.
> SUI is the big mover — up 8.4% with $340M volume. ETH flat at +0.2%.

**Important:** Filter top movers to `turnover24h > 5_000_000` to avoid obscure low-volume tokens.

## Trade idea scan

When the user wants trade ideas, use `search_examples` with query `"trade idea scan momentum mean-reversion scoring RSI MACD Bollinger"` to get the scoring pattern. Run it via `execute_code`.

**Present trade ideas with reasoning:** signal, confirmation, entry/stop/target, risk/reward. If nothing looks good, say so — "market's choppy, I wouldn't trade right now" builds more trust than a forced idea.

## Deep-dive on a symbol

When the user asks about a specific symbol, use `search_examples` with query `"deep-dive analysis multi-timeframe RSI MACD Bollinger VWAP orderbook"` to get the pattern. Replace the symbol and run via `execute_code`.

Synthesize — identify confluence (multiple indicators agreeing) and conflicts (RSI overbought but MACD still bullish). Lead with the actionable insight.

## SDK reference

If you need to discover additional methods or check exact signatures, use `search_sdk`:

- `search_sdk` with `query: "technical analysis"` and `detail_level: "summary"` — to find TA methods
- `search_sdk` with `methods: ["getRsi", "getMacd"]` and `detail_level: "full"` — for exact signatures

Valid intervals: `1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `1d`, `1w`. TA methods return numbers (no parseFloat needed). Bybit ticker values are strings (parseFloat needed).
