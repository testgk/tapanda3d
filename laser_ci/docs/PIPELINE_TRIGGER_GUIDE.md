# 🚀 Laser CI Pipeline Trigger Guide

## Project Architecture

**laser_ci** is a multi-component C++ integration project orchestrating:
- `creatures` - Base creature classes
- `lasergun` - Laser weapon system (Project ID: 77866175)
- `brain_implant` - Neural interface
- `lasershark` - Laser-equipped shark (Project ID: 77866232, depends on lasergun)
- `laserwhale` - Laser-equipped whale

---

## Pipeline Stages

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: BUILD                                              │
│   build_lasergun (optional)  ──────┐                       │
│   build_lasershark (depends) ──────┤                       │
└─────────────────────────────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 2: INTEGRATE                                          │
│   integration_tests (Jenkins job) ◄ Downloads all packages │
└─────────────────────────────────────────────────────────────┘
                                      ▼
┌─────────────────────────────────────────────────────────────┐
│ STAGE 3: DEPLOY                                             │
│   deploy_lasergun   ──────┐                                │
│   deploy_lasershark ──────┤ Publish to GitLab Registry    │
└─────────────────────────────────────────────────────────────┘
```

**Pipeline Logic:**
- If `TRIGGERED_BY=lasergun` → rebuild lasergun + lasershark
- If `TRIGGERED_BY=lasershark` → skip lasergun, rebuild lasershark  
- If `TRIGGERED_BY=null` (default) → full rebuild (lasergun + lasershark)

---

## How to Trigger a Pipeline

### **Method 1: GitLab CI/CD (Primary)**

**Automatic trigger on push to main:**
```bash
git push origin main
```

This runs all 3 stages: build → integrate → deploy

**Manual trigger from GitLab UI:**
1. Go to **CI/CD → Pipelines** in the GitLab project
2. Click **"Run pipeline"**
3. Optionally set variables like:
   - `TRIGGERED_BY=lasershark` (skip lasergun rebuild)
   - `PACKAGE_VERSION=1.1.0` (version override)

---

### **Method 2: Trigger Configuration (Cross-Project)**

When another project (e.g., lasershark repo) needs to trigger laser_ci:

**From the remote project's CI job:**
```bash
python3 scripts/py/trigger_config.py write lasershark \
    --version 1.1.0 \
    --branch feature/new-laser \
    --output trigger.json
```

**Generated trigger.json:**
```json
{
  "project": "lasershark",
  "version": "1.1.0",
  "branch": "feature/new-laser"
}
```

**In laser_ci's .gitlab-ci.yml, add dependency:**
```yaml
build_lasershark:
  needs:
    - project: aqualaser/lasershark
      job: prepare_trigger
      artifacts: true  # downloads trigger.json
```

laser_ci automatically picks up the config via `load_trigger_config()`.

---

### **Method 3: Jenkins Integration Tests Trigger**

**For direct Jenkins integration:**

**Prerequisites:**
Set environment variables (in GitLab CI/CD → Settings → Variables):
```
JENKINS_URL=https://jenkins.example.com
JENKINS_USER=admin
JENKINS_API_TOKEN=<your-token>
GITLAB_ACCESS_TOKEN=<gitlab-token-with-read_api>
JENKINS_JOB_NAME=laser-integration-tests
```

**Trigger from laser_ci integration job:**
```bash
CI_JOB_ID=$(curl -sf ...) python3 scripts/py/trigger_jenkins.py
```

The script:
1. Builds the GitLab artifact download URL
2. Triggers Jenkins job with parameters:
   - `GITLAB_ARTIFACT_URL` - Where Jenkins downloads built artifacts
   - `GITLAB_ACCESS_TOKEN` - Auth token for GitLab
   - `GITLAB_PIPELINE_ID` - For traceability
3. Polls Jenkins until build completes
4. Returns exit code based on Jenkins result

---

## Configuration Files

### Project Configs
Located in `configs/` directory:

**lasershark.ini:**
```ini
[package]
name = lasershark
id = 77866232
version = 1.0.0

[dependencies]
lasergun = 77866175

[source]
url = https://gitlab.com/aqualaser/lasershark.git

[registry]
url = https://gitlab.com/api/v4/projects

[paths]
repo_root = ..
build_dir = ../build
install_dir = ../install
```

**lasergun.ini:**
```ini
[package]
name = lasergun
id = 77866175
version = 1.0.0

