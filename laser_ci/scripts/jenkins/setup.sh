#!/usr/bin/env bash
# setup.sh — Start Laser CI services.
#
# Prerequisites:
#   1. Copy keys.env.example to keys.env and fill in your values.
#   2. Run this script.
#
# Usage:
#   ./scripts/jenkins/setup.sh

set -euo pipefail

CONFIG_FILE="jenkins.config.env"
MAX_WAIT=120

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: $CONFIG_FILE not found."
  echo "       Copy jenkins.config.env.example to jenkins.config.env and fill in your values."
  exit 1
fi

# Load config to resolve JENKINS_PUBLIC_URL for readiness check
# shellcheck disable=SC1090
source "$CONFIG_FILE"
JENKINS_URL="${JENKINS_PUBLIC_URL:-http://localhost:8080}"

echo "==> Starting services..."
docker compose up -d

echo "==> Waiting for Jenkins at $JENKINS_URL (max ${MAX_WAIT}s)..."
elapsed=0
until curl -sf -o /dev/null "$JENKINS_URL/login"; do
  if [ "$elapsed" -ge "$MAX_WAIT" ]; then
    echo "ERROR: Jenkins not reachable after ${MAX_WAIT}s. Check: docker compose logs jenkins-custom"
    exit 1
  fi
  sleep 3
  elapsed=$(( elapsed + 3 ))
  echo "    ...${elapsed}s"
done

echo ""
echo "Done! Jenkins is up at $JENKINS_URL  (admin / <JENKINS_ADMIN_PASSWORD from jenkins.config.env>)"
echo "API calls use JENKINS_API_TOKEN from jenkins.config.env — no token was generated or changed."
