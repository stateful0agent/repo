# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
# ]
# ///

import argparse
import requests
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Get latest exchange rates and convert currencies."
    )
    parser.add_argument("amount", type=float, help="Amount to convert")
    parser.add_argument("base", type=str, help="Base currency (e.g., USD)")
    parser.add_argument("target", type=str, help="Target currency (e.g., EUR)")

    args = parser.parse_args()

    base = args.base.upper()
    target = args.target.upper()

    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            print(f"Error fetching data: {data.get('error-type', 'Unknown error')}")
            sys.exit(1)

        rates = data.get("rates", {})
        if target not in rates:
            print(f"Error: Target currency {target} not found.")
            sys.exit(1)

        rate = rates[target]
        converted = args.amount * rate
        print(f"{args.amount} {base} = {converted:.2f} {target} (Rate: {rate})")

    except requests.RequestException as e:
        print(f"Failed to fetch exchange rates: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
