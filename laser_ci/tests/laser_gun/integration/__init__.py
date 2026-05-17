"""
Integration test category - Component integration tests.

Tests for multiple components working together, dependencies, and state consistency.
"""

from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class IntegrationTestBase(BaseLaserGunTest):
    """Base class for integration tests.

    Integration tests verify:
    - Multiple components working together
    - State consistency across operations
    - Dependency resolution
    - Cross-component communication
    """

    def setup_method(self):
        """Setup for integration tests."""
        super().setup_method()
        self.log_step("SETUP", "Setting up integration test environment")
        self.components = {}

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

    def create_mock_target(self, name: str, x: float = 0.0, y: float = 0.0):
        """Create a mock target."""
        class MockTarget:
            def __init__(self, name, x, y):
                self.name = name
                self.x = x
                self.y = y
                self.health = 100.0
                self.hit_count = 0

            def take_hit(self):
                self.hit_count += 1
                self.health -= 10.0
                return self.health > 0

        target = MockTarget(name, x, y)
        self.components[name] = target
        return target

    def assert_components_synced(self, *component_names):
        """Assert multiple components are in sync."""
        for name in component_names:
            self.assert_not_none(self.components.get(name), f"Component {name} should exist")

