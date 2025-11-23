import requests
from app.utils.logger import get_logger

log = get_logger("MarketDataTool")

def fetch_tcs_stock_price():
    """Optional market context. If fails, returns empty dict."""
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=TCS.NS"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = data["quoteResponse"]["result"][0].get("regularMarketPrice")
        return {"symbol": "TCS.NS", "price_inr": price}
    except Exception as e:
        log.warning(f"Market data fetch failed: {e}")
        return {}
