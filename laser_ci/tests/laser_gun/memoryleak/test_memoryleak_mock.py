"""
Mock memory leak tests for LaserGun.
"""

import gc
import pytest
from tests.laser_gun.memoryleak import MemoryLeakTestBase
from tests.laser_gun.mock import MockLaserGun


@pytest.mark.memoryleak
class TestLaserGunMemoryLeakMock(MemoryLeakTestBase):
    """Mock memory leak tests for laser gun."""
    
    def test_laser_gun_repeated_initialization_no_leak(self):
        """Test repeated laser gun initialization doesn't leak memory."""
        self.log_step("BASELINE", "Measuring initial objects")
        gc.collect()
        initial_count = len(gc.get_objects())
        
        self.log_step("OPERATION", "Creating and destroying laser guns 50 times")
        for i in range(50):
            lg = MockLaserGun()
            lg.initialize()
            lg.shutdown()
            del lg
        
        self.log_step("CLEANUP", "Running garbage collection")
        gc.collect()
        final_count = len(gc.get_objects())
        
        self.log_step("VERIFY", "Checking for memory leaks")
        self.assert_object_cleanup(initial_count, final_count, tolerance=5)
        self.log_info(f"✓ No memory leak: {initial_count} -> {final_count} objects")
    
    def test_laser_gun_fire_no_memory_leak(self):
        """Test repeated firing doesn't leak memory."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        
        self.log_step("BASELINE", "Measuring initial objects")
        gc.collect()
        initial_count = len(gc.get_objects())
        
        self.log_step("OPERATION", "Firing laser 1000 times")
        for i in range(1000):
            lg.fire(target=f"target_{i}")
        
        self.log_step("CLEANUP", "Running garbage collection")
        gc.collect()
        final_count = len(gc.get_objects())
        
        self.log_step("VERIFY", "Checking for memory leaks")
        self.assert_object_cleanup(initial_count, final_count, tolerance=10)
        self.log_info(f"✓ No memory leak during firing: {initial_count} -> {final_count} objects")
    
    def test_laser_gun_shutdown_cleanup(self):
        """Test laser gun properly cleans up on shutdown."""
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        
        self.log_step("OPERATION", "Setting power and firing")
        lg.set_power(80.0)
        lg.set_frequency(500.0)
        lg.fire(target="test")
        
        self.log_step("SHUTDOWN", "Shutting down laser gun")
        initial_refcount = self.get_refcount(lg)
        lg.shutdown()
        
        self.log_step("VERIFY", "Checking shutdown state")
        self.assert_false(lg.is_active, "Laser should be inactive after shutdown")
        self.log_info("✓ Laser gun properly cleaned up on shutdown")

