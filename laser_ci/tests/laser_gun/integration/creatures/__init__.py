"""
Generic Creatures Integration Base

Provides a reusable integration framework for any creature project
that wants to integrate with LaserGun.

This allows Shark, Whale, and other creature projects to test their
integration with LaserGun using a consistent pattern.
"""

from tests.laser_gun.integration import IntegrationTestBase
from tests.laser_gun.mock import MockLaserGun


class CreatureBase:
    """Mock creature base class for testing."""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species
        self.health = 100.0
        self.is_alive = True
        self.equipped_laser = None
        self.target_acquired = False
        self.current_target = None

    def equip_laser(self, laser_gun):
        """Equip a laser gun to this creature."""
        self.equipped_laser = laser_gun

    def unequip_laser(self):
        """Remove equipped laser gun."""
        self.equipped_laser = None

    def has_laser(self):
        """Check if creature has laser equipped."""
        return self.equipped_laser is not None

    def acquire_target(self, target):
        """Acquire a target."""
        self.current_target = target
        self.target_acquired = True

    def lose_target(self):
        """Lose current target."""
        self.target_acquired = False
        self.current_target = None

    def fire_laser(self):
        """Fire equipped laser if available."""
        if not self.has_laser():
            return False
        if not self.target_acquired:
            return False
        return self.equipped_laser.fire(target=self.current_target)

    def take_damage(self, amount: float):
        """Take damage."""
        self.health -= amount
        if self.health <= 0:
            self.is_alive = False
            self.health = 0

    def is_operational(self):
        """Check if creature is operational."""
        return self.is_alive and self.has_laser() and self.target_acquired


class GenericCreatureIntegrationTest(IntegrationTestBase):
    """Generic base class for creature-lasergun integration tests.

    Any creature project (lasershark, laserwhale, etc.) can inherit from this
    and provide a creature factory to test integration with LaserGun.

    Example:
        class LaserSharkIntegrationTest(GenericCreatureIntegrationTest):
            def create_creature(self):
                return LaserShark("Sharky", species="Great White")
    """

    def create_creature(self):
        """Create and return creature instance.

        Override this in subclasses to provide specific creature implementations.
        Default returns generic CreatureBase.
        """
        creature = CreatureBase("TestCreature", "Generic")
        self.components["creature"] = creature
        return creature

    def assert_creature_has_laser(self, creature):
        """Assert creature has laser equipped."""
        self.assert_true(creature.has_laser(), "Creature should have laser equipped")

    def assert_creature_without_laser(self, creature):
        """Assert creature does not have laser."""
        self.assert_false(creature.has_laser(), "Creature should not have laser")

    def assert_target_acquired(self, creature):
        """Assert creature has target acquired."""
        self.assert_true(creature.target_acquired, "Creature should have target acquired")

    def assert_target_not_acquired(self, creature):
        """Assert creature has not acquired target."""
        self.assert_false(creature.target_acquired, "Creature should not have target acquired")

    def assert_creature_operational(self, creature):
        """Assert creature is fully operational."""
        self.assert_true(creature.is_operational(),
                        "Creature should be operational (alive, has laser, target acquired)")

    def assert_creature_health(self, creature, expected_health):
        """Assert creature has specific health."""
        self.assert_equals(creature.health, expected_health,
                          f"Creature health should be {expected_health}")

    def assert_creature_alive(self, creature):
        """Assert creature is alive."""
        self.assert_true(creature.is_alive, "Creature should be alive")

    def assert_creature_dead(self, creature):
        """Assert creature is dead."""
        self.assert_false(creature.is_alive, "Creature should be dead")

