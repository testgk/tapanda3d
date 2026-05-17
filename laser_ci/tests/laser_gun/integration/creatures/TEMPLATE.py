"""
Template for Other Creature Projects

This template demonstrates how to create integration tests for your own creature project.

Simply copy this pattern and replace OtherCreature with your creature name.

Example: For LaserWhale project
=========

1. Create a file: your_project/tests/integration/test_laserwhale_integration.py

2. Import the generic base:
   from laser_gun_tests.integration.creatures import GenericCreatureIntegrationTest

3. Define your creature:
   class LaserWhale(CreatureBase):
       def __init__(self, name="Whale"):
           super().__init__(name, "Blue Whale")
           # Add whale-specific attributes

4. Create test class:
   class LaserWhaleIntegrationTest(GenericCreatureIntegrationTest):
       def create_creature(self):
           whale = LaserWhale()
           self.components["whale"] = whale
           return whale

5. Add whale-specific tests:
   class TestLaserWhaleIntegration(LaserWhaleIntegrationTest):
       def test_whale_specific_feature(self):
           creature = self.create_creature()
           # Your test here
"""

import pytest
from tests.laser_gun.integration.creatures import GenericCreatureIntegrationTest, CreatureBase


class OtherCreature(CreatureBase):
    """Template for other creature implementations.
    
    Copy and modify this class for your specific creature type.
    """
    
    def __init__(self, name: str = "Creature", species: str = "Generic"):
        super().__init__(name, species)
        # Add your creature-specific attributes here
        # self.custom_attribute = value
    
    def creature_specific_method(self):
        """Add creature-specific behavior here."""
        pass


class OtherCreatureIntegrationTest(GenericCreatureIntegrationTest):
    """Template base class for creature integration tests.
    
    Steps to use:
    1. Rename OtherCreature to your creature name
    2. Override create_creature() to return your creature
    3. Add specific assertions if needed
    4. Create test classes that inherit from this
    """
    
    def create_creature(self):
        """Create your creature instance."""
        creature = OtherCreature(name="TestCreature", species="Your Species")
        self.components["creature"] = creature
        return creature
    
    # Add creature-specific assertion methods here
    # def assert_creature_property(self, creature):
    #     """Assert creature-specific property."""
    #     pass


@pytest.mark.integration
class TestOtherCreatureTemplateIntegration(OtherCreatureIntegrationTest):
    """Template tests demonstrating the integration pattern."""
    
    def test_creature_template_equips_laser(self):
        """Template: Test creature can equip laser."""
        self.log_step("INIT", "Creating creature from template")
        creature = self.create_creature()
        
        self.log_step("CREATE_LASER", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        
        self.log_step("EQUIP", "Equipping laser")
        creature.equip_laser(lg)
        
        self.log_step("VERIFY", "Checking laser equipped")
        self.assert_creature_has_laser(creature)
        self.log_info("✓ Template creature equipped with laser gun")
    
    def test_creature_template_fire_sequence(self):
        """Template: Test creature fire sequence."""
        self.log_step("INIT", "Creating creature")
        creature = self.create_creature()
        
        self.log_step("EQUIP_LASER", "Equipping laser")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        creature.equip_laser(lg)
        
        self.log_step("ACQUIRE_TARGET", "Acquiring target")
        creature.acquire_target("test_target")
        
        self.log_step("FIRE", "Firing laser")
        result = creature.fire_laser()
        
        self.log_step("VERIFY", "Checking fire result")
        self.assert_true(result, "Fire should succeed")
        self.log_info("✓ Template creature fire sequence successful")

