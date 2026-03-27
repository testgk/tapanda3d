# ta3d

A Panda3D-based terrain simulation project.

## 🔄 GitLab Sync (Automatic Mirror)

[![Sync from GitLab](https://github.com/testgk/tapanda3d/actions/workflows/gitlab-sync.yml/badge.svg)](https://github.com/testgk/tapanda3d/actions/workflows/gitlab-sync.yml)

> **📍 Repository Info:**
> - **This is the GitHub repository** (`github.com/testgk/tapanda3d`)
> - **Changes made**: Added automation workflow to THIS GitHub repository
> - **Sync direction**: GitLab → GitHub (one-way sync FROM GitLab TO here)
> - **Source repository**: `https://gitlab.com/testgk/tapanda3d` (GitLab)

### When Was Code Last Pulled from GitLab?

- **Quick check**: See the [`LAST_GITLAB_SYNC`](./LAST_GITLAB_SYNC) file in this repository — it is updated automatically by the workflow every time new changes are pulled from GitLab. It contains the UTC timestamp, the GitLab branch name, and the commit SHA that was synced.
- **Workflow history**: Click the badge above (or visit the [Actions tab](https://github.com/testgk/tapanda3d/actions/workflows/gitlab-sync.yml)) to see the full run history with timestamps of every sync attempt.

### What Was Updated?

This **GitHub repository** now contains a GitHub Actions workflow that automatically pulls changes from the GitLab repository. The workflow file was added to THIS GitHub repository at `.github/workflows/gitlab-sync.yml`.

**No changes were made to the GitLab repository.** The GitLab repository remains the source of truth, and this GitHub repository automatically mirrors it.

### Sync Schedule

The sync runs:
- **Automatically**: Every hour via scheduled GitHub Actions workflow (ensuring frequent updates)
- **Manually**: Can be triggered manually from the GitHub Actions tab when immediate sync is needed

### How It Works

The GitHub Actions workflow automatically:
1. Fetches the latest changes from the **GitLab** repository (`https://gitlab.com/testgk/tapanda3d`)
2. Merges those changes into this **GitHub** repository
3. Updates [`LAST_GITLAB_SYNC`](./LAST_GITLAB_SYNC) with the timestamp and commit SHA of the sync
4. Keeps both repositories in sync (GitLab → GitHub direction)

### Setup Notes

- The workflow uses the default `GITHUB_TOKEN` for authentication. If your repository uses branch protection rules, you may need to configure a Personal Access Token (PAT) with appropriate permissions and add it as a repository secret.
- The sync includes `[skip ci]` in commit messages to prevent circular triggers.
- If merge conflicts occur, the workflow will fail and require manual intervention.
- The hourly sync schedule can be adjusted in the workflow file if a different frequency is preferred.