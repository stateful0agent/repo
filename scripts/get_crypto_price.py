# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""Get current cryptocurrency price from CoinGecko."""

import argparse
import sys
import requests


def main():
    parser = argparse.ArgumentParser(description="Get current cryptocurrency price.")
    parser.add_argument(
        "coin", type=str, help="Cryptocurrency ID (e.g., bitcoin, ethereum)"
    )
    parser.add_argument(
        "--currency",
        type=str,
        default="usd",
        help="Fiat currency to convert to (default: usd)",
    )

    args = parser.parse_args()

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={args.coin.lower()}&vs_currencies={args.currency.lower()}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if args.coin.lower() not in data:
            print(
                f"Error: Could not find price for '{args.coin}'. Check if the ID is correct (e.g., 'bitcoin').",
                file=sys.stderr,
            )
            sys.exit(1)

        price = data[args.coin.lower()][args.currency.lower()]
        print(f"{args.coin.capitalize()} ({args.currency.upper()}): ${price:,.2f}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