[source]
url = https://gitlab.com/aqualaser/lasergun.git
...
```

---

## Build Scripts Reference

### `scripts/py/build.py`
Configures and builds a project using CMake.

**Usage:**
```bash
python scripts/py/build.py <project>
```

**What it does:**
1. Sets `CMAKE_PREFIX_PATH` to `install/`
2. Runs CMake configure
3. Builds with `cmake --build`
4. Installs to `install/` directory

### `scripts/py/download.py`
Downloads pre-built packages from GitLab Package Registry.

### `scripts/py/publish.py`
Builds and publishes artifacts to the registry.

### `scripts/py/trigger_config.py`
Generates `trigger.json` for cross-project triggers.

### `scripts/py/trigger_jenkins.py`
Triggers a Jenkins job and waits for completion.

---

## Package Registry

All built packages stored at:
```
https://gitlab.com/api/v4/projects/{PROJECT_ID}/packages/generic/{NAME}/{VERSION}/
```

**Example URLs:**
- Lasergun (v1.0.0): `api/v4/projects/77866175/packages/generic/lasergun/1.0.0/`
- Lasershark (v1.0.0): `api/v4/projects/77866232/packages/generic/lasershark/1.0.0/`

Each package contains:
- `lib{name}.a` - Static library
- `lib{name}.so` - Shared library
- `include/{name}/*.h` - Headers
- `lib/cmake/{name}/*.cmake` - CMake config files

---

## Environment Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `TRIGGERED_BY` | All stages | Controls which projects rebuild |
| `PACKAGE_VERSION` | All | Version for packages (default: 1.0.0) |
| `CMAKE_PREFIX_PATH` | build.py | Where CMake finds dependencies |
| `CMAKE_INSTALL_PREFIX` | build.py | Where to install built packages |
| `GITLAB_TOKEN` | Registry scripts | Authentication for package upload/download |
| `GITLAB_ACCESS_TOKEN` | Jenkins trigger | GTLabtoken passed to Jenkins |
| `JENKINS_URL` | Jenkins trigger | Jenkins server base URL |
| `JENKINS_USER` | Jenkins trigger | Jenkins username |
| `JENKINS_API_TOKEN` | Jenkins trigger | Jenkins API token (masked) |
| `JENKINS_JOB_NAME` | Jenkins trigger | Job to trigger in Jenkins |

---

## Quick Start Examples

### **Build Only Lasershark (Skip Lasergun)**
```bash
# Via GitLab CI/CD variables
TRIGGERED_BY=lasershark git push origin main

# Or manually at GitLab UI → Run Pipeline
# Set TRIGGERED_BY=lasershark
```

### **Build Specific Version**
```bash
python scripts/py/trigger_config.py write lasershark --version 2.0.0
git add trigger.json
git commit -m "Trigger lasershark v2.0.0"
git push
```

### **Local Build (Development)**
```bash
cd laser_ci
mkdir build && cd build
cmake -DCMAKE_PREFIX_PATH=../install ..
cmake --build . --config Release
```

---

## Troubleshooting

**Pipeline fails at "Download artifacts":**
- Ensure `GITLAB_ACCESS_TOKEN` is set with `read_api` scope
- Check that artifacts were created in the build job

**Jenkins trigger fails:**
- Verify Jenkins is accessible at `JENKINS_URL`
- Check Jenkins credentials are valid
- Ensure GitLab token has `read_api` scope

**Build fails at CMake configure:**
- Ensure dependencies are available in `CMAKE_PREFIX_PATH`
- Run `python scripts/py/download.py <project>` to fetch registry packages
- Check `install/` directory exists and contains expected files

---

## Files Reference

| Path | Purpose |
|------|---------|
| `.gitlab-ci.yml` | Main CI config (includes simplified.yml) |
| `pipelines/.gitlab-ci-simplified.yml` | Actual pipeline definition |
| `pipelines/trigger-template.yml` | Template for external projects triggering laser_ci |
| `CMakeLists.txt` | Final integration build config |
| `scripts/py/` | Python build/trigger orchestration |
| `configs/` | *.ini files, one per project |

---

**Last Updated:** 2026-05-10
**Pipeline Type:** GitLab CI + Jenkins Integration
**Build System:** CMake 3.10+

