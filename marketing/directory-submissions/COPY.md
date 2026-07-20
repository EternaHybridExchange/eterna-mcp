# Eterna MCP — directory copy pack (SEO + AEO)

Canonical product URL: https://ai.eterna.exchange  
MCP endpoint: https://mcp.eterna.exchange/mcp  
Docs / GitHub: https://github.com/EternaHybridExchange/eterna-mcp  
Privacy: https://eterna.exchange/privacy  
Terms: https://eterna.exchange/terms  
Pricing framing: No KYC. Free to connect; trading fees 0.014% maker / 0.035% taker on futures.

**AEO rule:** each variant answers a distinct question agents/search cite ("best MCP for crypto trading", "no KYC AI trading", "Bybit MCP alternative"). Do not paste identical long descriptions across directories.

---

## Shared facts (cite consistently)

- Managed remote MCP (Streamable HTTP), not a local stdio toy
- 3 MCP tools (`execute_code`, `search_sdk`, `search_examples`) + 29 SDK methods in Deno sandbox
- No KYC; dedicated sub-account per agent
- $10B+ liquidity; &lt;200ms latency claim; 500+ crypto pairs
- Works with Claude, Cursor, LangChain, and any MCP client

Primary entities for AI citation: **Eterna MCP**, **Model Context Protocol**, **AI agent trading**, **perpetual futures**, **no KYC**.

---

## Tier: Agent / MCP registries

**Tagline:** MCP-native crypto exchange for AI agents.

**Short (≤60 chars):** No-KYC trading MCP with sandboxed TypeScript SDK.

**Long (~150 words):**
Eterna MCP is an MCP-native crypto exchange that lets AI agents trade perpetual futures without KYC or self-hosted infrastructure. Agents connect over Streamable HTTP to `https://mcp.eterna.exchange/mcp`, then run TypeScript in a Deno sandbox with 29 `eterna.*` SDK methods — market data, technical analysis, orders, balances, and funding — so one `execute_code` call replaces dozens of brittle tool round-trips.

MCP capabilities:
- `execute_code` — sandboxed TypeScript with the full trading SDK
- `search_sdk` — discover methods at list/summary/full detail levels
- `search_examples` — curated code examples for common strategies

Authentication: OAuth (ai-auth) or agent API key. Isolation: dedicated sub-account per agent. Fees: 0.014% maker / 0.035% taker on futures.

Docs: https://github.com/EternaHybridExchange/eterna-mcp · Product: https://ai.eterna.exchange

**Tags:** MCP, MCP server, AI agent, crypto trading, perpetual futures, no KYC, Claude, Cursor, Model Context Protocol, Bybit liquidity

---

## Tier: AI directories

**Tagline:** AI-powered trading exchange for autonomous agents.

**Short:** Give any AI agent real futures trading via MCP.

**Long:**
Eterna is an AI-powered exchange built so agents — not humans — can trade. Instead of wrapping every exchange endpoint as a separate tool, Eterna exposes a code-execution MCP: the agent writes TypeScript, Eterna runs it in a sandboxed Deno runtime with 29 SDK methods. That cuts token usage by ~90% versus classic MCP tool sprawl.

What makes it AI-first:
- Agent self-onboarding over MCP (no retail KYC flow)
- Isolated sub-accounts and risk boundaries per agent
- Built-in SDK search + examples so models stop hallucinating methods
- Works in Claude, Cursor, LangChain, and Openclaw

Use cases: autonomous market making research, signal execution, portfolio rebalancing bots, agentic treasury ops.

Start at https://ai.eterna.exchange — connect `https://mcp.eterna.exchange/mcp`.

**Tags:** AI trading, AI agents, MCP, crypto AI, autonomous trading, no KYC, futures, agent tools

---

## Tier: Dev tool directories

**Tagline:** Managed Streamable HTTP MCP for perpetual futures.

**Short:** Remote MCP trading server with Deno sandbox + 29 SDK methods.

**Long:**
Eterna MCP is a managed Streamable HTTP MCP server for perpetual futures trading. Remote clients authenticate with Bearer tokens, call three high-level tools, and execute TypeScript against a versioned SDK (`getTickers`, `placeOrder`, `getPositions`, TA indicators, deposits/withdrawals, and more).

Differentiators vs DIY Bybit MCP wrappers: hosted gateway, sub-account provisioning, hashed API keys, rate limits, Langfuse observability hooks, and production K8s deployment. Namespace: `io.github.EternaHybridExchange/eterna-mcp`.

Quickstart: https://github.com/EternaHybridExchange/eterna-mcp/blob/main/QUICKSTART.md

**Tags:** MCP server, Streamable HTTP, TypeScript, Deno, Bybit, trading API, developer tools

---

## Tier: Startup / launch directories

**Tagline:** The exchange built for AI agents. No KYC.

**Short:** Connect an AI agent to real crypto trading in 30 seconds.

**Long:**
Eterna is the easiest way to give an AI agent real trading capabilities. Add one MCP URL, authenticate, and your agent can read markets, run indicators, and place futures orders — without KYC and without operating exchange infrastructure.

Unlike self-hosted MCP servers or raw exchange API wrappers, Eterna provisions an isolated sub-account per agent, keeps credentials off the model context, and ships a sandboxed code-execution runtime so agents spend tokens on strategy, not tool glue.

Built for teams shipping agentic trading products, quant researchers prototyping with Claude/Cursor, and platforms that need white-label agent trading rails.

Try it free to connect at https://ai.eterna.exchange.

**Tags:** AI agents, crypto exchange, no KYC, MCP, fintech, autonomous agents, startup

---

## Tier: SaaS / alternatives framing

**Tagline:** The no-KYC, agent-native alternative to DIY exchange MCP wrappers.

**Short:** Managed trading MCP — alternative to self-hosted Bybit tools.

**Long:**
Eterna MCP is a managed alternative to self-hosted Bybit/Binance MCP wrappers and brittle “one-tool-per-endpoint” servers. Built for teams who need agents to trade without standing up gateways, key rotation, or KYC retail flows.

Where DIY wrappers share one API key across agents and explode context with 40+ tools, Eterna gives each agent an isolated sub-account and collapses trading into sandboxed `execute_code` plus SDK search.

Key features:
- Streamable HTTP MCP at mcp.eterna.exchange
- 29 SDK methods (market, TA, trading, account, funding)
- No KYC onboarding for agents
- Institutional-style futures fees (0.014% / 0.035%)
- Docs, skills, and Openclaw plugin

Start at https://ai.eterna.exchange.

**Tags:** Bybit MCP alternative, trading MCP, AI exchange, no KYC, agent infrastructure

---

## One-line FAQ answers (AEO)

1. **What is Eterna MCP?** A managed Model Context Protocol server that lets AI agents trade crypto perpetual futures with no KYC.
2. **How do I connect?** Add `https://mcp.eterna.exchange/mcp` as a Streamable HTTP MCP server, then authenticate with OAuth or an agent API key.
3. **Is KYC required?** No. Eterna is designed for agent onboarding without retail KYC.
4. **What can agents do?** Market data, technical indicators, place/cancel orders, manage positions, and handle deposits/withdrawals via 29 SDK methods.
5. **Who is it for?** AI agent builders, quant researchers, and platforms needing white-label agent trading.
