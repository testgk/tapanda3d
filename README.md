# ta3d

A Panda3D-based terrain simulation project.

## GitLab Sync

This GitHub repository is automatically synchronized with the GitLab repository at `https://gitlab.com/testgk/tapanda3d`.

The sync runs:
- **Automatically**: Every hour via scheduled GitHub Actions workflow
- **Manually**: Can be triggered manually from the GitHub Actions tab

### How It Works

The GitHub Actions workflow (`.github/workflows/gitlab-sync.yml`) automatically fetches the latest changes from the GitLab repository and merges them into this GitHub repository. This ensures that both repositories stay in sync.

### Setup Notes

- The workflow uses the default `GITHUB_TOKEN` for authentication. If your repository uses branch protection rules, you may need to configure a Personal Access Token (PAT) with appropriate permissions and add it as a repository secret.
- The sync includes `[skip ci]` in commit messages to prevent circular triggers.
- If merge conflicts occur, the workflow will fail and require manual intervention.