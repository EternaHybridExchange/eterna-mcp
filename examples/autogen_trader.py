"""AutoGen agent with Eterna MCP trading tools.

Demonstrates the full flow:
1. Connect without authentication
2. Agent registers itself and receives an API key
3. Reconnect with the key
4. Trade using AutoGen's AssistantAgent

Prerequisites:
    pip install autogen-agentchat autogen-ext[mcp]

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python autogen_trader.py
"""

import asyncio
import json

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StreamableHttpParams

MCP_URL = "https://mcp.eterna.exchange/mcp"


async def register_agent() -> str:
    """Connect without auth, call register_agent, return the API key."""
    server_params = StreamableHttpParams(url=MCP_URL)

    async with McpWorkbench(server_params) as workbench:
        tools = await workbench.list_tools()

        agent = AssistantAgent(
            name="registrar",
            model_client=AnthropicChatCompletionClient(model="claude-sonnet-4-6"),
            tools=tools,
            system_message="Register a new trading agent and return the API key.",
        )

        result = await agent.run(task="Register a new agent called my-autogen-bot")

        # Extract API key from the result
        for message in result.messages:
            text = str(message.content) if hasattr(message, "content") else str(message)
            if "eterna_mcp_" in text:
                for word in text.split():
                    if word.startswith("eterna_mcp_"):
                        return word.strip(".,;:\"'`")

        raise RuntimeError("Failed to extract API key from registration response")


async def trade(api_key: str):
    """Connect with the API key and run a trading agent."""
    server_params = StreamableHttpParams(
        url=MCP_URL,
        headers={"Authorization": f"Bearer {api_key}"},
    )

    async with McpWorkbench(server_params) as workbench:
        tools = await workbench.list_tools()
        print(f"Loaded {len(tools)} trading tools")

        agent = AssistantAgent(
            name="trader",
            model_client=AnthropicChatCompletionClient(model="claude-sonnet-4-6"),
            tools=tools,
            system_message=(
                "You are a trading assistant with access to Bybit perpetual futures "
                "via the Eterna MCP Gateway. Always check your balance before trading. "
                "Never risk more than 2% of your account on a single trade. "
                "Use limit orders when possible to save on fees."
            ),
        )

        await Console(
            agent.run_stream(
                task=(
                    "Check my balance and current positions. "
                    "Then get the BTC and ETH tickers and summarize "
                    "the market conditions."
                )
            )
        )


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
