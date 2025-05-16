import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("finance_server")

mcp = FastMCP("finance-server")

FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"


async def make_request(url: str) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch income statements or no income statements found."

    income_statements = data.get("income_statements", [])

    if not income_statements:
        return "Unable to fetch income statements or no income statements found."

    return json.dumps(income_statements, indent=2)


@mcp.tool()
async def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get balance sheets for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the balance sheet (e.g. annual, quarterly, ttm)
        limit: Number of balance sheets to return (default: 4)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch balance sheets or no balance sheets found."

    balance_sheets = data.get("balance_sheets", [])

    if not balance_sheets:
        return "Unable to fetch balance sheets or no balance sheets found."

    return json.dumps(balance_sheets, indent=2)


@mcp.tool()
async def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get cash flow statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
        limit: Number of cash flow statements to return (default: 4)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    cash_flow_statements = data.get("cash_flow_statements", [])

    if not cash_flow_statements:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    return json.dumps(cash_flow_statements, indent=2)


@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch current price or no current price found."

    snapshot = data.get("snapshot", {})

    if not snapshot:
        return "Unable to fetch current price or no current price found."

    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch prices or no prices found."

    prices = data.get("prices", [])

    if not prices:
        return "Unable to fetch prices or no prices found."

    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch news or no news found."

    news = data.get("news", [])

    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)


@mcp.tool()
async def get_available_crypto_tickers() -> str:
    """
    Gets all available crypto tickers.
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
    data = await make_request(url)

    if not data:
        return "Unable to fetch available crypto tickers or no available crypto tickers found."

    tickers = data.get("tickers", [])

    return json.dumps(tickers, indent=2)


@mcp.tool()
async def get_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """
    Gets historical prices for a crypto currency.
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch prices or no prices found."

    prices = data.get("prices", [])

    if not prices:
        return "Unable to fetch prices or no prices found."

    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_historical_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical prices for a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch prices or no prices found."

    prices = data.get("prices", [])

    if not prices:
        return "Unable to fetch prices or no prices found."

    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_current_crypto_price(ticker: str) -> str:
    """Get the current / latest price of a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
    """
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    if not data:
        return "Unable to fetch current price or no current price found."

    snapshot = data.get("snapshot", {})

    if not snapshot:
        return "Unable to fetch current price or no current price found."

    return json.dumps(snapshot, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
