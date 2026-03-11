"""AutoGen agent with Eterna MCP trading tools.

Uses AutoGen's MCP integration to give agents access to perpetual futures
trading via the Eterna MCP Gateway.

Prerequisites:
    pip install autogen-agentchat autogen-ext[mcp]

Usage:
    export ETERNA_API_KEY=eterna_mcp_your_key_here
    python autogen_trader.py
"""

import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench, StreamableHttpParams


async def main():
    eterna_key = os.environ["ETERNA_API_KEY"]

    server_params = StreamableHttpParams(
        url="https://mcp.eterna.exchange/mcp",
        headers={"Authorization": f"Bearer {eterna_key}"},
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

        # Run a trading task
        await Console(
            agent.run_stream(
                task=(
                    "Check my balance and current positions. "
                    "Then get the BTC and ETH tickers and summarize "
                    "the market conditions."
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
