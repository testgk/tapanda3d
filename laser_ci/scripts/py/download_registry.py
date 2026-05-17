#!/usr/bin/env python3
"""Python replacement for download-from-registry.sh."""

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

GITLAB_API = "https://gitlab.com/api/v4"


def _auth_header() -> tuple[str, str]:
    if os.environ.get("GITLAB_TOKEN"):
        return ("PRIVATE-TOKEN", os.environ["GITLAB_TOKEN"])
    if os.environ.get("CI_JOB_TOKEN"):
        return ("JOB-TOKEN", os.environ["CI_JOB_TOKEN"])
    raise RuntimeError("No token available — set GITLAB_TOKEN or run in CI")


def _get(url: str) -> bytes | None:
    name, value = _auth_header()
    req = urllib.request.Request(url, headers={name: value})
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.read()
    except urllib.error.HTTPError:
        return None


def _get_json(url: str) -> object:
    data = _get(url)
    if data is None:
        raise RuntimeError(f"HTTP error fetching {url}")
    return json.loads(data)


def download_package(name: str, project_id: str, version: str, output_dir: Path) -> None:
    output_dir = Path(output_dir)
    registry_url = f"{GITLAB_API}/projects/{project_id}/packages/generic/{name}/{version}"
    packages_api = f"{GITLAB_API}/projects/{project_id}/packages"

    print(f"=== Downloading {name} v{version} ===")

    # Download library files (.a / .so)
    (output_dir / "lib").mkdir(parents=True, exist_ok=True)
    for ext in ("a", "so"):
        fname = f"lib{name}.{ext}"
        data = _get(f"{registry_url}/{fname}")
        if data:
            (output_dir / "lib" / fname).write_bytes(data)
            print(f"  ✅ {fname}")
        else:
            print(f"  — {fname} not in registry, skipping")

    # Discover and download all other package files
    packages = _get_json(f"{packages_api}?package_type=generic&package_name={name}&per_page=1")
    if not packages:
        print(f"  — no package listing found for {name}")
        return

    files_raw = _get_json(f"{packages_api}/{packages[0]['id']}/package_files")
    file_names = sorted({f["file_name"] for f in files_raw})

    for fname in file_names:
        data = _get(f"{registry_url}/{fname}")
        if data is None:
            print(f"  ❌ {fname}")
            continue
        if fname.endswith(".h"):
            dest = output_dir / "include" / name / fname
        elif fname.endswith(".cmake"):
            dest = output_dir / "lib" / "cmake" / name / fname
        else:
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        print(f"  ✅ {fname}")

    print(f"=== done: {name} ===\n")
