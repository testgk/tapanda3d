"""
Mock LaserGun implementation for testing.
"""


class MockLaserGun:
    """Mock laser gun for testing without hardware dependencies."""
    
    def __init__(self):
        self.power = 0.0
        self.frequency = 0.0
        self.is_active = False
        self.fired_count = 0
        self.last_target = None
    
    def initialize(self):
        """Initialize the laser gun."""
        self.is_active = True
    
    def set_power(self, power):
        """Set laser power (0-100%)."""
        self.power = max(0.0, min(100.0, power))
    
    def set_frequency(self, frequency):
        """Set laser frequency (1-1000 Hz)."""
        self.frequency = max(1.0, min(1000.0, frequency))
    
    def fire(self, target=None):
        """Fire the laser.
        
        Args:
            target: Optional target identifier
            
        Returns:
            True if fire succeeded, False otherwise
        """
        if self.is_active and self.power > 0:
            self.fired_count += 1
            self.last_target = target
            return True
        return False
    
    def shutdown(self):
        """Shutdown the laser gun."""
        self.is_active = False

