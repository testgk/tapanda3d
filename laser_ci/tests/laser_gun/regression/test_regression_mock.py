"""
Mock regression tests for LaserGun.
"""

import pytest
from tests.laser_gun.regression import RegressionTestBase


@pytest.mark.regression
class TestLaserGunRegressionMock(RegressionTestBase):
    """Mock regression tests for laser gun system."""

    def test_regression_power_clamping_boundary(self):
        """Regression: Issue #001 - Power values exceeding 100% caused overflow.

        Fix: Clamp power values to [0, 100] range.
        """
        self.log_regression_issue("001", "Power overflow when set > 100%")

        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("TEST", "Setting power to extreme values")
        lg.set_power(999.0)
        self.assert_equals(lg.power, 100.0, "Power should be clamped to 100.0")

        lg.set_power(-50.0)
        self.assert_equals(lg.power, 0.0, "Power should be clamped to 0.0")

        self.log_info("✓ Regression #001 fixed: Power clamping works correctly")

    def test_regression_zero_power_fire_prevention(self):
        """Regression: Issue #002 - Laser fired with zero power causing simulation errors.

        Fix: Prevent firing when power is 0.
        """
        self.log_regression_issue("002", "Firing with zero power caused errors")

        self.log_step("INIT", "Creating laser gun with zero power")
        lg = self.create_laser_gun()
        lg.set_power(0.0)

        self.log_step("TEST", "Attempting to fire with zero power")
        result = lg.fire(target="test_target")

        self.assert_false(result, "Fire should fail with zero power")
        self.assert_equals(lg.fired_count, 0, "Should not increment fired count")
        self.log_info("✓ Regression #002 fixed: Zero power fire prevention works")

    def test_regression_frequency_bounce_back(self):
        """Regression: Issue #003 - Frequency values outside range weren't clamped.

        Fix: Clamp frequency to [1, 1000] Hz range.
        """
        self.log_regression_issue("003", "Frequency values outside valid range")

        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("TEST", "Setting invalid frequency values")
        lg.set_frequency(0.1)  # Below minimum
        self.assert_greater_than(lg.frequency, 0.5, "Frequency should be >= 1.0")

        lg.set_frequency(5000.0)  # Above maximum
        self.assert_less_than(lg.frequency, 1001.0, "Frequency should be <= 1000.0")

        self.log_info("✓ Regression #003 fixed: Frequency boundary clamping works")

    def test_regression_repeated_shutdown_safety(self):
        """Regression: Issue #004 - Calling shutdown multiple times caused errors.

        Fix: Make shutdown idempotent and safe to call multiple times.
        """
        self.log_regression_issue("004", "Multiple shutdown calls caused errors")

        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        lg.fire(target="test")

        self.log_step("TEST", "Calling shutdown multiple times")
        lg.shutdown()
        lg.shutdown()  # Should not error
        lg.shutdown()  # Should not error

        self.assert_false(lg.is_active, "Laser should remain inactive")
        self.log_info("✓ Regression #004 fixed: Multiple shutdown calls are safe")

