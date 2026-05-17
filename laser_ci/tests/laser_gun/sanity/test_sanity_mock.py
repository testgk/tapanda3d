"""
Mock sanity tests for LaserGun.
"""

import pytest
from tests.laser_gun.sanity import SanityTestBase


@pytest.mark.sanity
class TestLaserGunSanityMock(SanityTestBase):
    """Mock sanity tests for laser gun initialization and basic functionality."""

    def test_laser_gun_initialization(self):
        """Test laser gun initializes successfully."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("VERIFY", "Checking initialization state")
        self.assert_laser_initialized()
        self.log_info("✓ Laser gun initialized successfully")

    def test_laser_gun_power_control(self):
        """Test laser gun power can be controlled."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("SET_POWER", "Setting power to 50.0")
        lg.set_power(50.0)

        self.log_step("VERIFY", "Checking power level")
        self.assert_equals(lg.power, 50.0, "Power should be 50.0")
        self.log_info("✓ Power control working correctly")

    def test_laser_gun_frequency_control(self):
        """Test laser gun frequency can be controlled."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("SET_FREQUENCY", "Setting frequency to 100.0 Hz")
        lg.set_frequency(100.0)

        self.log_step("VERIFY", "Checking frequency level")
        self.assert_equals(lg.frequency, 100.0, "Frequency should be 100.0 Hz")
        self.log_info("✓ Frequency control working correctly")

    def test_laser_gun_fire(self):
        """Test laser gun can fire."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("CONFIG", "Setting power for firing")
        lg.set_power(75.0)

        self.log_step("FIRE", "Firing laser")
        result = lg.fire(target="test_target")

        self.log_step("VERIFY", "Checking fire status")
        self.assert_true(result, "Fire should succeed")
        self.assert_equals(lg.fired_count, 1, "Fired count should be 1")
        self.log_info("✓ Laser gun fired successfully")

    def test_laser_gun_power_boundaries(self):
        """Test laser gun power is clamped to valid range."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("SET_POWER", "Setting power to 150.0 (above max)")
        lg.set_power(150.0)

        self.log_step("VERIFY", "Checking power is clamped")
        self.assert_equals(lg.power, 100.0, "Power should be clamped to 100.0")
        self.log_info("✓ Power boundary clamping works correctly")

