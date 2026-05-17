📌 LASER CI - QUICK REFERENCE CARD
═════════════════════════════───═════════════════════════════════════════════════

🚀 TO TRIGGER A PIPELINE - THREE METHODS:
───────────────────────────────────────────────────────────────────────────────

1️⃣  SIMPLEST: Just push to main
    $ git push origin main
    ✅ Full pipeline: build → integrate → deploy

2️⃣  WITH CONFIG: Create trigger.json for specific version
    $ python scripts/py/trigger_config.py write lasershark --version 1.1.0
    $ git add trigger.json
    $ git push origin main
    ✅ Rebuild with version 1.1.0, skip lasergun if unchanged

3️⃣  MANUAL: Run from GitLab UI
    Go to: https://gitlab.com/aqualaser/laser_ci/-/pipelines
    Click: "Run pipeline"
    Set: TRIGGERED_BY=lasershark (optional)
    ✅ Pipeline runs immediately


📂 KEY FILES & FOLDERS:
───────────────────────────────────────────────────────────────────────────────

Pipeline Configuration:
  └─ .gitlab-ci.yml
     ���─ includes: pipelines/.gitlab-ci-simplified.yml
                  ├─ build_lasergun (Stage 1)
                  ├─ build_lasershark (Stage 1)
                  ├─ integration_tests (Stage 2 - calls Jenkins)
                  ├─ deploy_lasergun (Stage 3)
                  └─ deploy_lasershark (Stage 3)

Project Configs:
  └─ configs/
     ├─ lasergun.ini (Project ID: 77866175, v1.0.0)
     └─ lasershark.ini (Project ID: 77866232, v1.0.0)

Build Scripts:
  └─ scripts/py/
     ├─ build.py ..................... CMake build
     ├─ download.py .................. From registry
     ├─ publish.py ................... Build & publish
     ├─ push_to_registry.py .......... Upload artifacts
     ├─ trigger_config.py ........... Create trigger.json ⭐ USE ME
     └─ trigger_jenkins.py .......... Trigger Jenkins


🔀 PIPELINE LOGIC (Based on TRIGGERED_BY variable):
───────────────────────────────────────────────────────────────────────────────

TRIGGERED_BY=null (default, push to main):
  ✅ build_lasergun → ✅ build_lasershark → ✅ integration_tests
  └─ ✅ deploy_lasergun, deploy_lasershark

TRIGGERED_BY=lasergun:
  ✅ build_lasergun → ✅ build_lasershark → ✅ integration_tests
  └─ ✅ deploy_lasergun, deploy_lasershark

TRIGGERED_BY=lasershark:
  ⏭️  skip build_lasergun (use registry)
  ✅ build_lasershark → ✅ integration_tests
  └─ ✅ deploy_lasershark (skip deploy_lasergun)


⚙️  ENVIRONMENT VARIABLES:
───────────────────────────────────────────────────────────────────────────────

GitLab CI/CD:
  • TRIGGERED_BY .............. Project that triggered this (lasergun/lasershark)
  • PACKAGE_VERSION ........... Version string (default: 1.0.0)
  • CMAKE_PREFIX_PATH ......... Where to find dependencies
  • CMAKE_INSTALL_PREFIX ...... Where to install artifacts

Jenkins Integration (if used):
  • JENKINS_URL ............... Jenkins server URL
  • JENKINS_PUBLIC_URL ........ Public Jenkins URL (optional)
  • JENKINS_USER .............. Jenkins username
  • JENKINS_API_TOKEN ......... Jenkins auth token (masked)
  • GITLAB_ACCESS_TOKEN ....... GitLab token for artifact download
  • JENKINS_JOB_NAME .......... Job to trigger


📋 COMMON COMMANDS:
───────────────────────────────────────────────────────────────────────────────

Full rebuild (everything):
  $ git push origin main

Rebuild lasershark v2.0.0:
  $ python scripts/py/trigger_config.py write lasershark --version 2.0.0
  $ git add trigger.json
  $ git commit -m "Rebuild lasershark 2.0.0"
  $ git push origin main

Create trigger config for another project:
  $ python scripts/py/trigger_config.py write lasershark \
      --version 2.1.0 --branch feature/new-laser --output trigger.json

Verify trigger.json content:
  $ cat trigger.json

