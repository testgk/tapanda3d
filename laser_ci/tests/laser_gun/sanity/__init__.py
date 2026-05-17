"""
Sanity test category - Basic functionality tests.

Tests basic initialization, startup, configuration, and core operations.
"""

from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class SanityTestBase(BaseLaserGunTest):
    """Base class for sanity tests.

    Sanity tests verify:
    - Basic initialization
    - Configuration setup
    - Core functionality
    - State management
    """

    def setup_method(self):
        """Setup for sanity tests."""
        super().setup_method()
        self.log_step("SETUP", "Initializing laser gun for sanity test")

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

    def assert_laser_initialized(self):
        """Assert laser gun is properly initialized."""
        self.assert_not_none(self.laser_gun, "Laser gun should be initialized")
        self.assert_true(self.laser_gun.is_active, "Laser gun should be active")

    def assert_laser_can_fire(self):
        """Assert laser gun can fire."""
        self.assert_greater_than(self.laser_gun.power, 0, "Power should be > 0 to fire")

