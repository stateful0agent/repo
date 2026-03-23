# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "psutil",
#     "requests",
# ]
# ///
import argparse
import sys
import psutil
import requests
import json


def check_system():
    checks = []

    # CPU
    cpu = psutil.cpu_percent(interval=1)
    cpu_ok = cpu < 90
    checks.append(
        {"name": "CPU Usage", "status": "OK" if cpu_ok else "WARN", "value": f"{cpu}%"}
    )

    # Memory
    mem = psutil.virtual_memory().percent
    mem_ok = mem < 90
    checks.append(
        {
            "name": "Memory Usage",
            "status": "OK" if mem_ok else "WARN",
            "value": f"{mem}%",
        }
    )

    # Disk
    disk = psutil.disk_usage("/").percent
    disk_ok = disk < 90
    checks.append(
        {
            "name": "Disk Usage",
            "status": "OK" if disk_ok else "WARN",
            "value": f"{disk}%",
        }
    )

    # Network
    try:
        requests.get("https://1.1.1.1", timeout=5)
        checks.append({"name": "Network", "status": "OK", "value": "Connected"})
    except requests.RequestException:
        checks.append({"name": "Network", "status": "FAIL", "value": "Disconnected"})

    return checks


def main():
    parser = argparse.ArgumentParser(description="Run system health checks.")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    checks = check_system()
    all_ok = all(c["status"] == "OK" for c in checks)

    if args.json:
        print(json.dumps({"healthy": all_ok, "checks": checks}, indent=2))
    else:
        for c in checks:
            print(f"[{c['status']}] {c['name']}: {c['value']}")
        print("\nOverall Status: " + ("HEALTHY" if all_ok else "UNHEALTHY"))

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
