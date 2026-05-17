#!/usr/bin/env bash
# Monitor GitLab pipelines interactively.
# Usage:
#   ./scripts/check_pipeline.sh          — list active pipelines, pick one
#   ./scripts/check_pipeline.sh <branch> — jump straight to latest on branch
#   ./scripts/check_pipeline.sh <id>     — jump straight to pipeline by ID

set -euo pipefail

TOKEN="glpat-nz-6SbE4Uc1BFt5vNNXUjWM6MQpvOjEKdTpoZDNqMg8.01.170gjyz6b"
PROJECT_ID="77867289"
API="https://gitlab.com/api/v4"

print_jobs() {
  local pipe_id="$1"
  curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
    "$API/projects/$PROJECT_ID/pipelines/$pipe_id/jobs" | python3 -c "
import sys, json

ICON = {'success':'✓','failed':'✗','running':'►','pending':'…','created':'·','skipped':'—','canceled':'⊘'}

jobs = json.load(sys.stdin)
stage = None
for j in reversed(jobs):
    if j['stage'] != stage:
        stage = j['stage']
        print(f'  [{stage}]')
    icon = ICON.get(j['status'], '?')
    dur  = f\"{int(j['duration'])}s\" if j.get('duration') else ''
    note = f\"  ({j['failure_reason']})\" if j['status'] == 'failed' and j.get('failure_reason') else ''
    print(f'    {icon} {j[\"status\"]:10}  {j[\"name\"]:30}  {dur}{note}')
"
}

watch_pipeline() {
  local pipe_id="$1"
  local info
  info=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" "$API/projects/$PROJECT_ID/pipelines/$pipe_id" | python3 -c "
import sys,json
p=json.load(sys.stdin)
print(p['id'], p['status'], p['sha'][:8], p['ref'], p['created_at'][:16].replace('T',' '))
")
  local status ref sha created
  read -r pipe_id status sha ref created <<< "$info"

  echo ""
  echo "Pipeline: #$pipe_id  [$ref]  sha=$sha  created=$created  status=$status"
  echo ""
  print_jobs "$pipe_id"

  if [[ "$status" == "running" || "$status" == "pending" || "$status" == "created" ]]; then
    echo ""
    echo "Polling every 10s... (Ctrl+C to stop)"
    while true; do
      sleep 10
      status=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
        "$API/projects/$PROJECT_ID/pipelines/$pipe_id" | python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
      if [[ "$status" == "success" || "$status" == "failed" || "$status" == "canceled" ]]; then
        echo "$(date +%H:%M:%S) — $status"
        echo ""
        print_jobs "$pipe_id"
        break
      else
        echo -ne "$(date +%H:%M:%S) — $status\r"
      fi
    done
  fi
}

# --- Argument handling ---
ARG="${1:-}"

# If numeric ID passed directly
if [[ "$ARG" =~ ^[0-9]+$ ]] && [[ ${#ARG} -gt 6 ]]; then
  watch_pipeline "$ARG"
  exit 0
fi

# If branch name passed, jump to latest on that branch
if [[ -n "$ARG" ]]; then
  PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
    "$API/projects/$PROJECT_ID/pipelines?ref=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote('$ARG'))")&per_page=1" | \
    python3 -c "import sys,json; print(json.load(sys.stdin)[0]['id'])")
  watch_pipeline "$PIPE_ID"
  exit 0
fi

# --- Interactive mode: list recent pipelines and pick one ---
echo "Recent pipelines:"
echo ""
PIPELINES=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$API/projects/$PROJECT_ID/pipelines?per_page=10" | python3 -c "
import sys,json
ICON = {'success':'✓','failed':'✗','running':'►','pending':'…','created':'·','canceled':'⊘'}
pipes = json.load(sys.stdin)
for i,p in enumerate(pipes):
    icon = ICON.get(p['status'],'?')
    t = p['created_at'][:16].replace('T',' ')
    print(f\"{i+1}) {icon} #{p['id']}  {p['status']:10}  {p['ref']:30}  {t}\")
")
echo "$PIPELINES"
echo ""

# Count entries
COUNT=$(echo "$PIPELINES" | wc -l)

read -rp "Select pipeline [1-$COUNT] or press Enter for latest: " CHOICE
CHOICE="${CHOICE:-1}"

PIPE_ID=$(curl -sf --header "PRIVATE-TOKEN: $TOKEN" \
  "$API/projects/$PROJECT_ID/pipelines?per_page=10" | python3 -c "
import sys,json
pipes=json.load(sys.stdin)
idx=int('$CHOICE')-1
print(pipes[idx]['id'])
")

watch_pipeline "$PIPE_ID"