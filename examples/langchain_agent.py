"""LangChain agent with Eterna MCP trading tools.

Demonstrates the full flow:
1. Connect without authentication
2. Agent registers itself and receives an API key
3. Reconnect with the key
4. Trade using LangChain's ReAct agent

Prerequisites:
    pip install langchain-mcp-adapters langchain-anthropic langgraph

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python langchain_agent.py
"""

import asyncio
import json

from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

MCP_URL = "https://mcp.eterna.exchange/mcp"


async def register_agent() -> str:
    """Connect without auth, call register_agent, return the API key."""
    async with MultiServerMCPClient(
        {
            "trading": {
                "url": MCP_URL,
                "transport": "streamable_http",
            }
        }
    ) as client:
        tools = client.get_tools()
        llm = ChatAnthropic(model="claude-sonnet-4-6")
        agent = create_react_agent(llm, tools)

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Register a new trading agent called my-langchain-bot",
                    }
                ]
            }
        )

        # Extract the API key from the agent's response
        for message in result["messages"]:
            if hasattr(message, "content") and isinstance(message.content, str):
                if "eterna_mcp_" in message.content:
                    # Find the key in the response text
                    for word in message.content.split():
                        if word.startswith("eterna_mcp_"):
                            return word.strip(".,;:\"'`")

        raise RuntimeError("Failed to extract API key from registration response")


async def trade(api_key: str):
    """Connect with the API key and run a trading agent."""
    async with MultiServerMCPClient(
        {
            "trading": {
                "url": MCP_URL,
                "transport": "streamable_http",
                "headers": {"Authorization": f"Bearer {api_key}"},
            }
        }
    ) as client:
        tools = client.get_tools()
        print(f"Loaded {len(tools)} trading tools")

        llm = ChatAnthropic(model="claude-sonnet-4-6")
        agent = create_react_agent(llm, tools)

        result = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Check the current BTC price and my account balance. "
                            "If I have more than 100 USDT available, show me the "
                            "ETH order book and suggest whether to go long or short "
                            "based on the bid/ask imbalance."
                        ),
                    }
                ]
            }
        )

        for message in result["messages"]:
            if hasattr(message, "content") and isinstance(message.content, str):
                print(f"\n{message.type}: {message.content}")


async def main():
    # Step 1: Register (only needed once -- save the key for future runs)
    print("Registering agent...")
    api_key = await register_agent()
    print(f"Received API key: {api_key[:20]}...")

    # Step 2: Trade with the key
    print("\nConnecting with API key...")
    await trade(api_key)


if __name__ == "__main__":
    asyncio.run(main())
