# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "psutil",
# ]
# ///
import argparse
import psutil
import json


def get_system_info():
    info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }
    return info


def main():
    parser = argparse.ArgumentParser(description="System Information script")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    info = get_system_info()

    if args.json:
        print(json.dumps(info, indent=2))
    else:
        print(f"CPU Usage: {info['cpu_percent']}%")
        print(f"Memory Usage: {info['memory_percent']}%")
        print(f"Disk Usage: {info['disk_percent']}%")


if __name__ == "__main__":
    main()
