# Architecture

This document is archived.

The current Eterna AI MCP architecture is code-execution-first:

1. MCP client authenticates through OAuth in supported clients.
2. Agent uses `search_sdk` and `search_examples` to discover methods and workflows.
3. Agent calls `execute_code` with TypeScript/JavaScript.
4. Code runs in a managed sandbox with the injected `eterna.*` SDK.
5. The sandbox dispatches SDK calls through Eterna services.

Use the canonical docs in `eterna-ai`:

- https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/mcp.md
- https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/sdk.md
- https://github.com/EternaHybridExchange/eterna-ai/blob/main/docs/consolidation/sandbox-sdk-catalog.md
