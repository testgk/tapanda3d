"""
Base test class for all LaserGun tests.

This is the foundation class that all test categories inherit from.
Provides common utilities and fixtures.
"""

import pytest
import logging
from abc import ABC


class BaseLaserGunTest(ABC):
    """Base class for all LaserGun tests.

    Provides:
    - Common setup/teardown
    - Logging utilities
    - Mock laser gun instance
    - Common assertions
    """

    def setup_method(self):
        """Setup before each test."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Starting test")
        self.laser_gun = None
        self.test_data = {}

    def teardown_method(self):
        """Cleanup after each test."""
        if self.laser_gun:
            self._cleanup_laser_gun()
        self.logger.info(f"Finished test")

    def _cleanup_laser_gun(self):
        """Cleanup laser gun resources."""
        if hasattr(self.laser_gun, 'shutdown'):
            self.laser_gun.shutdown()
        self.laser_gun = None

    def log_step(self, step_name: str, message: str = ""):
        """Log a test step."""
        msg = f"[STEP] {step_name}"
        if message:
            msg += f" - {message}"
        self.logger.info(msg)

    def log_info(self, message: str):
        """Log info message."""
        self.logger.info(message)

    def log_warning(self, message: str):
        """Log warning message."""
        self.logger.warning(message)

    def log_error(self, message: str):
        """Log error message."""
        self.logger.error(message)

    def assert_not_none(self, value, message: str = ""):
        """Assert value is not None."""
        assert value is not None, f"Expected non-None value. {message}" if message else ""

    def assert_equals(self, actual, expected, message: str = ""):
        """Assert actual equals expected."""
        assert actual == expected, f"Expected {expected}, got {actual}. {message}" if message else ""

    def assert_true(self, value, message: str = ""):
        """Assert value is True."""
        assert value is True, f"Expected True, got {value}. {message}" if message else ""

    def assert_false(self, value, message: str = ""):
        """Assert value is False."""
        assert value is False, f"Expected False, got {value}. {message}" if message else ""

    def assert_greater_than(self, actual, threshold, message: str = ""):
        """Assert actual > threshold."""
        assert actual > threshold, f"Expected > {threshold}, got {actual}. {message}" if message else ""

    def assert_less_than(self, actual, threshold, message: str = ""):
        """Assert actual < threshold."""
        assert actual < threshold, f"Expected < {threshold}, got {actual}. {message}" if message else ""

    def assert_in_range(self, value, min_val, max_val, message: str = ""):
        """Assert min_val <= value <= max_val."""
        assert min_val <= value <= max_val, \
            f"Expected {value} in range [{min_val}, {max_val}]. {message}" if message else ""

