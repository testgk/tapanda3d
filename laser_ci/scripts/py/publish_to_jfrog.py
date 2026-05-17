#!/usr/bin/env python3
"""Upload built artifacts from install/ to JFrog Artifactory."""

import os
import urllib.error
import urllib.request
from pathlib import Path

from jfrog_config import JFrogConfig

# JFrog Artifactory configuration
jfrog_config = JFrogConfig.from_env()


def _auth_header() -> tuple[str, str]:
    """Get authentication header for JFrog."""
    return jfrog_config.get_auth_header()


def _upload(url: str, data: bytes) -> None:
    """Upload data to JFrog Artifactory."""
    name, value = _auth_header()
    req = urllib.request.Request(url, data=data, method="PUT", headers={name: value})
    req.add_header("Content-Type", "application/octet-stream")

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"Unexpected status {resp.status} uploading {url}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Upload failed ({e.code}): {url}") from e


def publish_package(name: str, project_id: str, version: str, install_dir: Path) -> None:
    """Publish package artifacts to JFrog Artifactory."""
    install_dir = Path(install_dir)
    base = f"{jfrog_config.url}/artifactory/{jfrog_config.repo}/{name}/{version}"

    print(f"=== Publishing {name} v{version} to JFrog ===")

    # Libraries
    lib_dir = install_dir / "lib"
    for ext in ("a", "so", "lib"):
        pattern = f"lib{name}.{ext}" if ext != "lib" else f"{name}.lib"
        path = lib_dir / pattern
        if path.exists():
            _upload(f"{base}/{pattern}", path.read_bytes())
            print(f"  {pattern}")

    # Headers
    include_dir = install_dir / "include" / name
    if include_dir.is_dir():
        for path in sorted(include_dir.glob("*.h")):
            _upload(f"{base}/{path.name}", path.read_bytes())
            print(f"  {path.name}")

    # CMake config files
    cmake_dir = lib_dir / "cmake" / name
    if cmake_dir.is_dir():
        for path in sorted(cmake_dir.glob("*.cmake")):
            _upload(f"{base}/{path.name}", path.read_bytes())
            print(f"  {path.name}")

    print(f"=== done: {name} ===\n")
