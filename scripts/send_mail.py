# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests",
# ]
# ///
"""Send an email using AgentMail API."""

import argparse, os, requests

API = "https://api.agentmail.to/v0"
HDR = {
    "Authorization": f"Bearer {os.environ['AGENTMAIL_API_KEY']}",
    "Content-Type": "application/json",
}


def send(to: str, subject: str, body: str, is_html: bool = False) -> dict:
    payload = {"to": to, "subject": subject}
    if is_html:
        payload["html"] = body
    else:
        payload["text"] = body

    r = requests.post(
        f"{API}/inboxes/{os.environ['AGENTMAIL_INBOX_ID']}/messages/send",
        headers=HDR,
        json=payload,
    )
    r.raise_for_status()
    print(f"Sent: {r.json()['message_id']}")
    return r.json()


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("to")
    p.add_argument("subject")
    p.add_argument("body")
    p.add_argument("--html", action="store_true", help="Send body as HTML")
    a = p.parse_args()
    send(a.to, a.subject, a.body, a.html)
