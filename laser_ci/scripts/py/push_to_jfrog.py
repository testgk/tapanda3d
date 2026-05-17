#!/usr/bin/env python3
"""Push already-built artifacts from install/ to JFrog Artifactory."""

import sys
import argparse

from publish_to_jfrog import publish_package
from registry import load_config


def push_to_jfrog(config) -> None:
    """Push package to JFrog Artifactory."""
    publish_package(
        config.package.name,
        config.package.id,
        config.package.version,
        config.paths.install_dir,
    )


DEFAULT_PROJECT = "lasershark"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push artifacts to JFrog Artifactory")
    parser.add_argument("project", nargs="?", default=DEFAULT_PROJECT,
                       help=f"Project to push (default: {DEFAULT_PROJECT})")
    args = parser.parse_args()

    try:
        push_to_jfrog(load_config(args.project))
    except RuntimeError as e:
        print(f"Push to JFrog failed: {e}", file=sys.stderr)
        sys.exit(1)
