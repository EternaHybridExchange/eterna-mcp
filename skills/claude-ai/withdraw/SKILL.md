---
name: withdraw
description: Withdraw crypto from Eterna to an external wallet
---

# Withdraw Skill

Guide the user through withdrawing funds from Eterna.

## Step 1 — Check withdrawable amount

Use `search_examples` with query `"withdrawable amount balance"` to get the code pattern. Run via `execute_code`.

If the user has open positions, available balance will be less than total equity. Explain this if it surprises them.

## Step 2 — Get chain options

Use `search_examples` with query `"withdrawal chains coin info"` to get the pattern. Run via `execute_code`.

Recommend Arbitrum for low fees unless the user specifies a chain.

## Step 3 — Submit withdrawal

**Always confirm address and amount with the user before submitting.** Double-check the chain matches their destination wallet.

Use `search_examples` with query `"submit withdrawal"` to get the pattern. Replace coin, amount, address, and chain based on user input, then run via `execute_code`.

## Step 4 — Check status

Use `search_sdk` with `methods: ["getWithdrawalStatus"]` and `detail_level: "full"` to check the method signature. Run via `execute_code`:

```typescript
const status = await eterna.getWithdrawalStatus();
return status;
```

## SDK reference

| Method | Purpose |
|--------|---------|
| `getWithdrawableAmount(coin)` | Check how much can be withdrawn |
| `getCoinInfo(coin)` | Get available chains for withdrawal |
| `submitWithdrawal(coin, amount, address, chain)` | Submit the withdrawal request |
| `getWithdrawalStatus(id?)` | Check withdrawal processing status |
