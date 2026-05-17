"""
Stress test category - Load and stress tests.

Tests for system behavior under heavy load and extreme conditions.
"""

from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class StressTestBase(BaseLaserGunTest):
    """Base class for stress tests.

    Stress tests verify:
    - Handling high volume operations
    - Behavior under heavy load
    - Error handling and recovery
    - System stability
    """

    def setup_method(self):
        """Setup for stress tests."""
        super().setup_method()
        self.log_step("SETUP", "Preparing stress test environment")

    def assert_all_operations_successful(self, results: list):
        """Assert all operations in result list succeeded."""
        failures = [r for r in results if not r]
        assert len(failures) == 0, f"{len(failures)} operations failed out of {len(results)}"

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

