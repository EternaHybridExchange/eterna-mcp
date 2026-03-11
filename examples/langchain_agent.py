"""LangChain agent with Eterna MCP trading tools.

Uses langchain-mcp-adapters to connect LangChain to the Eterna MCP Gateway,
giving any LangChain agent access to perpetual futures trading.

Prerequisites:
    pip install langchain-mcp-adapters langchain-anthropic langgraph

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    export ETERNA_API_KEY=eterna_mcp_your_key_here
    python langchain_agent.py
"""

import asyncio
import os

from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


async def main():
    eterna_key = os.environ["ETERNA_API_KEY"]

    async with MultiServerMCPClient(
        {
            "trading": {
                "url": "https://mcp.eterna.exchange/mcp",
                "transport": "streamable_http",
                "headers": {"Authorization": f"Bearer {eterna_key}"},
            }
        }
    ) as client:
        # Get all trading tools from the MCP server
        tools = client.get_tools()
        print(f"Loaded {len(tools)} trading tools")

        # Create a ReAct agent with Claude
        llm = ChatAnthropic(model="claude-sonnet-4-6")
        agent = create_react_agent(llm, tools)

        # Run the agent
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

        # Print the agent's response
        for message in result["messages"]:
            if hasattr(message, "content") and isinstance(message.content, str):
                print(f"\n{message.type}: {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
