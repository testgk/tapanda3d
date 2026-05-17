"""
Pytest configuration and fixtures for LaserGun tests.
"""

import pytest
import logging
from pathlib import Path


# Register custom markers
def pytest_configure(config):
    """Configure pytest and register custom markers."""
    config.addinivalue_line("markers", "sanity: basic functionality tests")
    config.addinivalue_line("markers", "performance: speed and efficiency tests")
    config.addinivalue_line("markers", "memoryleak: memory and resource tests")
    config.addinivalue_line("markers", "integration: component integration tests")
    config.addinivalue_line("markers", "stress: load and stress tests")
    config.addinivalue_line("markers", "regression: regression/known bugs tests")

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


@pytest.fixture(scope="session")
def test_data_dir():
    """Return test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_laser_gun():
    """Create a mock laser gun instance."""
    class MockLaserGun:
        def __init__(self):
            self.power = 0.0
            self.frequency = 0.0
            self.is_active = False
            self.fired_count = 0
            self.last_target = None

        def initialize(self):
            self.is_active = True

        def set_power(self, power):
            self.power = max(0.0, min(100.0, power))

        def set_frequency(self, frequency):
            self.frequency = max(1.0, min(1000.0, frequency))

        def fire(self, target=None):
            if self.is_active and self.power > 0:
                self.fired_count += 1
                self.last_target = target
                return True
            return False

        def shutdown(self):
            self.is_active = False

    return MockLaserGun()


@pytest.fixture
def logger():
    """Get a logger instance."""
    return logging.getLogger("test")

