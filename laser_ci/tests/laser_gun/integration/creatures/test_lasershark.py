"""
LaserShark Integration Tests

Tests for LaserShark creature integration with LaserGun system.
Demonstrates how to use GenericCreatureIntegrationTest for specific creatures.

This is an example pattern that other creature projects can replicate.
"""

import pytest
from tests.laser_gun.integration.creatures import GenericCreatureIntegrationTest, CreatureBase


class LaserShark(CreatureBase):
    """Mock LaserShark creature for testing."""

    def __init__(self, name: str = "Shark", species: str = "Great White"):
        super().__init__(name, species)
        self.bite_force = 4000  # PSI
        self.swim_speed = 35  # MPH
        self.predator_rating = 9.5


class LaserSharkIntegrationTest(GenericCreatureIntegrationTest):
    """Base class for LaserShark integration tests.

    Provides LaserShark-specific factory and assertions.
    Other LaserShark test classes can inherit from this.
    """

    def create_creature(self):
        """Create a LaserShark instance."""
        shark = LaserShark(name="TestShark", species="Great White")
        self.components["shark"] = shark
        return shark

    def assert_shark_ferocity(self, shark, expected_rating: float):
        """Assert shark has expected predator rating."""
        self.assert_equals(shark.predator_rating, expected_rating,
                          "Shark predator rating mismatch")

    def assert_shark_operational_ferocity(self, shark):
        """Assert shark is both operational and fierce."""
        self.assert_creature_operational(shark)
        self.assert_greater_than(shark.predator_rating, 5.0,
                                "Shark must be fierce to be dangerous")


@pytest.mark.integration
class TestLaserSharkBasicIntegration(LaserSharkIntegrationTest):
    """Mock: LaserShark basic integration tests."""

    def test_laser_shark_equips_laser(self):
        """Test LaserShark can equip laser gun."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("CREATE_LASER", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)

        self.log_step("EQUIP", "Equipping laser to shark")
        shark.equip_laser(lg)

        self.log_step("VERIFY", "Checking shark has laser")
        self.assert_shark_ferocity(shark, 9.5)
        self.assert_creature_has_laser(shark)
        self.log_info("✓ LaserShark equipped with laser gun")

    def test_laser_shark_target_acquisition(self):
        """Test LaserShark acquires targets."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("CREATE_LASER", "Creating laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        shark.equip_laser(lg)

        self.log_step("ACQUIRE_TARGET", "Acquiring target")
        shark.acquire_target("enemy_whale")

        self.log_step("VERIFY", "Checking target acquired")
        self.assert_target_acquired(shark)
        self.assert_equals(shark.current_target, "enemy_whale",
                          "Target should be set to enemy_whale")
        self.log_info("✓ LaserShark acquired target successfully")

    def test_laser_shark_fires_at_target(self):
        """Test LaserShark fires laser at acquired target."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("EQUIP_LASER", "Equipping laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        shark.equip_laser(lg)

        self.log_step("ACQUIRE_TARGET", "Acquiring enemy target")
        shark.acquire_target("enemy_creature")

        self.log_step("VERIFY_OPERATIONAL", "Checking creature is operational")
        self.assert_creature_operational(shark)

        self.log_step("FIRE", "Firing laser missile")
        fire_result = shark.fire_laser()

        self.log_step("VERIFY_FIRE", "Checking fire success")
        self.assert_true(fire_result, "Shark should fire successfully")
        self.assert_equals(lg.fired_count, 1, "Laser should have fired once")
        self.assert_equals(lg.last_target, "enemy_creature", "Target should be recorded")
        self.log_info("✓ LaserShark fired laser at target")


@pytest.mark.integration
class TestLaserSharkAdvancedIntegration(LaserSharkIntegrationTest):
    """Mock: LaserShark advanced integration scenarios."""

    def test_laser_shark_multi_target_engagement(self):
        """Test LaserShark engaging multiple targets sequentially."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("EQUIP_LASER", "Equipping laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        lg.set_frequency(500.0)
        shark.equip_laser(lg)

        self.log_step("MULTI_TARGET", "Engaging multiple targets")
        targets = ["target_1", "target_2", "target_3"]
        fire_count = 0

        for target in targets:
            self.log_step("ACQUIRE", f"Acquiring {target}")
            shark.acquire_target(target)

            result = shark.fire_laser()
            if result:
                fire_count += 1

        self.log_step("VERIFY", "Checking all targets engaged")
        self.assert_equals(lg.fired_count, 3, "Should fire 3 times")
        self.assert_shark_operational_ferocity(shark)
        self.log_info(f"✓ LaserShark engaged {fire_count} targets successfully")

    def test_laser_shark_without_target_cannot_fire(self):
        """Test LaserShark cannot fire without target."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("EQUIP_LASER", "Equipping laser gun")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        shark.equip_laser(lg)

        self.log_step("TRY_FIRE", "Attempting fire without target")
        result = shark.fire_laser()

        self.log_step("VERIFY", "Checking fire failed")
        self.assert_false(result, "Shark should not fire without target")
        self.assert_equals(lg.fired_count, 0, "Laser should not have fired")
        self.log_info("✓ LaserShark correctly prevented fire without target")

    def test_laser_shark_damage_system(self):
        """Test LaserShark takes damage."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()
        initial_health = shark.health

        self.log_step("DAMAGE", "Applying 25 damage")
        shark.take_damage(25.0)

        self.log_step("VERIFY", "Checking health reduced")
        self.assert_creature_alive(shark)
        self.assert_equals(shark.health, 75.0, "Health should be 75")
        self.log_info("✓ LaserShark damage system working")

    def test_laser_shark_lethal_damage(self):
        """Test LaserShark dies from lethal damage."""
        self.log_step("INIT", "Creating LaserShark")
        shark = self.create_creature()

        self.log_step("DAMAGE", "Applying 150 lethal damage")
        shark.take_damage(150.0)

        self.log_step("VERIFY", "Checking shark is dead")
        self.assert_creature_dead(shark)
        self.assert_equals(shark.health, 0.0, "Health should be 0")
        self.log_info("✓ LaserShark lethal damage system working")


@pytest.mark.integration
class TestLaserSharkWithTargetSync(LaserSharkIntegrationTest):
    """Mock: LaserShark with target system synchronization."""

    def test_laser_shark_coordinated_fire(self):
        """Test LaserShark coordinated firing with target tracking."""
        self.log_step("INIT", "Creating LaserShark and target")
        shark = self.create_creature()
        target = self.create_mock_target("whale_target", x=100.0, y=50.0)

        self.log_step("EQUIP_LASER", "Equipping laser")
        lg = self.create_laser_gun()
        lg.set_power(100.0)
        lg.set_frequency(600.0)
        shark.equip_laser(lg)

        self.log_step("ACQUIRE_TRACK", "Acquiring and tracking target")
        shark.acquire_target(target.name)

        self.log_step("MULTI_FIRE", "Multiple coordinated shots")
        for i in range(5):
            shark.fire_laser()

        self.log_step("VERIFY", "Checking coordination")
        self.assert_components_synced("whale_target")
        self.assert_equals(lg.fired_count, 5, "Should fire 5 times")
        self.assert_shark_operational_ferocity(shark)
        self.log_info("✓ LaserShark coordinated fire successful")

