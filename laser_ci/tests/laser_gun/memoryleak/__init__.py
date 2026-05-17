"""
Memory leak test category - Memory usage and resource management tests.

Tests for memory leaks, resource cleanup, and garbage collection.
"""

import gc
import sys
from tests.laser_gun.base import BaseLaserGunTest
from tests.laser_gun.mock import MockLaserGun


class MemoryLeakTestBase(BaseLaserGunTest):
    """Base class for memory leak tests.

    Memory leak tests verify:
    - Resource cleanup
    - No memory leaks with repeated operations
    - Proper garbage collection
    - Reference cycles cleanup
    """

    def setup_method(self):
        """Setup for memory leak tests."""
        super().setup_method()
        self.log_step("SETUP", "Clearing garbage before test")
        gc.collect()

    def teardown_method(self):
        """Cleanup for memory leak tests."""
        self.log_step("TEARDOWN", "Collecting garbage after test")
        gc.collect()
        super().teardown_method()

    def get_object_count(self, obj_type: type) -> int:
        """Get count of objects of a specific type."""
        return len([obj for obj in gc.get_objects() if isinstance(obj, obj_type)])

    def get_refcount(self, obj) -> int:
        """Get reference count of an object."""
        return sys.getrefcount(obj)

    def assert_object_cleanup(self, initial_count: int, final_count: int, tolerance: int = 2):
        """Assert objects were properly cleaned up.

        Args:
            initial_count: Count before operation
            final_count: Count after cleanup
            tolerance: Allowed extra objects (default 2 for safety)
        """
        diff = final_count - initial_count
        assert diff <= tolerance, \
            f"Memory leak detected: {diff} extra objects, tolerance={tolerance}"

    def create_laser_gun(self):
        """Create and initialize laser gun."""
        self.laser_gun = MockLaserGun()
        self.laser_gun.initialize()
        return self.laser_gun

