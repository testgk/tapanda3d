#!/usr/bin/env python3
"""Upload built artifacts from install/ to the GitLab Generic Package Registry."""

import os
import urllib.error
import urllib.request
from pathlib import Path

GITLAB_API = "https://gitlab.com/api/v4"


def _auth_header() -> tuple[str, str]:
    if os.environ.get("GITLAB_ACCESS_TOKEN"):
        return ("PRIVATE-TOKEN", os.environ["GITLAB_ACCESS_TOKEN"])
    if os.environ.get("CI_JOB_TOKEN"):
        return ("JOB-TOKEN", os.environ["CI_JOB_TOKEN"])
    raise RuntimeError( "No token available — set GITLAB_ACCESS_TOKEN or run in CI" )


def _upload( url: str, data: bytes ) -> None:
    name, value = _auth_header()
    req = urllib.request.Request( url, data=data, method="PUT", headers={ name: value } )
    req.add_header( "Content-Type", "application/octet-stream" )
    try:
        with urllib.request.urlopen( req ) as resp:
            if resp.status not in ( 200, 201 ):
                raise RuntimeError( f"Unexpected status {resp.status} uploading {url}" )
    except urllib.error.HTTPError as e:
        raise RuntimeError( f"Upload failed ({e.code}): {url}" ) from e


def publish_package( name: str, project_id: str, version: str, install_dir: Path ) -> None:
    install_dir = Path( install_dir )
    base = f"{GITLAB_API}/projects/{project_id}/packages/generic/{name}/{version}"

    print( f"=== Publishing {name} v{version} ===" )

    # Libraries
    lib_dir = install_dir / "lib"
    for ext in ( "a", "so" ):
        path = lib_dir / f"lib{name}.{ext}"
        if path.exists():
            _upload( f"{base}/lib{name}.{ext}", path.read_bytes() )
            print( f"  lib{name}.{ext}" )

    # Headers
    include_dir = install_dir / "include" / name
    if include_dir.is_dir():
        for path in sorted( include_dir.glob( "*.h" ) ):
            _upload( f"{base}/{path.name}", path.read_bytes() )
            print( f"  {path.name}" )

    # CMake config files
    cmake_dir = lib_dir / "cmake" / name
    if cmake_dir.is_dir():
        for path in sorted( cmake_dir.glob( "*.cmake" ) ):
            _upload( f"{base}/{path.name}", path.read_bytes() )
            print( f"  {path.name}" )

    print( f"=== done: {name} ===\n" )
