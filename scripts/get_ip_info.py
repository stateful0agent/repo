# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
import argparse
import sys
import requests


def get_ip_info(ip_address=""):
    url = (
        f"http://ip-api.com/json/{ip_address}"
        if ip_address
        else "http://ip-api.com/json/"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "fail":
            print(f"Error: {data.get('message')}")
            sys.exit(1)

        print(f"IP: {data.get('query')}")
        print(f"City: {data.get('city')}")
        print(f"Region: {data.get('regionName')}")
        print(f"Country: {data.get('country')}")
        print(f"ISP: {data.get('isp')}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Get information about an IP address.")
    parser.add_argument(
        "ip",
        nargs="?",
        default="",
        help="IP address to lookup (default: your public IP)",
    )
    args = parser.parse_args()

    get_ip_info(args.ip)


if __name__ == "__main__":
    main()
