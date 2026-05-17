#!/usr/bin/env python3
"""Push already-built artifacts from install/ to the package registry."""

import sys

from publish_to_registry import publish_package
from registry import load_config


def push_to_registry(config) -> None:
    publish_package(
        config.package.name,
        config.package.id,
        config.package.version,
        config.paths.install_dir,
    )


DEFAULT_PROJECT = "lasershark"

if __name__ == "__main__":
    project = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else DEFAULT_PROJECT
    try:
        push_to_registry(load_config(project))
    except RuntimeError as e:
        print(f"Push to registry failed: {e}", file=sys.stderr)
        sys.exit(1)
