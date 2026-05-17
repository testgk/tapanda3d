#!/usr/bin/env python3
"""Trigger a Jenkins job, wait for it to finish, and exit with its result code.

Passes GitLab artifact download details to Jenkins so the job can fetch
the built artifacts directly instead of cloning the repository.

Required CI/CD variables (set as protected/masked in GitLab):
  JENKINS_URL         e.g. https://jenkins.example.com
  JENKINS_USER        Jenkins username
  JENKINS_API_TOKEN   Jenkins API token
  JENKINS_JOB_NAME    e.g. laser-integration-tests
  GITLAB_ACCESS_TOKEN GitLab project/deploy token with read_api scope
                      (used by Jenkins to download artifacts)
"""

import os
import sys
import time
import urllib.request
import urllib.error
import http.cookiejar
import json
from base64 import b64encode
from urllib.parse import urlparse, urlunparse

# Maintain session cookies so the CSRF crumb stays valid across requests
_jar = http.cookiejar.CookieJar()
urllib.request.install_opener(
    urllib.request.build_opener( urllib.request.HTTPCookieProcessor( _jar ) )
)


def env(key: str) -> str:
    val = os.environ.get(key, "").strip()
    if not val:
        print(f"ERROR: required environment variable {key} is not set", file=sys.stderr)
        sys.exit(1)
    return val


def _rebase(url: str, base_url: str) -> str:
    """Replace the host:port in url with the one from base_url, keeping the path."""
    p = urlparse(url)
    b = urlparse(base_url)
    return urlunparse(p._replace(scheme=b.scheme, netloc=b.netloc))


def get_crumb(base_url: str, user: str, token: str) -> dict:
    """Fetch a CSRF crumb from Jenkins. Returns empty dict if CSRF is disabled."""
    status, body, _ = make_request(f"{base_url}/crumbIssuer/api/json", user, token)
    if status == 200:
        data = json.loads(body)
        return {data["crumbRequestField"]: data["crumb"]}
    return {}


def make_request(url: str, user: str, token: str, method: str = "GET", data: bytes | None = None, extra_headers: dict | None = None):
    credentials = b64encode(f"{user}:{token}".encode()).decode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Basic {credentials}")
    if data is not None:
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    for k, v in (extra_headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, resp.read().decode(), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), {}


def build_artifact_url() -> str:
    """Build the GitLab API URL to download this job's artifacts zip."""
    server  = os.environ.get("CI_SERVER_URL", "").rstrip("/")
    project = os.environ.get("CI_PROJECT_ID", "")
    job_id  = os.environ.get("CI_JOB_ID", "")
    if not (server and project and job_id):
        print("ERROR: CI_SERVER_URL, CI_PROJECT_ID, CI_JOB_ID must be set", file=sys.stderr)
        sys.exit(1)
    return f"{server}/api/v4/projects/{project}/jobs/{job_id}/artifacts"


def trigger_job(base_url: str, job: str, user: str, token: str, params: dict) -> str:
    crumb = get_crumb(base_url, user, token)
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}/job/{job}/buildWithParameters?{query}"

    status, _, headers = make_request(url, user, token, method="POST", data=b"", extra_headers=crumb)
    if status not in (200, 201):
        print(f"ERROR: failed to trigger Jenkins job (HTTP {status})", file=sys.stderr)
        sys.exit(1)

    queue_url = headers.get("Location", "")
    if not queue_url:
        print("ERROR: Jenkins did not return a queue location header", file=sys.stderr)
        sys.exit(1)

    return queue_url.rstrip("/")


def wait_for_queue(queue_url: str, user: str, token: str, poll: int = 3) -> int:
    print(f"Queued: {queue_url}")
    while True:
        status, body, _ = make_request(f"{queue_url}/api/json", user, token)
        if status != 200:
            print(f"ERROR: queue poll failed (HTTP {status})", file=sys.stderr)
            sys.exit(1)
        data = json.loads(body)
        executable = data.get( "executable" )
        if executable is not None:
            build_number = executable[ "number" ]
            print( f"Build started: #{build_number}" )
            return build_number
        if data.get("cancelled"):
            print("ERROR: Jenkins build was cancelled", file=sys.stderr)
            sys.exit(1)
        time.sleep(poll)


def wait_for_build(base_url: str, job: str, build_number: int, user: str, token: str, poll: int = 5) -> str:
    build_url = f"{base_url}/job/{job}/{build_number}"
    print(f"Watching: {build_url}")
    while True:
        status, body, _ = make_request(f"{build_url}/api/json", user, token)
        if status != 200:
            print(f"ERROR: build poll failed (HTTP {status})", file=sys.stderr)
            sys.exit(1)
        data = json.loads(body)
        if not data.get("building") and data.get("result"):
            return data["result"]
        elapsed = data.get("duration", 0) // 1000
        print(f"  still running... ({elapsed}s elapsed)")
        time.sleep(poll)


def main() -> int:
    base_url     = env("JENKINS_URL").rstrip("/")
    public_url   = os.environ.get("JENKINS_PUBLIC_URL", base_url).rstrip("/")
    user         = env("JENKINS_USER")
    token        = env("JENKINS_API_TOKEN")
    job          = env("JENKINS_JOB_NAME")
    gitlab_token = env("GITLAB_ACCESS_TOKEN")

    artifact_url = build_artifact_url()

    params = {
        # Jenkins fetches the artifacts zip from GitLab using these
        "GITLAB_ARTIFACT_URL":   artifact_url,
        "GITLAB_ACCESS_TOKEN":   gitlab_token,
        # Traceability
        "GITLAB_PIPELINE_ID":    os.environ.get("CI_PIPELINE_ID", ""),
        "GITLAB_PROJECT_NAME":   os.environ.get("CI_PROJECT_NAME", ""),
        "TRIGGERED_BY":          os.environ.get("TRIGGERED_BY", ""),
        # Additional sync parameters
        "GITLAB_COMMIT_SHA":     os.environ.get("CI_COMMIT_SHA", ""),
        "GITLAB_BRANCH":         os.environ.get("CI_COMMIT_BRANCH", os.environ.get("CI_COMMIT_REF_NAME", "")),
    }
    # Remove empty values
    params = {k: v for k, v in params.items() if v}

    print(f"Triggering Jenkins job: {job}")
    print(f"  Artifact URL: {artifact_url}")

    queue_url    = trigger_job(base_url, job, user, token, params)
    build_number = wait_for_queue(_rebase(queue_url, base_url), user, token)
    result       = wait_for_build(base_url, job, build_number, user, token)

    build_url = f"{public_url}/job/{job}/{build_number}"
    print(f"\nJenkins result: {result}")
    print(f"Build URL:      {build_url}")

    return 0 if result == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