View pipeline:
  $ git log --oneline -1  # Get commit hash
  # Then go to GitLab CI/CD → Pipelines


🔍 REGISTRY PACKAGES:
───────────────────────────────────────────────────────────────────────────────

LaserGun Package Registry:
  https://gitlab.com/api/v4/projects/77866175/packages/generic/lasergun/1.0.0/
  Files: liblasergun.a, liblasergun.so, LaserGun.h, *Config.cmake

LaserShark Package Registry:
  https://gitlab.com/api/v4/projects/77866232/packages/generic/lasershark/1.0.0/
  Files: liblasershark.so, lasershark/*.h, *Config.cmake


✅ BUILD STAGES EXPLAINED:
───────────────────────────────────────────────────────────────────────────────

Stage 1: BUILD
  • Clones source repository
  • Runs: cmake -DCMAKE_PREFIX_PATH=install ..
  • Runs: cmake --build . --config Release
  • Installs artifacts to install/ directory
  • Creates pipeline artifacts

Stage 2: INTEGRATE
  • Downloads all packages from registry
  • Runs: cmake -DCMAKE_PREFIX_PATH=install ..
  • Runs integration tests
  • Calls Jenkins with GITLAB_ARTIFACT_URL parameter
  • Jenkins downloads artifacts and runs hardware tests

Stage 3: DEPLOY
  • Only runs if integration passed
  • Uploads install/ directory to GitLab Package Registry
  • Packages are now available for other projects


📖 DOCUMENTATION REFERENCES:
───────────────────────────────────────────────────────────────────────────────

Created Files (in docs/):
  ✅ PIPELINE_TRIGGER_GUIDE.md ......... Full comprehensive guide
  ✅ QUICK_REFERENCE.md ............... This file
  ✅ trigger_examples.py .............. Interactive examples with output
  ✅ TRIGGER_EXAMPLE.json ............ Sample trigger configuration

Original Docs:
  📄 README.md ............................. Project overview
  📄 docs/REGISTRY_INTEGRATION.md ........ Package registry setup
  📄 docs/PACKAGE_MANAGEMENT.md ......... Package management
  📄 docs/DEMO.md ....................... Demo walkthrough


🎯 NEXT STEPS:
───────────────────────────────────────────────────────────────────────────────

1. Understand pipeline stages:
   → Read pipelines/.gitlab-ci-simplified.yml

2. Try basic trigger:
   → git push origin main

3. Try configuration trigger:
   → python scripts/py/trigger_config.py write lasershark --version X.Y.Z

4. Set up Jenkins integration (optional):
   → GitLab Settings → CI/CD → Variables
   → Add: JENKINS_URL, JENKINS_USER, JENKINS_API_TOKEN, etc.

5. Monitor runs:
   → GitLab: CI/CD → Pipelines
   → Jenkins: <JENKINS_URL>/job/laser-integration-tests


💡 TIPS & TRICKS:
───────────────────────────────────────────────────────────────────────────────

• Trigger.json is picked up automatically by load_trigger_config()
• TRIGGERED_BY variable controls which projects rebuild
• Pre-built packages cached in registry for faster builds
• Each pipeline has 30 days artifact retention (integration stage)
• Build artifacts expire after 1 day (build stage)
• Jenkins integration optional—can skip if not needed


⚠️  COMMON ISSUES:
───────────────────────────────────────────────────────────────────────────────

Pipeline fails at "Download artifacts":
  → Check GITLAB_ACCESS_TOKEN has read_api scope
  → Verify build_lasershark job succeeded first

CMake configure fails:
  → Check $CMAKE_PREFIX_PATH contains install/ directory
  → Run: python scripts/py/download.py lasershark

Jenkins trigger fails:
  → Verify JENKINS_URL is accessible
  → Check JENKINS_API_TOKEN is valid and not expired
  → Ensure GITLAB_ACCESS_TOKEN has read_api scope

Artifact not found in registry:
  → Check deploy job ran successfully
  → Verify GITLAB_TOKEN/GITLAB_ACCESS_TOKEN is set
  → Check project IDs in configs/*.ini


═══════════════════════════════════════════════════════════════════════════════
Generated: 2026-05-10
Status: ✅ Pipeline Ready to Trigger
══════════════════════════════════���════════════════════════════════════════════


