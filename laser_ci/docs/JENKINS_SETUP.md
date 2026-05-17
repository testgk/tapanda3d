# 🚀 Jenkins-GitLab CI/CD Synchronization Setup

## Overview

This guide sets up Jenkins to synchronize with GitLab CI/CD pipelines for the Laser CI project. Jenkins acts as the integration test runner, receiving build artifacts from GitLab and providing detailed test reports.

## Quick Setup

### 1. Start Jenkins (Docker)
```bash
cd runner
docker-compose up -d jenkins
```

### 2. Get Jenkins Initial Admin Password
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

### 3. Configure Jenkins
1. Open http://localhost:8080
2. Enter admin password
3. Install suggested plugins
4. Create admin user

### 4. Get API Token
1. Go to: http://localhost:8080/user/admin/configure
2. Click "Add new Token"
3. Copy the token value

### 5. Run Setup Script
```bash
export JENKINS_TOKEN="your_token_here"
./scripts/setup_jenkins.sh
```

## Environment Variables

Set these in GitLab CI/CD Variables (protected/masked):

| Variable | Value | Protected | Masked |
|----------|-------|-----------|--------|
| `JENKINS_URL` | `http://jenkins:8080` | ✅ | ❌ |
| `JENKINS_USER` | `admin` | ✅ | ❌ |
| `JENKINS_API_TOKEN` | `your_token` | ✅ | ✅ |
| `GITLAB_ACCESS_TOKEN` | `glpat-xxxxx` | ✅ | ✅ |
| `JENKINS_JOB_NAME` | `laser-integration-tests` | ❌ | ❌ |

## Jenkins Job Features

### Parameters
- `GITLAB_ARTIFACT_URL` - URL to download build artifacts
- `GITLAB_ACCESS_TOKEN` - Token for GitLab API access
- `GITLAB_PIPELINE_ID` - Source pipeline ID
- `GITLAB_COMMIT_SHA` - Commit SHA
- `GITLAB_BRANCH` - Branch name

### Pipeline Stages
1. **Setup & Validation** - Parameter validation
2. **Checkout Tests** - Clone test suite
3. **Download Artifacts** - Get build artifacts from GitLab
4. **Validate Build** - Check libraries and headers
5. **Run Integration Tests** - Execute pytest suite
6. **Performance Tests** - Basic performance validation

### Synchronization Features
- **Bidirectional Status Updates** - Jenkins updates GitLab pipeline status
- **Enhanced Traceability** - Full build context tracking
- **Detailed Reports** - JUnit XML and HTML test reports

## Testing the Integration

### Manual Test
```bash
# Test connection
python scripts/setup_jenkins.py --test-connection --jenkins-token YOUR_TOKEN

# Create job
python scripts/setup_jenkins.py --create-job --jenkins-token YOUR_TOKEN

# Trigger test
python scripts/setup_jenkins.py --trigger-test --jenkins-token YOUR_TOKEN
```

### Full Pipeline Test
1. Push to GitLab main branch
2. Monitor GitLab pipeline
3. Check Jenkins job execution
4. Verify test reports
5. Confirm status updates

## Troubleshooting

### Connection Issues
```bash
# Check Jenkins
curl http://localhost:8080/api/json

# Check Docker
docker ps | grep jenkins
```

### Authentication Issues
```bash
# Verify token
curl -u "admin:YOUR_TOKEN" http://localhost:8080/api/json
```

### Integration Issues
- Check GitLab token has `read_api` scope
- Verify artifact URLs are accessible
- Check network connectivity

## Files Reference

| File | Purpose |
|------|---------|
| `jenkins-job-config.xml` | Jenkins job configuration |
| `scripts/setup_jenkins.sh` | Bash setup script |
| `scripts/setup_jenkins.py` | Python setup script |
| `runner/docker-compose.yml` | Docker orchestration |

---

**Last Updated:** 2026-05-10
