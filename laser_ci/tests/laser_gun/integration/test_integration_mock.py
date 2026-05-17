"""
Mock integration tests for LaserGun.
"""

import pytest
from tests.laser_gun.integration import IntegrationTestBase


@pytest.mark.integration
class TestLaserGunIntegrationMock(IntegrationTestBase):
    """Mock integration tests for laser gun system."""

    def test_laser_gun_with_target_system(self):
        """Test laser gun integrated with target system."""
        self.log_step("INIT", "Creating laser gun and target")
        lg = self.create_laser_gun()
        target = self.create_mock_target("test_target", x=10.0, y=5.0)

        self.log_step("CONFIG", "Setting laser power for target")
        lg.set_power(100.0)
        lg.set_frequency(500.0)

        self.log_step("ENGAGE", "Firing at target")
        lg.fire(target="test_target")

        self.log_step("VERIFY", "Checking target was hit")
        self.assert_components_synced("test_target")
        self.assert_equals(lg.last_target, "test_target", "Target should be set")
        self.log_info("✓ Laser gun successfully engaged target")

    def test_multiple_targets_sequential_engagement(self):
        """Test engaging multiple targets sequentially."""
        self.log_step("INIT", "Creating laser gun and multiple targets")
        lg = self.create_laser_gun()
        target1 = self.create_mock_target("target_1", x=0.0, y=0.0)
        target2 = self.create_mock_target("target_2", x=10.0, y=10.0)
        target3 = self.create_mock_target("target_3", x=-10.0, y=5.0)

        self.log_step("CONFIG", "Configuring laser")
        lg.set_power(75.0)

        self.log_step("ENGAGE", "Engaging targets sequentially")
        lg.fire(target="target_1")
        lg.fire(target="target_2")
        lg.fire(target="target_3")

        self.log_step("VERIFY", "Checking all targets registered")
        self.assert_components_synced("target_1", "target_2", "target_3")
        self.assert_equals(lg.fired_count, 3, "Should fire 3 times")
        self.assert_equals(lg.last_target, "target_3", "Last target should be target_3")
        self.log_info("✓ Sequential target engagement successful")

    def test_laser_gun_frequency_adaptation_for_targets(self):
        """Test laser gun adapts frequency for different targets."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)

        self.log_step("OPERATION", "Adapting frequency for different scenarios")
        target_configs = [
            ("armored_target", 100.0),
            ("fast_target", 500.0),
            ("stealth_target", 750.0)
        ]

        for target_name, freq in target_configs:
            self.log_step("ENGAGE", f"Targeting {target_name} at {freq} Hz")
            lg.set_frequency(freq)
            lg.fire(target=target_name)

        self.log_step("VERIFY", "Checking all engagements recorded")
        self.assert_equals(lg.fired_count, 3, "Should fire 3 times")
        self.log_info("✓ Frequency adaptation for different targets successful")

