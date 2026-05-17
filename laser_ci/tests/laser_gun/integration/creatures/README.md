# Creatures Integration Framework

## Overview

The Creatures Integration Framework is a generic, reusable pattern for testing creature-LaserGun integration across multiple projects (LaserShark, LaserWhale, and other animals that use LaserGun).

## Architecture

```
tests/laser_gun/integration/creatures/

├── __init__.py                  # Generic framework base classes
│   ├── CreatureBase             # Mock creature base (for all creatures)
│   └── GenericCreatureIntegrationTest  # Generic test base
│
├── lasershark.py               # LaserShark-specific implementation
│   ├── LaserShark              # LaserShark mock creature
│   ├── LaserSharkIntegrationTest    # Base for shark tests
│   └── Test classes             # Concrete shark test scenarios
│
├── TEMPLATE.py                 # Template for other creature projects
└── README.md                   # This file
```

## Core Components

### 1. CreatureBase (Mock Creature)

Base mock class that represents any creature integrating with LaserGun.

**Features:**
- Basic attributes: `name`, `species`, `health`, `is_alive`
- Laser integration: `equip_laser()`, `unequip_laser()`, `has_laser()`
- Target system: `acquire_target()`, `lose_target()`, `target_acquired`
- Combat: `fire_laser()`, `take_damage()`, `is_operational()`

**Properties:**
```python
creature.name              # Creature name
creature.species           # Species type
creature.health            # Current health (0-100)
creature.is_alive          # Alive status
creature.equipped_laser    # Reference to equipped laser gun
creature.current_target    # Current target name/id
creature.target_acquired   # Boolean: has target locked
```

**Methods:**
```python
creature.equip_laser(laser_gun)     # Attach laser to creature
creature.unequip_laser()             # Remove laser
creature.has_laser()                 # Check if armed
creature.acquire_target(target)      # Lock onto target
creature.lose_target()               # Release target
creature.fire_laser()                # Fire equipped laser at target
creature.take_damage(amount)         # Reduce health
creature.is_operational()            # All systems go? (armed + target + alive)
```

### 2. GenericCreatureIntegrationTest

Generic test base that any creature project can inherit from.

**Base Assertions:**
```python
self.assert_creature_has_laser(creature)       # Has laser equipped
self.assert_creature_without_laser(creature)   # No laser
self.assert_target_acquired(creature)          # Target locked
self.assert_target_not_acquired(creature)      # No target
self.assert_creature_operational(creature)     # All systems operational
self.assert_creature_health(creature, value)   # Specific health
self.assert_creature_alive(creature)           # Creature alive
self.assert_creature_dead(creature)            # Creature dead
```

**Override Methods:**
```python
def create_creature(self):
    """Must override to provide your creature implementation."""
    # Return your creature instance
```

**Inherited Methods:**
- All `IntegrationTestBase` methods (logging, step tracking)
- All `BaseLaserGunTest` methods (assertions, lifecycle)
- Target and component management

### 3. LaserShark Implementation Example

Shows how to create creature-specific integration tests.

**Structure:**
```python
# 1. Define creature class
class LaserShark(CreatureBase):
    def __init__(self, name, species):
        super().__init__(name, species)
        self.bite_force = 4000
        self.predator_rating = 9.5

# 2. Create test base
class LaserSharkIntegrationTest(GenericCreatureIntegrationTest):
    def create_creature(self):
        shark = LaserShark(name="TestShark", species="Great White")
        self.components["shark"] = shark
        return shark
    
    # Add shark-specific assertions
    def assert_shark_ferocity(self, shark, rating):
        self.assert_equals(shark.predator_rating, rating)

# 3. Create test classes
@pytest.mark.integration
class TestLaserSharkBasicIntegration(LaserSharkIntegrationTest):
    def test_laser_shark_equips_laser(self):
        # Test implementation
```

**Test Categories in LaserShark:**

1. **Basic Integration** (3 tests)
   - Equip laser gun
   - Target acquisition
   - Firing at target

2. **Advanced Integration** (3 tests)
   - Multi-target engagement
   - Fire without target (negative test)
   - Damage system

3. **Synchronized Integration** (1 test)
   - Coordinated firing with target tracking

## For Other Creature Projects

### Step-by-Step Implementation

#### 1. Import the Framework
```python
from tests.laser_gun.integration.creatures import (
    GenericCreatureIntegrationTest, 
    CreatureBase
)
```

#### 2. Define Your Creature
```python
class LaserWhale(CreatureBase):
    def __init__(self, name="Whale", species="Blue Whale"):
        super().__init__(name, species)
        self.echolocation_range = 1000  # meters
        self.sonar_active = False
        self.intelligence_rating = 9.8
    
    def use_echolocation(self):
        self.sonar_active = True
        # Find nearby targets using sonar
```

