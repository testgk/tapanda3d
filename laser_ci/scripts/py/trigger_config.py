#!/usr/bin/env python3
"""Option 3: artifact-based config passing between pipelines.

A remote project generates a trigger.json artifact before triggering laser_ci.
laser_ci downloads it as a dependency artifact and loads it here, merging its
fields over the base ini config.

Remote project usage (in their CI job):
    script:
      - python3 path/to/trigger_config.py write lasershark --version 1.2.0 --branch feature/foo
    artifacts:
      paths:
        - trigger.json

laser_ci usage (build_final job):
    needs:
      - project: aqualaser/lasershark
        job: prepare_trigger
        artifacts: true
    script:
      - python3 scripts/py/download.py $TRIGGERED_BY
      - python3 scripts/py/build.py $TRIGGERED_BY

The scripts automatically pick up trigger.json when present via load_trigger_config().
"""

import json
import sys
from pathlib import Path

from project_config import ProjectConfig
from registry import load_config

TRIGGER_FILE = Path("trigger.json")


def write_trigger_file(project: str, overrides: dict, path: Path = TRIGGER_FILE) -> None:
    """Write a trigger.json artifact to be consumed by laser_ci."""
    payload = {"project": project, **overrides}
    path.write_text(json.dumps(payload, indent=2))
    print(f"Written trigger config to {path}:\n{json.dumps(payload, indent=2)}")


def load_trigger_config(path: Path = TRIGGER_FILE) -> ProjectConfig | None:
    """Load config from a trigger.json artifact if present.

    Supports two payload shapes:
      - Full ini:   {"project": "lasergun", "config": {<all ini sections>}}
      - Overrides:  {"project": "lasergun", "version": "1.2.0", "branch": "feat"}

    Returns None if no trigger file exists (fall back to TRIGGERED_BY / default).
    """
    if not path.exists():
        return None
    payload = json.loads(path.read_text())
    project = payload.pop("project")

    # Full ini payload — build overrides from the config sections
    if "config" in payload:
        ini = payload["config"]
        overrides = {}
        if "package" in ini and "version" in ini["package"]:
            overrides["version"] = ini["package"]["version"]
        if "source" in ini and ini["source"].get("branch"):
            overrides["branch"] = ini["source"]["branch"]
        if "paths" in ini:
            for key in ("install_dir", "build_dir", "repo_root"):
                if ini["paths"].get(key):
                    overrides[key] = ini["paths"][key]
        payload = overrides

    config = load_config(project)
    if payload:
        print(f"Applying trigger.json overrides: {payload}")
        config = config.apply_overrides(payload)
    return config


if __name__ == "__main__":
    # CLI helper for remote projects to generate trigger.json
    # Usage: trigger_config.py write <project> [--version X] [--branch Y] [--install_dir Z]
    import argparse

    parser = argparse.ArgumentParser(description="Write a trigger.json for laser_ci")
    parser.add_argument("action", choices=["write"])
    parser.add_argument("project", help="Project name (e.g. lasershark)")
    parser.add_argument("--version")
    parser.add_argument("--branch")
    parser.add_argument("--install_dir")
    parser.add_argument("--build_dir")
    parser.add_argument("--output", default=str(TRIGGER_FILE))
    args = parser.parse_args()

    overrides = {k: v for k, v in vars(args).items()
                 if k not in ("action", "project", "output") and v is not None}
    write_trigger_file(args.project, overrides, Path(args.output))
