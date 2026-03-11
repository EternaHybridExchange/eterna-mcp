"""CrewAI trading crew with Eterna MCP tools.

Creates a crew of specialized trading agents that collaborate using
the Eterna MCP Gateway for market analysis and trade execution.

Prerequisites:
    pip install crewai crewai-tools[mcp]

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    export ETERNA_API_KEY=eterna_mcp_your_key_here
    python crewai_trading_crew.py
"""

import os

from crewai import Agent, Crew, Task
from crewai_tools.mcp import MCPServerAdapter


def main():
    eterna_key = os.environ["ETERNA_API_KEY"]

    # Connect to Eterna MCP Gateway
    server = MCPServerAdapter(
        server_url="https://mcp.eterna.exchange/mcp",
        headers={"Authorization": f"Bearer {eterna_key}"},
    )
    tools = server.tools
    print(f"Loaded {len(tools)} trading tools")

    # Define specialized agents
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

    # Define tasks
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

    # Run the crew
    crew = Crew(
        agents=[analyst, risk_manager],
        tasks=[analysis_task, risk_task],
        verbose=True,
    )

    result = crew.kickoff()
    print(f"\n{'=' * 60}")
    print("CREW RESULT:")
    print(result)


if __name__ == "__main__":
    main()
