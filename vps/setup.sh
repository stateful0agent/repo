#!/bin/bash
# One-time VPS setup. Run as root on a fresh Ubuntu machine.
# Usage: ./setup.sh <github-runner-token> <repo-owner/repo-name>
set -e

TOKEN="$1"
REPO="$2"
if [ -z "$TOKEN" ] || [ -z "$REPO" ]; then
  echo "Usage: ./setup.sh <runner-registration-token> <owner/repo>"
  exit 1
fi

apt update && apt install -y git curl jq
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
curl -fsSL https://opencode.ai/install | bash
export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"
echo "export PATH=\"\$HOME/.opencode/bin:\$HOME/.local/bin:\$PATH\"" >> /etc/profile.d/theo.sh

RUNNER_DIR=/opt/actions-runner
mkdir -p "$RUNNER_DIR" && cd "$RUNNER_DIR"
RUNNER_VERSION=$(curl -s https://api.github.com/repos/actions/runner/releases/latest | jq -r .tag_name | sed 's/^v//')
curl -o actions-runner.tar.gz -L "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
tar xzf actions-runner.tar.gz && rm actions-runner.tar.gz
RUNNER_ALLOW_RUNASROOT=1 ./config.sh --url "https://github.com/$REPO" --token "$TOKEN" --unattended --name theo-vps
./svc.sh install
./svc.sh start

git clone "https://github.com/$REPO.git" /opt/theo

echo ""
echo "=== Now create /opt/theo/.env with your secrets ==="
echo "    Open another terminal and run: vim /opt/theo/.env"
echo "    Press ENTER here when done."
read -r

set -a
source /opt/theo/.env
set +a

mkdir -p ~/.local/share/opencode
echo "{\"vercel\":{\"apiKey\":\"$AI_GATEWAY_API_KEY\"}}" > ~/.local/share/opencode/auth.json

cd /opt/theo
bash vps/sync-schedule.sh
uv run scripts/sync_secrets.py "$REPO"
chmod +x wake.sh vps/*.sh

echo ""
echo "Setup complete. Runner is online, schedule installed, secrets synced."
echo "Trigger a test: curl -sf -X POST -H 'Authorization: token $REPO_PAT' -H 'Accept: application/vnd.github+json' https://api.github.com/repos/$REPO/dispatches -d '{\"event_type\":\"wake\"}'"
