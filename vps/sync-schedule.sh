#!/bin/bash
# Reads calendar/schedule.txt and installs crontab entries that trigger
# GitHub repository_dispatch at each scheduled time.
# Requires .env to have REPO_PAT and REPO set.
set -e
cd "$(dirname "$0")/.."
source .env

CRON=""
while IFS= read -r line; do
  line=$(echo "$line" | xargs)
  [ -z "$line" ] && continue
  hour="${line%%:*}"
  min="${line##*:}"
  CMD="curl -sf -X POST -H 'Authorization: token $REPO_PAT' -H 'Accept: application/vnd.github+json' https://api.github.com/repos/$REPO/dispatches -d '{\"event_type\":\"wake\"}'"
  CRON+="$min $hour * * * $CMD"$'\n'
done < calendar/schedule.txt

echo "$CRON" | crontab -
echo "Installed crontab:"
crontab -l
