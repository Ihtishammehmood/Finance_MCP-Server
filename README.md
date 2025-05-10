# Building a Finance agents wit MCP

## Overview

This project demonstrates the use of a **Model Context Protocol (MCP)** server for retrieving financial data. The MCP server is integrated with **Agno** and **Smol Agent** to showcase its versatility in handling multiple agentic frameworks in standardized way.



1. **MCP Server (Finance):**

   * This server is created using `yfinance` fetch financial information of companies
   * Standardizes interactions with external financial data sources using MCP.
2. **Agentic Framework Integration**

   * Integrated mcp server with Agno and Smol Agent.
   * MCP creates a universal standard for all agentic workflows.


## Features

* MCP enables AI applications to access diverse data sources and tools using a consistent protocol, streamlining the development process.
* AI applications (clients) communicate with MCP servers that expose specific capabilities, such as data access or function execution
* MCP allows AI models to retrieve up-to-date information and perform actions based on real-time data, enhancing their responsiveness and accuracy .

## Getting Started


1. Clone the repository:

```bash
    git clone https://github.com/Ihtishammehmood/Finance_MCP-Server.git
```
2.  Add Groq APi to .env:
```
GROQ_API_KEY = "Place your GROQ API key here"
```

3. Install UV package Manager
```bash
pip install uv
```

4. Create Virtual Environment

```bash
uv venv
```

5. Activate virtual Environment:

```bash
.venv\Scripts\activate

```

6. Install dependencies

```bash
uv pip sync requirements.txt
```

7. Start Agno and Smol Agent integrations:

```bash
    uv run agno_agent.py
    uv run smol_agent.py
```

## Initialize MCP Inspector

* Run `mcp dev server.py` in Terminal
## Add MCP server in IDE
```
{
    "mcpServers": {
      "stockTools": {
        "command": "uv",
        "args": [
          "--directory",
          "Place your absolute path here",
          "run",
          "server.py"
        ]
      }
    }
  }

```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

