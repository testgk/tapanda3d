#!/usr/bin/env python3
"""Python implementation of build.sh — configures, builds, and installs laserproject."""

import subprocess
import sys

from project_config import ProjectConfig
from registry import load_config


def build(config: ProjectConfig) -> None:
    paths = config.paths
    print(f"Building {config.package.name}...")
    print(f"  Build directory:   {paths.build_dir}")
    print(f"  Install directory: {paths.install_dir}")

    paths.build_dir.mkdir(parents=True, exist_ok=True)

    print("\nConfiguring CMake...")
    subprocess.run(
        [
            "cmake",
            f"-DCMAKE_PREFIX_PATH={paths.install_dir}",
            f"-DCMAKE_INSTALL_PREFIX={paths.install_dir}",
            "-S", str(paths.repo_root),
            "-B", str(paths.build_dir),
        ],
        check=True,
    )

    print("Building...")
    subprocess.run(["cmake", "--build", str(paths.build_dir)], check=True)

    print("Installing...")
    subprocess.run(["cmake", "--install", str(paths.build_dir)], check=True)

    print(f"\nBuild complete! Artifacts installed to: {paths.install_dir}")


if __name__ == "__main__":
    DEFAULT_PROJECT = "lasershark"
    project = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else DEFAULT_PROJECT
    try:
        build(load_config(project))
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)