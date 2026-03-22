"""Check Vercel AI Gateway credit balance."""

import argparse, os, requests

if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    r = requests.get(
        "https://ai-gateway.vercel.sh/v1/credits",
        headers={"Authorization": f"Bearer {os.environ['AI_GATEWAY_API_KEY']}"},
    )
    r.raise_for_status()
    c = r.json()
    print(f"Balance: ${c['balance']} | Used: ${c['total_used']}")
