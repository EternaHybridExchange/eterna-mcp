"""CrewAI trading crew with Eterna MCP tools.

Demonstrates the full flow:
1. Connect without authentication
2. Register and receive an API key via MCP
3. Reconnect with the key
4. Run a multi-agent crew (analyst + risk manager)

Prerequisites:
    pip install crewai crewai-tools[mcp]

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python crewai_trading_crew.py
"""

import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from crewai import Agent, Crew, Task
from crewai_tools.mcp import MCPServerAdapter

MCP_URL = "https://mcp.eterna.exchange/mcp"


async def register_agent() -> str:
    """Connect without auth, call register_agent directly, return the API key."""
    import asyncio

    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "register_agent", {"name": "my-crewai-crew"}
            )
            # Parse the API key from the response
            for content in result.content:
                text = content.text if hasattr(content, "text") else str(content)
                if "eterna_mcp_" in text:
                    for word in text.split():
                        if word.startswith("eterna_mcp_"):
                            return word.strip(".,;:\"'`")
                    # Try parsing as JSON
                    try:
                        data = json.loads(text)
                        if isinstance(data, dict) and "apiKey" in data:
                            return data["apiKey"]
                    except (json.JSONDecodeError, TypeError):
                        pass

    raise RuntimeError("Failed to extract API key from registration response")


def trade(api_key: str):
    """Connect with the API key and run a trading crew."""
    server = MCPServerAdapter(
        server_url=MCP_URL,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    tools = server.tools
    print(f"Loaded {len(tools)} trading tools")

    analyst = Agent(
        role="Market Analyst",
        goal="Analyze market conditions and identify trading opportunities",
        backstory=(
            "You are an experienced crypto market analyst. You study price action, "
            "order book depth, and funding rates to identify high-probability setups."
        ),
        tools=tools,
        verbose=True,
    )

    risk_manager = Agent(
        role="Risk Manager",
        goal="Ensure all trades follow strict risk management rules",
        backstory=(
            "You are a conservative risk manager. You never allow more than 2% "
            "of the account balance on a single trade. You always verify account "
            "state before approving any trade."
        ),
        tools=tools,
        verbose=True,
    )

    analysis_task = Task(
        description=(
            "1. Get the current BTC and ETH tickers\n"
            "2. Check the BTC order book for bid/ask imbalance\n"
            "3. Summarize: current prices, 24h changes, funding rates, "
            "and order book sentiment\n"
            "4. Recommend whether conditions favor long or short positions"
        ),
        expected_output="Market analysis report with trading recommendation",
        agent=analyst,
    )

    risk_task = Task(
        description=(
            "1. Check the current account balance\n"
            "2. Check all open positions\n"
            "3. Based on the market analysis, calculate the maximum position size "
            "that risks no more than 2% of equity\n"
            "4. Approve or reject the trading recommendation with position sizing"
        ),
        expected_output="Risk assessment with approved position size or rejection reason",
        agent=risk_manager,
    )

    crew = Crew(
        agents=[analyst, risk_manager],
        tasks=[analysis_task, risk_task],
        verbose=True,
    )

    result = crew.kickoff()
    print(f"\n{'=' * 60}")
    print("CREW RESULT:")
    print(result)


def main():
    import asyncio

    # Step 1: Register (only needed once -- save the key for future runs)
    print("Registering agent...")
    api_key = asyncio.run(register_agent())
    print(f"Received API key: {api_key[:20]}...")

    # Step 2: Trade with the key
    print("\nConnecting with API key...")
    trade(api_key)


if __name__ == "__main__":
    main()
