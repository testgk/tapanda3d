# ta3d

A Panda3D-based terrain simulation project.

## 🔄 GitLab Sync (Automatic Mirror)

> **📍 Repository Info:**
> - **This is the GitHub repository** (`github.com/testgk/tapanda3d`)
> - **Changes made**: Added automation workflow to THIS GitHub repository
> - **Sync direction**: GitLab → GitHub (one-way sync FROM GitLab TO here)
> - **Source repository**: `https://gitlab.com/testgk/tapanda3d` (GitLab)

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
3. Keeps both repositories in sync (GitLab → GitHub direction)

### Setup Notes

- The workflow uses the default `GITHUB_TOKEN` for authentication. If your repository uses branch protection rules, you may need to configure a Personal Access Token (PAT) with appropriate permissions and add it as a repository secret.
- The sync includes `[skip ci]` in commit messages to prevent circular triggers.
- If merge conflicts occur, the workflow will fail and require manual intervention.
- The hourly sync schedule can be adjusted in the workflow file if a different frequency is preferred.

---

## 🔐 Secrets & Settings — Where to Find Them

The workflow requires one manually-configured secret (`GITLAB_TOKEN`) in addition to the automatically-provided `GITHUB_TOKEN`.

### 1. `GITHUB_TOKEN` (automatic)

This secret is **automatically created by GitHub** for every repository. You do **not** need to create it yourself. It is available to every workflow run under `secrets.GITHUB_TOKEN`.

> If you use branch protection rules that prevent the default `GITHUB_TOKEN` from pushing, create a **Personal Access Token (PAT)** (see step 3 below) and add it as a secret named `GITHUB_TOKEN` to override the default.

### 2. `GITLAB_TOKEN` — How to create it on GitLab

1. Sign in to **GitLab** at [https://gitlab.com](https://gitlab.com).
2. Click your **avatar** (top-right corner) → **Edit profile**.
3. In the left sidebar choose **Access Tokens**.
4. Click **Add new token**.
5. Give it a name (e.g. `github-sync`), set an expiry date if desired, and tick the **`read_repository`** scope.
6. Click **Create personal access token** and **copy the token value** — it is shown only once.

### 3. Adding secrets to this GitHub repository

1. Open this repository on GitHub.
2. Click the **Settings** tab (top navigation bar of the repository).
3. In the left sidebar expand **Secrets and variables** → click **Actions**.
4. Click **New repository secret**.
5. Set **Name** to `GITLAB_TOKEN` and paste the token value you copied from GitLab into the **Secret** field.
6. Click **Add secret**.

> **Location in the GitHub UI:**
> `https://github.com/<owner>/<repo>/settings/secrets/actions`

That's it — the workflow will now use your `GITLAB_TOKEN` to authenticate with GitLab and `GITHUB_TOKEN` to push synced changes back to this repository.