from smolagents import ToolCallingAgent, ToolCollection, LiteLLMModel
from mcp import StdioServerParameters
import os
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

api_key = os.getenv("GROQ_API_KEY")

# Specify  LLM via LiteLLM
model = LiteLLMModel(
        model_id="groq/llama-3.3-70b-versatile",
        api_key=api_key)

server_parameters = StdioServerParameters(
    command="uv",
    args=["run", "server.py"],
    env=None,
)

with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
    agent = ToolCallingAgent(tools=[*tool_collection.tools], model=model)
    agent.run("What is the historical price of ibm for 1month?")