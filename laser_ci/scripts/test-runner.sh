#!/bin/bash
# Verify the runner config and connectivity before triggering a pipeline.
# Usage: bash scripts/test-runner.sh

set -euo pipefail

RUNNER="gitlab-runner-1"
JENKINS_URL="http://jenkins:8080"

echo "==> 1. Runner container is running..."
docker inspect "$RUNNER" --format '{{.State.Status}}' | grep -q running \
  && echo "    OK" \
  || { echo "    FAIL: start it with: docker compose up -d"; exit 1; }

echo ""
echo "==> 2. JENKINS_API_TOKEN is set in config.toml..."
docker exec "$RUNNER" grep -q "JENKINS_API_TOKEN=" /etc/gitlab-runner/config.toml \
  && echo "    OK" \
  || { echo "    FAIL: add JENKINS_API_TOKEN to config.toml environment array"; exit 1; }

echo ""
echo "==> 3. GITLAB_ACCESS_TOKEN is set in config.toml..."
docker exec "$RUNNER" grep -q "GITLAB_ACCESS_TOKEN=" /etc/gitlab-runner/config.toml \
  && echo "    OK" \
  || { echo "    FAIL: add GITLAB_ACCESS_TOKEN to config.toml environment array"; exit 1; }

echo ""
echo "==> 4. Jenkins reachable from a job container (ci network)..."
docker run --rm --network ci ubuntu:22.04 \
  bash -c "apt-get install -qq -y curl > /dev/null 2>&1 && curl -sf -u admin:admin $JENKINS_URL/api/json -o /dev/null" \
  && echo "    OK" \
  || { echo "    FAIL: Jenkins not reachable at $JENKINS_URL from the ci network"; exit 1; }

echo ""
echo "==> 5. Jenkins job exists..."
docker run --rm --network ci ubuntu:22.04 \
  bash -c "apt-get install -qq -y curl > /dev/null 2>&1 && curl -sf -u admin:admin $JENKINS_URL/job/laser-integration-tests/api/json -o /dev/null" \
  && echo "    OK" \
  || echo "    FAIL: job 'laser-integration-tests' not found — rebuild the Jenkins image"

echo ""
echo "All checks passed. Runner is ready."
