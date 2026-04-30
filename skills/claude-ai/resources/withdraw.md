# Withdraw — Detailed Guide

## Full flow

### Step 1 — Check withdrawable amount
Use `search_examples` with query `"withdrawable amount balance"`.

If user has open positions, available balance will be less than total equity. Explain this.

### Step 2 — Get chain options
Use `search_examples` with query `"withdrawal chains coin info"`.

Recommend **Arbitrum** for low fees unless user specifies a chain.

### Step 3 — Submit withdrawal
**Always confirm address and amount with the user before submitting.** Double-check the chain matches their destination wallet.

Use `search_examples` with query `"submit withdrawal"`. Replace coin, amount, address, and chain.

### Step 4 — Check status
Use `search_sdk` with `methods: ["getWithdrawalStatus"]` and `detail_level: "full"`, then run via `execute_code`.

## SDK quick reference

| Method | Purpose |
|--------|---------|
| `getWithdrawableAmount(coin)` | Available to withdraw (equity minus margin) |
| `getCoinInfo(coin)` | Chains with withdrawals enabled |
| `submitWithdrawal(coin, amount, address, chain)` | Submit withdrawal request |
| `getWithdrawalStatus(id?)` | Check processing status |
