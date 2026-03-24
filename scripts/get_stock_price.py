# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "yfinance",
# ]
# ///
"""Get current stock price."""

import argparse
import sys
import yfinance as yf


def main():
    parser = argparse.ArgumentParser(description="Get current stock price.")
    parser.add_argument(
        "ticker", type=str, help="Stock ticker symbol (e.g., AAPL, MSFT)"
    )

    args = parser.parse_args()

    ticker_symbol = args.ticker.upper()
    ticker = yf.Ticker(ticker_symbol)

    try:
        data = ticker.fast_info
        if "lastPrice" in data:
            price = data["lastPrice"]
            print(f"{ticker_symbol}: ${price:,.2f}")
        else:
            print(
                f"Error: Could not retrieve price for '{ticker_symbol}'.",
                file=sys.stderr,
            )
            sys.exit(1)

    except Exception as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
