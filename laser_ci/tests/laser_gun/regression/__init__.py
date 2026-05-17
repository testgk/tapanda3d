"""
Regression test category - Previously known bug tests.

Tests for issues that have been fixed to prevent reoccurrence.
"""

from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class RegressionTestBase(BaseLaserGunTest):
    """Base class for regression tests.

    Regression tests verify:
    - Previously fixed bugs don't reoccur
    - Fixed edge cases still work
    - Known problematic scenarios are covered
    """

    def setup_method(self):
        """Setup for regression tests."""
        super().setup_method()
        self.log_step("SETUP", "Setting up regression test environment")
        self.regression_issues = []

    def log_regression_issue(self, issue_id: str, description: str):
        """Log a regression issue being tested."""
        self.regression_issues.append((issue_id, description))
        self.log_info(f"[REGRESSION #{issue_id}] {description}")

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

