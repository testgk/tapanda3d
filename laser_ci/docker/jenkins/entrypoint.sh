#!/bin/bash
set -e

if [ -z "$JENKINS_ADMIN_PASSWORD" ]; then
  echo "ERROR: JENKINS_ADMIN_PASSWORD is not set. Copy jenkins.config.env.example to jenkins.config.env and fill in your values."
  exit 1
fi

exec /usr/local/bin/jenkins.sh "$@"
