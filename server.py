
from mcp.server.fastmcp import FastMCP
import yfinance as yf



# Create an MCP server with a custom name
mcp = FastMCP("Stock Financial Decision Server")

@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """
    Retrieve the current stock price for the given ticker symbol.
    Returns a formatted string with the latest closing price and currency.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        info = ticker.info
        currency = info.get("currency", "USD")
        if not data.empty:
            price = data['Close'].iloc[-1]
            return f"Current price of {symbol}: {price:.2f} {currency}"
        else:
            price = info.get("regularMarketPrice", None)
            if price is not None:
                return f"Current price of {symbol}: {price:.2f} {currency}"
            else:
                return f"Price data not available for {symbol}."
    except Exception as e:
        return f"Error retrieving price for {symbol}: {str(e)}"

@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo", max_rows: int = 10) -> str:
    """
    Retrieve historical data for a stock given a ticker symbol and a period.
    Returns the last `max_rows` as a markdown table.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty:
            return f"No historical data found for {symbol} with period '{period}'."
        data = data.tail(max_rows)
        md = data.to_markdown()
        return f"**Historical Prices for {symbol} ({period}, last {max_rows} rows):**\n\n{md}"
    except Exception as e:
        return f"Error fetching historical data: {str(e)}"

@mcp.tool()
def get_financial_statement(symbol: str, statement_type: str = "income") -> str:
    """
    Retrieve a financial statement for the given ticker symbol.
    statement_type: "income", "balance", or "cashflow"
    Returns the latest statement as a markdown table.
    """
    try:
        ticker = yf.Ticker(symbol)
        if statement_type == "income":
            df = ticker.income_stmt
            label = "Income Statement"
        elif statement_type == "balance":
            df = ticker.balance_sheet
            label = "Balance Sheet"
        elif statement_type == "cashflow":
            df = ticker.cashflow
            label = "Cashflow Statement"
        else:
            return f"Invalid statement_type: {statement_type}. Use 'income', 'balance', or 'cashflow'."
        if df.empty:
            return f"No {label.lower()} data found for {symbol}."
        latest = df.iloc[:, 0:1]
        md = latest.to_markdown()
        return f"**{label} for {symbol} (most recent):**\n\n{md}"
    except Exception as e:
        return f"Error fetching {statement_type} statement: {str(e)}"

@mcp.tool()
def get_analyst_recommendations(symbol: str) -> str:
    """
    Retrieve analyst recommendations for the given ticker symbol.
    Returns a summary of the latest analyst recommendations as a markdown table.
    """
    try:
        ticker = yf.Ticker(symbol)
        recs = ticker.recommendations
        if recs is None or recs.empty:
            return f"No analyst recommendations found for {symbol}."
        latest = recs.tail(5)
        md = latest.to_markdown()
        return f"**Latest Analyst Recommendations for {symbol}:**\n\n{md}"
    except Exception as e:
        return f"Error fetching analyst recommendations: {str(e)}"


@mcp.tool()
def get_company_info(symbol: str) -> str:
    """
    Retrieve detailed company information for the given ticker symbol.
    Returns a formatted string with company name, sector, industry, CEO, website, and summary.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        name = info.get("longName", "N/A")
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")
        ceo = info.get("companyOfficers", [{}])[0].get("name", "N/A") if info.get("companyOfficers") else "N/A"
        website = info.get("website", "N/A")
        summary = info.get("longBusinessSummary", "N/A")
        return (
            f"**Company Information for {symbol}:**\n"
            f"- Name: {name}\n"
            f"- Sector: {sector}\n"
            f"- Industry: {industry}\n"
            f"- CEO: {ceo}\n"
            f"- Website: {website}\n"
            f"- Summary: {summary}"
        )
    except Exception as e:
        return f"Error fetching company info: {str(e)}"


@mcp.tool()
def get_company_news(symbol: str, limit: int = 5) -> str:
    """
    Retrieve recent news articles for the given ticker symbol.
    Returns a formatted string with news headlines and links.
    """
    try:
        ticker = yf.Ticker(symbol)
        news = ticker.news
        if not news:
            return f"No news found for {symbol}."
        lines = []
        for item in news[:limit]:
            title = item.get("title", "No Title")
            link = item.get("link", "")
            publisher = item.get("publisher", "")
            lines.append(f"- **{title}** ({publisher})\n  {link}")
        return f"**Recent News for {symbol}:**\n" + "\n".join(lines)
    except Exception as e:
        return f"Error fetching news: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

# mcp dev server.py