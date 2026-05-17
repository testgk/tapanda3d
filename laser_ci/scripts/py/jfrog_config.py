#!/usr/bin/env python3
"""JFrog Artifactory configuration."""

import os
from dataclasses import dataclass


@dataclass
class JFrogConfig:
    """Configuration for JFrog Artifactory publishing."""

    url: str
    repo: str
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    access_token: str | None = None

    @classmethod
    def from_env(cls) -> "JFrogConfig":
        """Create JFrog config from environment variables."""
        return cls(
            url=os.environ.get("JFROG_URL", "https://your-jfrog-instance.jfrog.io"),
            repo=os.environ.get("JFROG_REPO", "laser-ci-generic"),
            username=os.environ.get("JFROG_USERNAME"),
            password=os.environ.get("JFROG_PASSWORD"),
            api_key=os.environ.get("JFROG_API_KEY"),
        )

    def get_auth_header(self) -> tuple[str, str]:
        """Get appropriate authentication header for JFrog."""
        if self.api_key:
            return ("X-JFrog-Art-Api", self.api_key)
        elif self.username and self.password:
            import base64
            auth = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            return ("Authorization", f"Basic {auth}")
        else:
            raise RuntimeError(
                "No JFrog credentials available — set JFROG_API_KEY or JFROG_USERNAME/JFROG_PASSWORD"
            )
