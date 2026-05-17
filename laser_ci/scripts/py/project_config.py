#!/usr/bin/env python3
"""Reads project ini configuration files and exposes typed configuration objects."""

import configparser
import copy
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PackageConfig:
    name: str
    id: str
    version: str


@dataclass
class RegistryConfig:
    url: str


@dataclass
class PathsConfig:
    repo_root: Path
    build_dir: Path
    install_dir: Path


@dataclass
class SourceConfig:
    url: str
    branch: str = ""


@dataclass
class ProjectConfig:
    package: PackageConfig
    dependencies: dict[str, str]
    registry: RegistryConfig
    paths: PathsConfig
    source: SourceConfig

    @classmethod
    def from_file(cls, path: str | Path) -> "ProjectConfig":
        path = Path(path)
        parser = configparser.ConfigParser()
        parser.read(path)

        package = PackageConfig(
            name=parser["package"]["name"],
            id=parser["package"]["id"],
            version=parser["package"]["version"],
        )

        dependencies = dict(parser["dependencies"]) if "dependencies" in parser else {}

        registry = RegistryConfig(
            url=parser["registry"]["url"] if "registry" in parser else "",
        )

        ini_dir = path.parent
        raw_paths = parser["paths"] if "paths" in parser else {}
        paths = PathsConfig(
            repo_root=(ini_dir / raw_paths.get("repo_root", ".")).resolve(),
            build_dir=(ini_dir / raw_paths.get("build_dir", "build")).resolve(),
            install_dir=(ini_dir / raw_paths.get("install_dir", "install")).resolve(),
        )

        source = SourceConfig(
            url=parser["source"]["url"] if "source" in parser else "",
            branch=parser["source"].get("branch", "") if "source" in parser else "",
        )

        return cls(package=package, dependencies=dependencies, registry=registry, paths=paths, source=source)

    def apply_overrides(self, overrides: dict) -> "ProjectConfig":
        """Return a new config with fields overridden from a dict.

        Supported keys: version, branch, install_dir, build_dir, repo_root.
        """
        updated = copy.deepcopy(self)
        if "version" in overrides:
            updated.package.version = overrides["version"]
        if "branch" in overrides:
            updated.source.branch = overrides["branch"]
        if "install_dir" in overrides:
            updated.paths.install_dir = Path(overrides["install_dir"])
        if "build_dir" in overrides:
            updated.paths.build_dir = Path(overrides["build_dir"])
        if "repo_root" in overrides:
            updated.paths.repo_root = Path(overrides["repo_root"])
        return updated

    @classmethod
    def load_all(cls, configs_dir: str | Path) -> dict[str, "ProjectConfig"]:
        """Load all *.ini files from a directory, keyed by project name."""
        return {
            path.stem: cls.from_file(path)
            for path in Path(configs_dir).glob("*.ini")
        }