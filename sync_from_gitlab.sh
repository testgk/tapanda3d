#!/bin/bash

# Script to sync changes from GitLab repository to the local repository
# Based on the GitHub Actions workflow at .github/workflows/gitlab-sync.yml

set -e  # Exit on error

echo "=== GitLab to Local Repository Sync Script ==="
echo ""

# Configure Git
echo "Configuring Git..."
git config user.name "GitLab Sync Script"
git config user.email "sync-script@local"
echo "✓ Git configured"
echo ""

# Add GitLab remote
echo "Setting up GitLab remote..."
if git remote get-url gitlab >/dev/null 2>&1; then
  echo "GitLab remote already exists, updating URL..."
  git remote set-url gitlab https://gitlab.com/testgk/tapanda3d.git
else
  echo "Adding GitLab remote..."
  git remote add gitlab https://gitlab.com/testgk/tapanda3d.git
fi
echo "✓ GitLab remote configured"
echo ""

# Fetch from GitLab
echo "Fetching from GitLab repository..."
git fetch gitlab --prune
echo "✓ Fetched from GitLab"
echo ""

# Detect GitLab default branch
echo "Detecting GitLab default branch..."
GITLAB_DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/gitlab/HEAD 2>/dev/null | sed 's@^refs/remotes/gitlab/@@' || echo "")

# Fallback to git ls-remote if symbolic-ref fails
if [ -z "$GITLAB_DEFAULT_BRANCH" ]; then
  GITLAB_DEFAULT_BRANCH=$(git ls-remote --symref gitlab HEAD 2>/dev/null | head -n1 | awk '{print $2}' | sed 's@refs/heads/@@' || echo "")
fi

# Final fallback to 'main' if all else fails
if [ -z "$GITLAB_DEFAULT_BRANCH" ]; then
  GITLAB_DEFAULT_BRANCH="main"
fi

echo "GitLab default branch: ${GITLAB_DEFAULT_BRANCH}"
echo ""

# Sync default branch
echo "Syncing from GitLab branch: ${GITLAB_DEFAULT_BRANCH}"

# Validate branch name is not empty
if [ -z "$GITLAB_DEFAULT_BRANCH" ]; then
  echo "❌ Error: Could not determine GitLab default branch"
  exit 1
fi

# Validate branch name contains only valid characters
if ! echo "$GITLAB_DEFAULT_BRANCH" | grep -qE '^[a-zA-Z0-9/_.-]+$'; then
  echo "❌ Error: Invalid branch name detected: ${GITLAB_DEFAULT_BRANCH}"
  exit 1
fi

# Get the current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current local branch: ${CURRENT_BRANCH}"
echo ""

# Check if GitLab branch exists
if git rev-parse gitlab/${GITLAB_DEFAULT_BRANCH} >/dev/null 2>&1; then
  # Check if we're already up to date
  if git merge-base --is-ancestor gitlab/${GITLAB_DEFAULT_BRANCH} HEAD; then
    echo "✓ Already up to date with GitLab"
    exit 0
  fi
  
  # Attempt to merge changes
  echo "Merging changes from GitLab..."
  if git merge gitlab/${GITLAB_DEFAULT_BRANCH} -m "Sync from GitLab ${GITLAB_DEFAULT_BRANCH} branch"; then
    echo "✓ Successfully merged changes from GitLab"
  else
    echo "❌ Merge conflict detected. Manual intervention required."
    exit 1
  fi
else
  echo "❌ GitLab branch ${GITLAB_DEFAULT_BRANCH} not found"
  exit 1
fi

echo ""
echo "=== Sync Complete ==="
echo "Note: Changes are merged locally. To push to GitHub, run: git push origin ${CURRENT_BRANCH}"
