import asyncio
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.mcp import MCPTools
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_finance_agent(session):
    """Create and configure a finance agent with MCP tools."""
    # Initialize the MCP toolkit
    mcp_tools = MCPTools(session=session)
    await mcp_tools.initialize()

    # Create an agent with the MCP toolkit
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[mcp_tools],
        instructions=[
            'As a financial analyst, only respond to financial questions',
            'Highlight key metrics and Actionable Insights',
            'Do not respond to non-financial questions'
        ],
        markdown=True,
        show_tool_calls=True,
    )


async def run_agent(message: str) -> None:
    """Run the finance agent with the given message."""
    # Initialize the MCP server
    server_params = StdioServerParameters(
           command="uv",
           args=["run", "server.py"],
           env=None
           )

    # Create a client session to connect to the MCP server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            agent = await create_finance_agent(session)

            # Run the agent
            await agent.aprint_response(message, stream=True)


if __name__ == "__main__":
    asyncio.run(run_agent("What is the current stock price of IBM?"))