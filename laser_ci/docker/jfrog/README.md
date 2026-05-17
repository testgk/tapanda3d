# JFrog Configuration

This folder contains the JFrog Artifactory configuration for the laser CI/CD system.

## Files

- `jfrog.env.config.example` - Example configuration file with all available options
- `jfrog.env.config` - Actual configuration file (gitignored, create from example)

## Setup

1. Copy the example file:
   ```bash
   cp jfrog.env.config.example jfrog.env.config
   ```

2. Edit the configuration file with your JFrog instance details:
   ```bash
   nano jfrog.env.config
   ```

3. Fill in the required values:
   - `JFROG_URL`: Your JFrog Artifactory instance URL
   - `JFROG_REPO`: Repository name for publishing artifacts
   - `GITLAB_ACCESS_TOKEN`: Your GitLab access token for authentication

## Usage

The configuration is automatically loaded by Docker Compose when running:

```bash
docker-compose up -d
```

The JFrog CLI service will be configured with your settings and ready for publishing operations.

## Security

- The `jfrog.env.config` file is gitignored and should never be committed
- Keep your GitLab access token secure
- Only share the `.example` file which contains no sensitive information
