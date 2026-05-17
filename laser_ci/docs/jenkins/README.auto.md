# Automated Jenkins Setup for Laser CI

This directory contains automated Jenkins setup for the Laser CI project, allowing you to run Jenkins with pre-configured jobs and API tokens in different environments.

## Quick Start Options

### Option 1: Fully Automated Setup (Recommended)
```bash
chmod +x scripts/jenkins/setup_auto.sh
./scripts/jenkins/setup_auto.sh
```

### Option 2: Custom Docker Image with Build-Time Token Generation
```bash
# Build image with token generated during build
docker build -f docker/jenkins/Dockerfile_.token-build -t laser-ci-jenkins .

# Run the container (token will be displayed on startup)
docker run -d -p 8080:8080 laser-ci-jenkins

# Extract token from built image without running
./scripts/jenkins/extract_token.sh laser-ci-jenkins
```

### Option 3: Custom Docker Image with Runtime Token Generation
```bash
# Build image with token generated when container starts
docker build -f docker/jenkins/Dockerfile_.custom -t laser-ci-jenkins .

# Run the container
docker run -d -p 8080:8080 laser-ci-jenkins

# Get token from running container
docker exec $(docker ps -q --filter ancestor=laser-ci-jenkins) cat /var/jenkins_home/api-token.txt
```

## Dockerfile Options

| Dockerfile | Token Generation | When Token is Available |
|------------|------------------|-------------------------|
| `Dockerfile.jenkins-token-build` | **During build** | Immediately after build |
| `Dockerfile.jenkins-custom` | **During startup** | After container starts |
| `Dockerfile.jenkins-custom-token` | **During startup** | After container starts |

## Build-Time Token Generation (Option 2)

The `Dockerfile.jenkins-token-build` generates the API token during the Docker build process:

```dockerfile
# Generate a deterministic API token during build
RUN mkdir -p /var/jenkins_home && \
    echo "laser-ci-jenkins-token-2026" > /tmp/seed.txt && \
    JENKINS_API_TOKEN=$(openssl dgst -sha256 -hex /tmp/seed.txt | cut -d' ' -f2 | cut -c1-32) && \
    echo "$JENKINS_API_TOKEN" > /var/jenkins_home/api-token.txt
```

**Benefits:**
- ✅ Token available immediately after build
- ✅ Deterministic token (same every build)
- ✅ No need to wait for Jenkins startup
- ✅ Can extract token without running container

**Usage:**
```bash
# Build and extract token
docker build -f docker/jenkins/Dockerfile_.token-build -t laser-ci-jenkins .
./scripts/jenkins/extract_token.sh laser-ci-jenkins

# Output:
# ==================================================
#   Jenkins API Token from Docker Image
# ==================================================
# Image: laser-ci-jenkins
# Token: a1b2c3d4e5f67890123456789012345
#
# Add to GitLab CI/CD variables:
# JENKINS_API_TOKEN: "a1b2c3d4e5f67890123456789012345"
# ==================================================
```

## Files Overview

| File | Purpose |
|------|---------|
| `docker/jenkins/Dockerfile.token-build` | **Build-time token generation** |
| `docker/jenkins/Dockerfile.custom` | Runtime token generation |
| `docker/jenkins/Dockerfile.custom-token` | Alternative runtime generation |
| `docker-compose.yml` | Automated deployment |
| `scripts/jenkins/extract_token.sh` | Extract token from built image |
| `docker/jenkins/init.groovy` | Jenkins initialization |
| `docker/jenkins/casc.yaml` | Configuration as Code |
| `scripts/jenkins/setup_auto.sh` | Fully automated setup |
| `docker/jenkins/entrypoint.sh` | Custom entrypoint |

## Token Generation Methods

### 1. Build-Time Generation (Deterministic)
- Uses fixed seed + SHA256 hash
- Same token every build
- Available immediately after `docker build`
- Extract with `extract_jenkins_token.sh`

### 2. Runtime Generation (Random)
- Generated when Jenkins starts
- Unique token per container
- Available after Jenkins initialization
- Extract with `docker exec cat /var/jenkins_home/api-token.txt`

## Environment Variables

Set these when running the container:

```bash
# Jenkins Configuration
JENKINS_ADMIN_ID=admin
JENKINS_ADMIN_PASSWORD=admin
JENKINS_URL=http://localhost:8080

# Laser CI Integration
JENKINS_JOB_NAME=laser-integration-tests
GITLAB_PROJECT_URL=https://gitlab.com/aqualaser/laser_ci

# API Tokens (override these in production)
JENKINS_API_TOKEN=your-jenkins-api-token
GITLAB_ACCESS_TOKEN=your-gitlab-access-token
```

## CI/CD Integration Examples

### GitLab CI/CD
```yaml
stages:
  - build
  - test
  - deploy

variables:
  JENKINS_API_TOKEN: "a1b2c3d4e5f67890123456789012345"  # From build-time generation

jenkins_integration:
  stage: test
  script:
    - docker build -f docker/jenkins/Dockerfile_.token-build -t laser-ci-jenkins .
    - |
      JENKINS_TOKEN=$(docker run --rm laser-ci-jenkins /bin/bash -c 'cat /var/jenkins_home/api-token.txt')
      echo "JENKINS_API_TOKEN=$JENKINS_TOKEN" >> build.env
  artifacts:
    reports:
      dotenv: build.env
```

### GitHub Actions
```yaml
- name: Build Jenkins Image
  run: docker build -f docker/jenkins/Dockerfile_.token-build -t laser-ci-jenkins .

- name: Extract Jenkins Token
  run: |
    TOKEN=$(docker run --rm laser-ci-jenkins /bin/bash -c 'cat /var/jenkins_home/api-token.txt')
    echo "JENKINS_API_TOKEN=$TOKEN" >> $GITHUB_ENV
```

## Security Considerations

### Production Deployment
- **Use build-time token generation** for consistent tokens
- **Override tokens** with environment variables in production
- **Store tokens securely** (GitLab CI/CD variables, Kubernetes secrets)
- **Rotate tokens regularly** using new seed values

### Token Storage
- **Never commit tokens** to version control
- **Use environment variables** for runtime configuration
- **Extract tokens programmatically** in CI/CD pipelines
- **Monitor token usage** and rotate when needed

## Troubleshooting

### Build-Time Token Issues
```bash
# Check if token was generated during build
docker run --rm laser-ci-jenkins /bin/bash -c 'cat /var/jenkins_home/api-token.txt'

# Use the extraction script
./scripts/jenkins/extract_token.sh laser-ci-jenkins
```

### Runtime Token Issues
```bash
# Check Jenkins logs
docker logs $(docker ps -q --filter ancestor=laser-ci-jenkins)

# Check if token file exists
docker exec $(docker ps -q --filter ancestor=laser-ci-jenkins) ls -la /var/jenkins_home/api-token.txt

# Extract token manually
docker exec $(docker ps -q --filter ancestor=laser-ci-jenkins) cat /var/jenkins_home/api-token.txt
```

### Jenkins Startup Issues
```bash
# Check container health
docker ps --filter ancestor=laser-ci-jenkins

# Check Jenkins health endpoint
curl http://localhost:8080/login

# View Jenkins logs
docker logs $(docker ps -q --filter ancestor=laser-ci-jenkins) | tail -50
```

---

**Result**: Jenkins API tokens generated during Docker build process, available immediately without running containers! 🎉
