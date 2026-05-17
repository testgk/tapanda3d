"""
Performance test category - Speed and efficiency tests.

Tests firing speed, response time, and operational efficiency.
"""

import time
from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class PerformanceTestBase(BaseLaserGunTest):
    """Base class for performance tests.

    Performance tests verify:
    - Firing speed
    - Response time
    - Throughput
    - Resource efficiency
    """

    def setup_method(self):
        """Setup for performance tests."""
        super().setup_method()
        self.log_step("SETUP", "Initializing for performance test")
        self.timings = {}

    def start_timer(self, name: str):
        """Start a named timer."""
        self.timings[name] = time.time()

    def end_timer(self, name: str) -> float:
        """End a named timer and return elapsed time in seconds."""
        if name not in self.timings:
            raise ValueError(f"Timer '{name}' not started")
        elapsed = time.time() - self.timings[name]
        self.log_info(f"Timer '{name}': {elapsed:.4f}s")
        return elapsed

    def assert_under_threshold(self, elapsed: float, threshold: float, operation: str):
        """Assert operation completed under time threshold."""
        assert elapsed < threshold, \
            f"{operation} took {elapsed:.4f}s, expected < {threshold}s"

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