#### 3. Create Test Base Class
```python
class LaserWhaleIntegrationTest(GenericCreatureIntegrationTest):
    def create_creature(self):
        whale = LaserWhale()
        self.components["whale"] = whale
        return whale
    
    def assert_whale_intelligent(self, whale):
        self.assert_greater_than(whale.intelligence_rating, 9.0)
    
    def assert_whale_sonar_active(self, whale):
        self.assert_true(whale.sonar_active)
```

#### 4. Write Your Tests
```python
@pytest.mark.integration
class TestLaserWhaleIntegration(LaserWhaleIntegrationTest):
    def test_whale_uses_echolocation_to_find_targets(self):
        self.log_step("INIT", "Creating whale")
        whale = self.create_creature()
        
        self.log_step("EQUIP", "Equipping laser")
        lg = self.create_laser_gun()
        whale.equip_laser(lg)
        
        self.log_step("SONAR", "Activating echolocation")
        whale.use_echolocation()
        
        self.log_step("VERIFY", "Checking sonar and equipment")
        self.assert_whale_sonar_active(whale)
        self.assert_creature_has_laser(whale)
        self.log_info("✓ Whale echolocation with laser ready")
```

#### 5. Copy and Customize Template
- Copy `TEMPLATE.py` or `lasershark.py` as reference
- Replace `OtherCreature` with your creature class
- Update test methods for your specific scenarios
- Add creature-specific assertions

## Test Inheritance Chain

```
BaseLaserGunTest
    ↓
IntegrationTestBase (adds component management)
    ↓
GenericCreatureIntegrationTest (adds creature integration)
    ↓
LaserSharkIntegrationTest (shark-specific base)
    ↓
TestLaserSharkBasicIntegration (concrete tests)
```

## Running Tests

### All Creature Integration Tests
```bash
pytest tests/laser_gun/integration/creatures -v
```

### Only LaserShark Tests
```bash
pytest tests/laser_gun/integration/creatures/lasershark.py -v
```

### Specific Test Class
```bash
pytest tests/laser_gun/integration/creatures/lasershark.py::TestLaserSharkBasicIntegration -v
```

### With Verbose Logging
```bash
pytest tests/laser_gun/integration/creatures/lasershark.py -v -s
```

## Design Patterns

### Pattern 1: Generic Base → Specific Implementation
```python
# Generic
GenericCreatureIntegrationTest
    ↓
# Specific
LaserSharkIntegrationTest  # ← LaserShark override
    ↓
# Concrete
TestLaserSharkBasicIntegration  # ← Actual tests
```

### Pattern 2: CreatureBase → Custom Creature
```python
# Base mock
CreatureBase  # fire_laser(), equip_laser(), take_damage(), etc.
    ↓
# Custom
LaserShark  # Add bite_force, predator_rating, etc.
```

### Pattern 3: Reusable Assertions
```python
# Generic assertions (available in all test classes)
self.assert_creature_operational(creature)
self.assert_creature_has_laser(creature)

# Creature-specific assertions (define in your test base)
self.assert_shark_ferocity(shark, 9.5)
self.assert_whale_intelligent(whale)
```

## Best Practices

1. **Keep CreatureBase Generic** - Don't add game-specific logic
2. **Override create_creature()** - Every creature project must implement this
3. **Add Species-Specific Assertions** - Create `assert_whale_*()` style methods
4. **Test Integration, Not Creatures** - Focus on creature↔laser interaction
5. **Reuse Generic Tests** - Inherit test methods from GenericCreatureIntegrationTest
6. **Document Custom Features** - Explain creature-specific behaviors in tests

## Expected Test Output

```
tests/laser_gun/integration/creatures/lasershark.py::TestLaserSharkBasicIntegration::test_laser_shark_equips_laser PASSED
INFO - [STEP] INIT - Creating LaserShark
INFO - [STEP] CREATE_LASER - Creating laser gun
INFO - [STEP] EQUIP - Equipping laser to shark
INFO - [STEP] VERIFY - Checking shark has laser
INFO - ✓ LaserShark equipped with laser gun
```

## Current Status

✅ **Generic Framework**: Complete
✅ **LaserShark Implementation**: Complete with 7 tests
✅ **Template**: Provided for other projects
✅ **Documentation**: This file

## Next Steps for Other Projects

1. Copy `TEMPLATE.py` or `lasershark.py`
2. Adapt for your creature
3. Implement `create_creature()`
4. Add creature-specific tests
5. Run and validate

---

**This framework enables any creature project to test LaserGun integration consistently and reusably! 🦈🐋**

