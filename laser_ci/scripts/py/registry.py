#!/usr/bin/env python3
"""Resolve a project name string to its ProjectConfig instance."""

import importlib
import json
import os
from project_config import ProjectConfig


def load_config(project: str) -> ProjectConfig:
    """Load config for a project by name (e.g. 'lasershark').

    If the TRIGGER_PARAMS env var is set, its JSON fields override the ini values.
    Expects a module named <project>_config with a class named
    <Project>Config that has a load() classmethod.
    """
    module_name = f"{project}_config"
    class_name = "".join(w.capitalize() for w in project.split("_")) + "Config"
    try:
        mod = importlib.import_module(module_name)
        cls = getattr(mod, class_name)
    except (ImportError, AttributeError) as e:
        raise ValueError(f"No config found for project '{project}': {e}")

    config = cls.load()

    # Option 3: artifact-based override (trigger.json) takes priority
    from pathlib import Path
    trigger_file = Path("trigger.json")
    if trigger_file.exists():
        payload = json.loads(trigger_file.read_text())
        payload.pop("project", None)
        if payload:
            print(f"Applying trigger.json overrides: {payload}")
            config = config.apply_overrides(payload)
    # Option 2: JSON string in TRIGGER_PARAMS env var
    elif trigger_params := os.environ.get("TRIGGER_PARAMS"):
        overrides = json.loads(trigger_params)
        print(f"Applying TRIGGER_PARAMS overrides: {overrides}")
        config = config.apply_overrides(overrides)

    return config
