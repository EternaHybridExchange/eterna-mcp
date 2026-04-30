---
name: deposit
description: Guide user through depositing crypto and transferring funds to the trading wallet
---

# Deposit Skill

Guide the user through depositing funds into their Eterna trading account.

**Critical flow:** Deposit address -> send crypto -> monitor with deposit records -> transfer to trading wallet -> confirm balance.

## Important context

- Deposits arrive in the **Funding wallet**, NOT the trading wallet.
- After deposit confirms, you MUST transfer to trading wallet before funds are usable.
- `getBalance()` checks the **trading wallet** — it will show zero until you transfer. **Do NOT use `getBalance()` to check if a deposit has arrived.**
- Use deposit records to monitor incoming deposits.
- Recommend **Arbitrum** for USDT deposits — cheapest and fastest.

## Step 1 — Show deposit options

Use `search_examples` with query `"allowed deposit chains USDT"` to get the code pattern. Run via `execute_code`.

Present as a simple choice: "I'd recommend **Arbitrum** — fast and cheap. Which chain works for your wallet?"

If the user wants a different coin (BTC, ETH, USDC), use `search_sdk` with `query: "getAllowedDepositCoins"` and `detail_level: "full"` to check the method signature, then adapt the code.

## Step 2 — Get deposit address

Use `search_examples` with query `"deposit address Arbitrum USDT"` to get the code pattern. Replace coin/chain based on user's choice and run via `execute_code`.

Show address clearly. If there's a tag/memo, emphasize it — missing tags can lose funds.

## Step 3 — Monitor deposit

Once the user says they've sent funds, use `search_examples` with query `"monitor deposit status pending confirmed"` to get the monitoring pattern. Run via `execute_code`.

**Status codes:**
- 0 = unknown
- 1 = waiting for confirmations — tell user: "I can see it, waiting for blockchain confirmations."
- 2 = processing — "Almost there, Eterna is processing it."
- **3 = success** — proceed to Step 4 immediately.
- 4 = failed — "Something went wrong. Check the tx on a block explorer."

Check when the user asks. If they ask you to poll, check every minute.

## Step 4 — Transfer to trading wallet

**This step is mandatory.** Funds sit in the Funding wallet until transferred.

If they deposited USDT, use `search_examples` with query `"transfer to trading wallet"` — run the `transferToTrading("USDT", "ALL_BALANCE")` pattern via `execute_code`.

If they deposited a non-USDT coin, use `search_examples` with query `"swap to USDT transfer trading wallet"` to get the swap+transfer pattern. Run via `execute_code`.

## Step 5 — Confirm balance is ready

Use `search_examples` with query `"check account balance equity"` to get the balance check pattern. Run via `execute_code`.

Celebrate: "You're funded! $X ready to trade." Then suggest looking at trade ideas.

## SDK reference

Use `search_sdk` with `query: "deposit"` and `detail_level: "summary"` to discover all deposit-related methods if needed.

| Method | Purpose |
|--------|---------|
| `getAllowedDepositCoins(coin?, chain?)` | Available deposit chains and minimums |
| `getDepositAddress(coin, chainType)` | Get deposit address for a specific chain |
| `getDepositRecords(coin?)` | Check deposit status (status 0-4) |
| `transferToTrading(coin, amount)` | Move funds from Funding to Trading wallet — use `"ALL_BALANCE"` for full transfer |
| `swapToUsdt(coin, amount?)` | Swap a coin to USDT — omit amount for full balance |
| `getBalance()` | Check **trading wallet** balance |
