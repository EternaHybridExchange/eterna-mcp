# Deposit — Detailed Guide

## Critical warnings

- Deposits arrive in the **Funding wallet**, NOT the trading wallet.
- After deposit confirms, you **MUST** transfer to trading wallet before funds are usable.
- `getBalance()` checks the **trading wallet** — it shows zero until you transfer. **Do NOT use it to check if a deposit arrived.**
- Use deposit records to monitor incoming deposits.
- Recommend **Arbitrum** for USDT deposits — cheapest and fastest.

## Full flow

### Step 1 — Show deposit options
Use `search_examples` with query `"allowed deposit chains USDT"`. Present as a simple choice: "I'd recommend **Arbitrum** — fast and cheap. Which chain works for your wallet?"

For other coins (BTC, ETH, USDC), use `search_sdk` with `query: "getAllowedDepositCoins"` and `detail_level: "full"`.

### Step 2 — Get deposit address
Use `search_examples` with query `"deposit address Arbitrum USDT"`. Replace coin/chain per user's choice.

Show address clearly. **If there's a tag/memo, emphasize it** — missing tags can lose funds.

### Step 3 — Monitor deposit
Use `search_examples` with query `"monitor deposit status pending confirmed"`.

**Status codes:**
- 0 = unknown
- 1 = waiting for confirmations — "I can see it, waiting for blockchain confirmations."
- 2 = processing — "Almost there, Eterna is processing it."
- **3 = success** — proceed to transfer immediately.
- 4 = failed — "Something went wrong. Check the tx on a block explorer."

### Step 4 — Transfer to trading wallet
**Mandatory.** Funds sit in the Funding wallet until transferred.

- USDT: `search_examples` with query `"transfer to trading wallet"` — use `transferToTrading("USDT", "ALL_BALANCE")`
- Non-USDT: `search_examples` with query `"swap to USDT transfer trading wallet"` — swap first, then transfer

### Step 5 — Confirm balance
Use `search_examples` with query `"check account balance equity"`.

Celebrate: "You're funded! $X ready to trade." Then suggest trade ideas.

## SDK quick reference

| Method | Purpose |
|--------|---------|
| `getAllowedDepositCoins(coin?, chain?)` | Available deposit chains and minimums |
| `getDepositAddress(coin, chainType)` | Get deposit address for a chain |
| `getDepositRecords(coin?)` | Check deposit status (status 0-4) |
| `transferToTrading(coin, amount)` | Move Funding → Trading wallet. Use `"ALL_BALANCE"` for full transfer |
| `swapToUsdt(coin, amount?)` | Swap a coin to USDT. Omit amount for full balance |
| `getBalance()` | **Trading wallet only** |
