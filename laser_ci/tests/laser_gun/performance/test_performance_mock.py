"""
Mock performance tests for LaserGun.
"""

import pytest
from tests.laser_gun.performance import PerformanceTestBase


@pytest.mark.performance
class TestLaserGunPerformanceMock(PerformanceTestBase):
    """Mock performance tests for laser gun."""

    def test_laser_gun_fire_speed(self):
        """Test laser gun firing speed."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)

        self.log_step("BENCHMARK", "Measuring fire speed")
        self.start_timer("fire_speed")
        for i in range(100):
            lg.fire(target=f"target_{i}")
        elapsed = self.end_timer("fire_speed")

        self.log_step("VERIFY", "Checking fire speed threshold")
        self.assert_under_threshold(elapsed, 1.0, "100 fire operations")
        self.assert_equals(lg.fired_count, 100, "Should fire 100 times")
        self.log_info(f"✓ Fire speed: {lg.fired_count/elapsed:.0f} shots/second")

    def test_laser_gun_power_adjustment_responsiveness(self):
        """Test laser gun power adjustment responsiveness."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()

        self.log_step("BENCHMARK", "Measuring power adjustment response time")
        self.start_timer("power_adjustment")
        for i in range(100):
            power = (i % 100) / 100.0 * 100.0
            lg.set_power(power)
        elapsed = self.end_timer("power_adjustment")

        self.log_step("VERIFY", "Checking responsiveness threshold")
        self.assert_under_threshold(elapsed, 0.5, "100 power adjustments")
        self.log_info(f"✓ Power adjustments per second: {100/elapsed:.0f}")

    def test_laser_gun_frequency_sweep_performance(self):
        """Test laser gun frequency sweep performance."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)

        self.log_step("BENCHMARK", "Measuring frequency sweep")
        self.start_timer("frequency_sweep")
        for i in range(1, 101):
            lg.set_frequency(i * 10.0)
            lg.fire(target=f"target_{i}")
        elapsed = self.end_timer("frequency_sweep")

        self.log_step("VERIFY", "Checking throughput")
        self.assert_under_threshold(elapsed, 1.0, "Frequency sweep with firing")
        self.log_info(f"✓ Frequency sweep throughput: {lg.fired_count/elapsed:.0f} ops/sec")

