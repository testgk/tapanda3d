#!/usr/bin/env python3
"""
Laser CI Pipeline Trigger Examples
===================================

This script demonstrates the three ways to trigger the laser_ci pipeline:
1. GitLab CI/CD (automatic or manual)
2. Trigger configuration (cross-project)
3. Jenkins integration
"""

import json
from pathlib import Path
from datetime import datetime

def example_1_gitlab_ci():
    """Method 1: GitLab CI/CD Trigger (Simplest)"""
    print("┌" + "─" * 78 + "┐")
    print("│ METHOD 1: GitLab CI/CD (Automatic on git push)".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    print("📌 AUTOMATIC: Push to main branch")
    print("   $ git push origin main")
    print()

    print("   Result: Full pipeline runs automatically")
    print("   - build_lasergun")
    print("   - build_lasershark")
    print("   - integration_tests (Jenkins)")
    print("   - deploy_lasergun & deploy_lasershark")
    print()

    print("📌 MANUAL: Via GitLab UI")
    print("   1. Go to: CI/CD → Pipelines")
    print("   2. Click: 'Run pipeline'")
    print("   3. (Optional) Set variables:")
    print("      • TRIGGERED_BY=lasershark (skip lasergun rebuild)")
    print("      • PACKAGE_VERSION=1.1.0")
    print()


def example_2_trigger_config():
    """Method 2: Trigger Configuration (Cross-Project)"""
    print("┌" + "─" * 78 + "┐")
    print("│ METHOD 2: Trigger Configuration (Cross-Project)".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    print("🔧 SETUP: Create trigger.json in laser_ci")
    print()
    print("   Command:")
    print("   $ python scripts/py/trigger_config.py write lasershark \\")
    print("       --version 1.1.0 \\")
    print("       --branch feature/new-laser")
    print()

    print("   Generated trigger.json:")
    config = {
        "project": "lasershark",
        "version": "1.1.0",
        "branch": "feature/new-laser"
    }
    print("   " + json.dumps(config, indent=2).replace("\n", "\n   "))
    print()

    print("   In laser_ci/.gitlab-ci.yml, another project adds:")
    print("   ```yaml")
    print("   build_lasershark:")
    print("     needs:")
    print("       - project: aqualaser/lasershark")
    print("         job: prepare_trigger")
    print("         artifacts: true  # downloads trigger.json")
    print("   ```")
    print()

    print("   Result:")
    print("   - laser_ci automatically picks up trigger.json")
    print("   - Uses version 1.1.0 and feature/new-laser branch")
    print("   - Rebuilds with overridden configuration")
    print()


def example_3_jenkins_trigger():
    """Method 3: Jenkins Integration"""
    print("┌" + "─" * 78 + "┐")
    print("│ METHOD 3: Jenkins Integration Trigger".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    print("⚙️  PREREQUISITES: Set these as GitLab CI/CD variables (protected/masked)")
    print()
    print("   JENKINS_URL = https://jenkins.example.com")
    print("   JENKINS_USER = admin")
    print("   JENKINS_API_TOKEN = <your-token>  (masked)")
    print("   GITLAB_ACCESS_TOKEN = glpat-xxxxx (masked, with read_api scope)")
    print("   JENKINS_JOB_NAME = laser-integration-tests")
    print()

    print("🚀 TRIGGER: In integration_tests job")
    print()
    print("   # Get the build job ID that has our artifacts")
    print("   BUILD_JOB_ID=$(curl -sf \\")
    print("     --header \"PRIVATE-TOKEN: $GITLAB_ACCESS_TOKEN\" \\")
    print("     \"$CI_SERVER_URL/api/v4/projects/$CI_PROJECT_ID/\" \\")
    print("     \"pipelines/$CI_PIPELINE_ID/jobs\" | \\")
    print("     python3 -c \"import sys,json; jobs=json.load(sys.stdin);\")")
    print()
    print("   # Trigger Jenkins with artifact details")
    print("   CI_JOB_ID=$BUILD_JOB_ID python3 scripts/py/trigger_jenkins.py")
    print()

    print("   What happens:")
    print("   1. Script builds artifact download URL from GitLab")
    print("   2. Triggers Jenkins job: POST /job/{name}/buildWithParameters")
    print("   3. Passes parameters:")
    print("      - GITLAB_ARTIFACT_URL (where Jenkins downloads)")
    print("      - GITLAB_ACCESS_TOKEN (Jenkins auth)")
    print("      - GITLAB_PIPELINE_ID (traceability)")
    print("   4. Polls Jenkins every 5 seconds")
    print("   5. Returns exit code: 0=SUCCESS, 1=FAILURE")
    print()


def example_pipeline_logic():
    """Show pipeline execution logic based on TRIGGERED_BY"""
    print("┌" + "─" * 78 + "┐")
    print("│ PIPELINE LOGIC BY TRIGGERED_BY VARIABLE".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    scenarios = [
        {
            "scenario": "TRIGGERED_BY not set (default)",
            "builds": [
                "✅ build_lasergun",
                "✅ build_lasershark (depends on lasergun)",
                "✅ integration_tests",
                "✅ deploy_lasergun & deploy_lasershark"
            ],
            "use_case": "Full pipeline rebuild"
        },
        {
            "scenario": "TRIGGERED_BY=lasergun",
            "builds": [
                "✅ build_lasergun",
                "✅ build_lasershark",
                "✅ integration_tests",
                "✅ deploy_lasergun & deploy_lasershark"
            ],
            "use_case": "Lasergun changed → rebuild lasershark too"
        },
        {
            "scenario": "TRIGGERED_BY=lasershark",
            "builds": [
                "⏭️  build_lasergun (skip, use registry)",
                "✅ build_lasershark",
                "✅ integration_tests",
                "⏭️  deploy_lasergun (skip)",
                "✅ deploy_lasershark"
            ],
            "use_case": "Only lasershark changed → skip lasergun"
        }
    ]

    for scenario in scenarios:
        print(f"📋 {scenario['scenario']}")
        print(f"   Use Case: {scenario['use_case']}")
        print(f"   Builds:")
        for build in scenario['builds']:
            print(f"     {build}")
        print()


def example_configuration_files():
    """Show the configuration files structure"""
    print("┌" + "─" * 78 + "┐")
    print("│ CONFIGURATION FILES".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    print("📁 configs/lasershark.ini")
    print("   ├─ [package] name=lasershark, id=77866232, version=1.0.0")
    print("   ├─ [dependencies] lasergun=77866175")
    print("   ├─ [source] url=https://gitlab.com/aqualaser/lasershark.git")
    print("   ├─ [registry] url=https://gitlab.com/api/v4/projects")
    print("   └─ [paths] repo_root=.., build_dir=../build, install_dir=../install")
    print()

    print("📁 configs/lasergun.ini")
    print("   ├─ [package] name=lasergun, id=77866175, version=1.0.0")
    print("   ├─ [source] url=https://gitlab.com/aqualaser/lasergun.git")
    print("   ├─ [registry] url=https://gitlab.com/api/v4/projects")
    print("   └─ [paths] repo_root=.., build_dir=../build, install_dir=../install")
    print()

    print("📄 .gitlab-ci.yml → includes pipelines/.gitlab-ci-simplified.yml")
    print()


def example_quick_start():
    """Quick start commands"""
    print("┌" + "─" * 78 + "┐")
    print("│ QUICK START COMMANDS".ljust(79) + "│")
    print("└" + "─" * 78 + "┘")
    print()

    print("🚀 Trigger full pipeline (rebuilds everything)")
    print("   $ cd laser_ci")
    print("   $ git push origin main")
    print()

    print("🚀 Trigger only lasershark rebuild (skip lasergun)")
    print("   $ python scripts/py/trigger_config.py write lasershark --version 1.1.0")
    print("   $ git add trigger.json")
    print("   $ git commit -m 'Rebuild lasershark v1.1.0'")
    print("   $ git push origin main")
    print()

    print("🚀 Create trigger config to pass to another project")
    print("   $ python scripts/py/trigger_config.py write lasershark \\")
    print("       --version 2.0.0 --branch dev --output trigger.json")
    print()

    print("🚀 Verify pipeline logs")
    print("   • GitLab: CI/CD → Pipelines → click pipeline")
    print("   • Jenkins: Navigate to laser-integration-tests job")
    print()


def main():
    print()
    print("=" * 80)
    print(" LASER CI - PIPELINE TRIGGER GUIDE & EXAMPLES")
    print("=" * 80)
    print()

    example_1_gitlab_ci()
    print()
    example_2_trigger_config()
    print()
    example_3_jenkins_trigger()
    print()
    example_pipeline_logic()
    print()
    example_configuration_files()
    print()
    example_quick_start()

    print("=" * 80)
    print(" For more details, see PIPELINE_TRIGGER_GUIDE.md")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()


