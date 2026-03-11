"""Basic trading example using the Eterna MCP Gateway.

Demonstrates the full flow:
1. Connect without authentication
2. Call register_agent to get an API key
3. Reconnect with the key
4. Fetch market data and check balance

Prerequisites:
    pip install mcp

Usage:
    python basic-trading.py
"""

import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_URL = "https://mcp.eterna.exchange/mcp"


async def main():
    # Step 1: Connect without auth and register
    print("Connecting to register...")
    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # The agent registers itself -- no pre-existing API key needed
            result = await session.call_tool(
                "register_agent", {"name": "my-python-bot"}
            )
            print(f"Registration response: {result.content}")

            # Extract the API key from the response
            api_key = None
            for content in result.content:
                text = content.text if hasattr(content, "text") else str(content)
                try:
                    data = json.loads(text)
                    if isinstance(data, dict) and "apiKey" in data:
                        api_key = data["apiKey"]
                        break
                except (json.JSONDecodeError, TypeError):
                    if "eterna_mcp_" in text:
                        for word in text.split():
                            if word.startswith("eterna_mcp_"):
                                api_key = word.strip(".,;:\"'`")
                                break

    if not api_key:
        print("Failed to get API key from registration")
        return

    print(f"Received API key: {api_key[:20]}...")

    # Step 2: Reconnect with the API key and trade
    print("\nConnecting with API key...")
    headers = {"Authorization": f"Bearer {api_key}"}
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
