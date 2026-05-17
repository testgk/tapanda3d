#!/usr/bin/env python3
"""Download all dependencies declared in a project config from the registry."""

import sys

from download_registry import download_package
from registry import load_config


def download(config) -> None:
    for dep_name, dep_id in config.dependencies.items():
        download_package(dep_name, dep_id, config.package.version, config.paths.install_dir)


DEFAULT_PROJECT = "lasershark"

if __name__ == "__main__":
    project = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else DEFAULT_PROJECT
    download(load_config(project))