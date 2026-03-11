# Fee Comparison

## Trading Fees

Eterna agents trade through Bybit's master/sub-account structure, which qualifies for institutional-tier fee schedules.

### Futures (USDT Perpetuals)

| Provider | Maker Fee | Taker Fee | How |
|---|---|---|---|
| **Eterna MCP** | 0.014% | 0.035% | Master account VIP tier, inherited by sub-accounts |
| Self-hosted (Bybit default) | 0.020% | 0.055% | Standard retail tier unless you independently qualify |
| Self-hosted (Bybit VIP 1) | 0.016% | 0.042% | Requires $10M+ monthly volume on your account |

### Spot

| Provider | Maker Fee | Taker Fee | How |
|---|---|---|---|
| **Eterna MCP** | 0.065% | 0.0775% | Master account VIP tier, inherited by sub-accounts |
| Self-hosted (Bybit default) | 0.100% | 0.100% | Standard retail tier unless you independently qualify |
| Self-hosted (Bybit VIP 1) | 0.060% | 0.080% | Requires $10M+ monthly volume on your account |

### What this means in practice

For a $10,000 futures trade:

| | Eterna | Self-hosted (default) | Savings |
|---|---|---|---|
| **Market order (taker)** | $3.50 | $5.50 | $2.00 per trade |
| **Limit order (maker)** | $1.40 | $2.00 | $0.60 per trade |

At 10 futures trades/day, Eterna saves $6-20/day ($180-600/month) compared to default Bybit fees.

## Infrastructure Costs

| | Eterna MCP | Self-hosted MCP |
|---|---|---|
| **Server** | $0 (hosted) | $5-50/mo (VPS/cloud) |
| **Maintenance** | $0 | Your time |
| **API key rotation** | Automatic | Manual |
| **Bybit API updates** | We handle it | You update & redeploy |
| **Monitoring** | Built-in | You build it |

## No Hidden Fees

Eterna does not charge a platform fee, subscription, or per-trade surcharge. The only fees are Bybit's standard trading fees at the master account's VIP tier, passed through directly to your sub-account.
