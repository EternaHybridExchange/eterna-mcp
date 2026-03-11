# Fee Comparison

## Trading Fees

Eterna agents trade through Bybit's master/sub-account structure, which qualifies for institutional-tier fee schedules.

| Provider | Maker Fee | Taker Fee | How |
|---|---|---|---|
| **Eterna MCP** | 0.035% | 0.055% | Master account VIP tier, inherited by sub-accounts |
| Self-hosted (Bybit default) | 0.100% | 0.100% | Standard retail tier unless you independently qualify |
| Self-hosted (Bybit VIP 1) | 0.040% | 0.060% | Requires $10M+ monthly volume on your account |
| Binance (default) | 0.020% | 0.050% | Different exchange, different liquidity |

### What this means in practice

For a $10,000 trade:

| | Eterna | Self-hosted (default) | Savings |
|---|---|---|---|
| **Market order (taker)** | $5.50 | $10.00 | $4.50 per trade |
| **Limit order (maker)** | $3.50 | $10.00 | $6.50 per trade |

At 10 trades/day, Eterna saves $45-65/day ($1,350-1,950/month) compared to default Bybit fees.

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
