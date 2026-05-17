#!/usr/bin/env python3
"""
Jenkins Setup Script for Laser CI Integration
=============================================

This script configures Jenkins to work with GitLab CI/CD pipelines.
It creates the necessary jobs and sets up the integration.

Usage:
    python setup_jenkins.py [options]

Options:
    --jenkins-url URL       Jenkins server URL (default: http://localhost:8080)
    --jenkins-user USER     Jenkins username (default: admin)
    --jenkins-token TOKEN   Jenkins API token
    --gitlab-token TOKEN    GitLab access token
    --create-job           Create/update the laser-integration-tests job
    --test-connection      Test Jenkins connection
    --help                 Show this help message
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from base64 import b64encode

class JenkinsSetup:
    def __init__(self, jenkins_url, jenkins_user, jenkins_token):
        self.jenkins_url = jenkins_url.rstrip('/')
        self.jenkins_user = jenkins_user
        self.jenkins_token = jenkins_token
        self.auth_header = self._get_auth_header()

    def _get_auth_header(self):
        credentials = b64encode(f"{self.jenkins_user}:{self.jenkins_token}".encode()).decode()
        return f"Basic {credentials}"

    def _make_request(self, url, method="GET", data=None):
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", self.auth_header)
        if data:
            req.add_header("Content-Type", "application/xml")

        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, resp.read().decode(), dict(resp.headers)
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode(), {}

    def test_connection(self):
        """Test connection to Jenkins server"""
        print(f"Testing connection to Jenkins at {self.jenkins_url}...")
        status, body, headers = self._make_request(f"{self.jenkins_url}/api/json")

        if status == 200:
            data = json.loads(body)
            print("✅ Jenkins connection successful!")
            print(f"   Jenkins version: {data.get('version', 'unknown')}")
            print(f"   Server: {data.get('server', 'unknown')}")
            return True
        else:
            print(f"❌ Jenkins connection failed (HTTP {status})")
            print(f"   Response: {body}")
            return False

    def job_exists(self, job_name):
        """Check if a Jenkins job exists"""
        status, _, _ = self._make_request(f"{self.jenkins_url}/job/{job_name}/api/json")
        return status == 200

    def create_or_update_job(self, job_name, config_xml):
        """Create or update a Jenkins job"""
        print(f"Creating/updating Jenkins job: {job_name}")

        # Check if job exists
        exists = self.job_exists(job_name)

        if exists:
            print(f"   Job '{job_name}' exists, updating...")
            url = f"{self.jenkins_url}/job/{job_name}/config.xml"
            method = "POST"
        else:
            print(f"   Job '{job_name}' does not exist, creating...")
            url = f"{self.jenkins_url}/createItem?name={job_name}"
            method = "POST"

        status, body, headers = self._make_request(url, method=method, data=config_xml.encode())

        if status in [200, 201]:
            print(f"✅ Job '{job_name}' {'updated' if exists else 'created'} successfully!")
            return True
        else:
            print(f"❌ Failed to {'update' if exists else 'create'} job '{job_name}' (HTTP {status})")
            print(f"   Response: {body}")
            return False

    def trigger_job(self, job_name, parameters=None):
        """Trigger a Jenkins job with optional parameters"""
        print(f"Triggering Jenkins job: {job_name}")

        url = f"{self.jenkins_url}/job/{job_name}/build"
        if parameters:
            param_str = "&".join(f"{k}={v}" for k, v in parameters.items())
            url += f"WithParameters?{param_str}"

        status, body, headers = self._make_request(url, method="POST")

        if status in [200, 201]:
            print(f"✅ Job '{job_name}' triggered successfully!")
            queue_url = headers.get("Location", "")
            if queue_url:
                print(f"   Queue URL: {queue_url}")
            return True
        else:
            print(f"❌ Failed to trigger job '{job_name}' (HTTP {status})")
            print(f"   Response: {body}")
            return False

    def get_job_status(self, job_name, build_number=None):
        """Get status of a Jenkins job"""
        if build_number:
            url = f"{self.jenkins_url}/job/{job_name}/{build_number}/api/json"
        else:
            url = f"{self.jenkins_url}/job/{job_name}/api/json"

        status, body, headers = self._make_request(url)

        if status == 200:
            data = json.loads(body)
            if build_number:
                return {
                    'building': data.get('building', False),
                    'result': data.get('result'),
                    'duration': data.get('duration', 0),
                    'timestamp': data.get('timestamp', 0)
                }
            else:
                last_build = data.get('lastBuild', {})
                return {
                    'last_build_number': last_build.get('number'),
                    'last_build_url': last_build.get('url')
                }
        else:
            print(f"❌ Failed to get job status (HTTP {status})")
            return None


def load_job_config():
    """Load the Jenkins job configuration XML"""
    config_path = Path(__file__).parent / "docker" / "jenkins" / "jenkins-job-config.xml"
    if not config_path.exists():
        print(f"❌ Jenkins job config not found: {config_path}")
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(description="Jenkins Setup for Laser CI Integration")
    parser.add_argument("--jenkins-url", default="http://localhost:8080",
                       help="Jenkins server URL")
    parser.add_argument("--jenkins-user", default="admin",
                       help="Jenkins username")
    parser.add_argument("--jenkins-token", required=True,
                       help="Jenkins API token")
    parser.add_argument("--gitlab-token",
                       help="GitLab access token (for testing)")
    parser.add_argument("--create-job", action="store_true",
                       help="Create/update the laser-integration-tests job")
    parser.add_argument("--test-connection", action="store_true",
                       help="Test Jenkins connection")
    parser.add_argument("--trigger-test", action="store_true",
                       help="Trigger a test job run")

    args = parser.parse_args()

    if not any([args.test_connection, args.create_job, args.trigger_test]):
        parser.print_help()
        return 1

    # Initialize Jenkins setup
    jenkins = JenkinsSetup(args.jenkins_url, args.jenkins_user, args.jenkins_token)

    # Test connection
    if args.test_connection:
        if not jenkins.test_connection():
            return 1

    # Create/update job
    if args.create_job:
        config_xml = load_job_config()
        if config_xml:
            if not jenkins.create_or_update_job("laser-integration-tests", config_xml):
                return 1
        else:
            return 1

    # Trigger test job
    if args.trigger_test:
        test_params = {}
        if args.gitlab_token:
            test_params = {
                "GITLAB_ARTIFACT_URL": "https://gitlab.com/api/v4/projects/12345/jobs/67890/artifacts",
                "GITLAB_ACCESS_TOKEN": args.gitlab_token,
                "GITLAB_PIPELINE_ID": "test-pipeline",
                "GITLAB_PROJECT_NAME": "laser_ci",
                "TRIGGERED_BY": "test"
            }

        if not jenkins.trigger_job("laser-integration-tests", test_params):
            return 1

    print("\n🎉 Jenkins setup completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

