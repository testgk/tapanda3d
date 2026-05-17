# JFrog Artifactory Setup

This document explains how to configure and use JFrog Artifactory for publishing laser project artifacts instead of GitLab.

## Overview

The laser CI/CD system now supports publishing to JFrog Artifactory using the GitLab access token for authentication, as requested.

## Configuration

### Environment Variables

Create the configuration file:

```bash
# Copy the example file
cp jfrog/jfrog.env.config.example jfrog/jfrog.env.config

# Edit with your values
nano jfrog/jfrog.env.config
```

The configuration file contains:

```dotenv
# JFrog Artifactory Configuration
# Copy this file to jfrog/jfrog.env.config and fill in your values.
# jfrog/jfrog.env.config is gitignored — never commit it.

# --- JFrog Artifactory ---
# URL of your JFrog Artifactory instance
JFROG_URL=https://your-jfrog-instance.jfrog.io

# Repository name in JFrog Artifactory
JFROG_REPO=laser-ci-generic

# --- Authentication ---
# GitLab access token (used for JFrog authentication as requested)
GITLAB_ACCESS_TOKEN=your-gitlab-access-token-here

# Alternative JFrog authentication (uncomment if not using GitLab token)
# JFROG_API_KEY=your-jfrog-api-key
# JFROG_USERNAME=your-jfrog-username
# JFROG_PASSWORD=your-jfrog-password

# --- Optional JFrog Settings ---
# JFrog CLI log level (DEBUG, INFO, WARN, ERROR)
JFROG_CLI_LOG_LEVEL=INFO
```

### Docker Compose

The `jfrog-cli` service is automatically included in both `docker-compose.yml` and `docker-compose.simple.yml`.

Start the services:

```bash
docker-compose up -d
```

## Publishing Process

### Automatic Publishing

The build scripts automatically publish to JFrog:

```bash
# Publish a project (clones, builds, and publishes)
python scripts/py/publish.py lasershark

# Skip publishing
python scripts/py/publish.py lasershark --skip-publish

# Push already built artifacts
python scripts/py/push_to_jfrog.py lasershark
```

### Manual Publishing

You can also publish manually using the JFrog CLI:

```bash
# Configure JFrog CLI
docker exec jfrog-cli jfrog config add laser-ci \
  --url=$JFROG_URL \
  --access-token=$GITLAB_ACCESS_TOKEN

# Upload artifacts
docker exec jfrog-cli jfrog rt upload \
  "install/lib/liblasershark.*" \
  $JFROG_REPO/lasershark/1.0.0/
```

## Authentication

The system uses the GitLab access token for JFrog authentication as requested. The authentication hierarchy is:

1. `GITLAB_ACCESS_TOKEN` (as Bearer token)
2. `JFROG_API_KEY` (X-JFrog-Art-Api header)
3. `JFROG_USERNAME` + `JFROG_PASSWORD` (Basic auth)

## Artifacts Structure

Artifacts are published with the following structure:

```
{your-jfrog-instance}/artifactory/laser-ci-generic/
├── lasershark/1.0.0/
│   ├── liblasershark.a
│   ├── liblasershark.so
│   ├── LaserShark.h
│   ├── LaserSharkConfig.cmake
│   └── ...
├── lasergun/1.0.0/
│   └── ...
└── ...
```

## Migration from GitLab

The system has been updated to use JFrog instead of GitLab's Generic Package Registry:

- `publish_to_registry.py` → `publish_to_jfrog.py`
- `push_to_registry.py` → `push_to_jfrog.py`
- GitLab API calls → JFrog REST API calls
- `GITLAB_ACCESS_TOKEN` now used for JFrog authentication

## Testing

Test the JFrog publishing:

```bash
# Test publishing script
python scripts/py/push_to_jfrog.py lasershark

# Check JFrog CLI configuration
docker logs jfrog-cli
```

## Troubleshooting

### Authentication Issues

- Ensure `GITLAB_ACCESS_TOKEN` is set and has appropriate permissions
- Check JFrog instance URL is correct
- Verify repository exists and is accessible

### Upload Failures

- Check network connectivity to JFrog instance
- Verify artifact paths exist in `install/` directory
- Check JFrog CLI logs: `docker logs jfrog-cli`

### Configuration Issues

- Ensure environment variables are properly set
- Check docker-compose service is running: `docker ps`
- Verify volume mounts are correct
