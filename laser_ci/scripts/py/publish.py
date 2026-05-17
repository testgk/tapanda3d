#!/usr/bin/env python3
"""Clone, build, and publish a project to the package registry."""

import os
import subprocess
import sys
from pathlib import Path

from project_config import ProjectConfig
from registry import load_config

SCRIPTS_DIR = Path(__file__).parent.parent


def publish(config: ProjectConfig, skip_publish: bool = False) -> None:
    name = config.package.name
    install_dir = config.paths.install_dir
    install_dir.mkdir(parents=True, exist_ok=True)

    # Inject credentials into clone URL
    user = os.environ.get("GIT_FETCH_USER", "")
    token = os.environ.get("GIT_FETCH_TOKEN", "")
    clone_url = config.source.url.replace("https://", f"https://{user}:{token}@")
    source_dir = Path(name)

    # Clone
    print(f"=== Cloning {name} ===")
    clone_cmd = ["git", "clone", clone_url, str(source_dir)]
    if config.source.branch:
        clone_cmd += ["--branch", config.source.branch]
    subprocess.run(clone_cmd, check=True)

    # Build
    print(f"=== Building {name} ===")
    build_dir = source_dir / "build"
    subprocess.run(
        [
            "cmake",
            "-S", str(source_dir),
            "-B", str(build_dir),
            f"-DCMAKE_INSTALL_PREFIX={install_dir}",
            f"-DCMAKE_PREFIX_PATH={install_dir}",
        ],
        check=True,
    )
    subprocess.run(["cmake", "--build", str(build_dir)], check=True)
    subprocess.run(["cmake", "--install", str(build_dir)], check=True)

    # Publish
    if skip_publish:
        print(f"=== Skipping JFrog publish for {name} (--skip-publish) ===")
    else:
        print(f"=== Publishing {name} ===")
        subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "py" / "push_to_jfrog.py"),
                name,
            ],
            check=True,
        )


DEFAULT_PROJECT = "lasershark"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", default=DEFAULT_PROJECT)
    parser.add_argument("--skip-publish", action="store_true")
    args = parser.parse_args()
    try:
        publish(load_config(args.project), skip_publish=args.skip_publish)
    except subprocess.CalledProcessError as e:
        print(f"Publish failed: {e}", file=sys.stderr)
        sys.exit(1)
