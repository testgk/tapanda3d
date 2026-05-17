#!/usr/bin/env python3
from pathlib import Path

from project_config import ProjectConfig

CONFIGS_DIR = Path(__file__).parent.parent.parent / "configs"


class LasersharkConfig(ProjectConfig):
    @classmethod
    def load(cls) -> "LasersharkConfig":
        return cls.from_file(CONFIGS_DIR / "lasershark.ini")