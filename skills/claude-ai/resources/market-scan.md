# Market Scan — Detailed Guide

## Presentation rules

Present results as a **market briefing narrative**, not raw data.

Example tone:
> BTC at $94,200 — up 1.3%. RSI 62 on the hourly, MACD flipping bullish. Bollinger Bands tight (1.8%) — a move is brewing.
> SUI is the big mover — up 8.4% with $340M volume. ETH flat at +0.2%.

**Filter top movers** to `turnover24h > 5_000_000` to avoid obscure low-volume tokens.

## Trade idea presentation

Present with the full reasoning chain: **signal → confirmation → risk management**.

> **Long SUI at $3.82** — up 6.2% but RSI only 58 (room to run). MACD histogram positive and growing. BB position at 72%.
> Stop: $3.74 (-2.1%), Target: $3.95 (+3.4%). R:R 1.6:1. Size: ~25% of equity at 3x.

If nothing looks good, say so. "Market's choppy, I wouldn't trade right now" builds more trust than a forced idea.

## Deep-dive synthesis

When analyzing a single symbol:
- Identify **confluence** — multiple indicators agreeing (RSI + MACD + BB all bullish)
- Flag **conflicts** — RSI overbought but MACD still bullish
- Lead with the **actionable insight**, not the data

## SDK quick reference

| Method | Returns |
|--------|---------|
| `getTickers(symbol?)` | `{ list: [{ symbol, lastPrice, price24hPcnt, turnover24h, fundingRate }] }` — strings |
| `getRsi(symbol, interval, period?)` | `{ value: number }` — 0-100 |
| `getMacd(symbol, interval)` | `{ valueMACD, valueMACDSignal, valueMACDHist: number }` |
| `getBollingerBands(symbol, interval)` | `{ valueUpperBand, valueMiddleBand, valueLowerBand: number }` |
| `getVwap(symbol, interval)` | `{ value: number }` |
| `getEma(symbol, interval, period?)` | `{ value: number }` |
| `getSma(symbol, interval, period?)` | `{ value: number }` |
| `getOrderbook(symbol, limit?)` | `{ b: [[price, qty], ...], a: [[price, qty], ...] }` — strings |
| `getInstruments(symbol?)` | `{ list: [{ lotSizeFilter, priceFilter, leverageFilter }] }` |
