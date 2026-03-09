"""Basic trading example using the Eterna MCP Gateway."""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_URL = "https://mcp.eterna.exchange/mcp"
API_KEY = "eterna_mcp_your_key_here"


async def main():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    async with streamablehttp_client(MCP_URL, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Get BTC ticker
            result = await session.call_tool("get_tickers", {"symbol": "BTCUSDT"})
            print(f"BTC ticker: {result.content}")

            # Check balance
            balance = await session.call_tool("get_balance", {})
            print(f"Balance: {balance.content}")


if __name__ == "__main__":
    asyncio.run(main())
