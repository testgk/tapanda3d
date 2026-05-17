# LaserGun Test Package - Quick Start

## Basic Usage

### Run All Tests
```bash
cd /path/to/laser_ci
pytest tests/laser_gun -v
```

### Run by Category
```bash
# Sanity tests only
pytest tests/laser_gun/sanity -v

# Performance tests only
pytest tests/laser_gun/performance -v

# Using markers
pytest tests/laser_gun -m sanity -v
pytest tests/laser_gun -m performance -v
```

### Quick Commands
```bash
# Verbose output
pytest tests/laser_gun -v

# Show print statements
pytest tests/laser_gun -s -v

# Stop on first failure
pytest tests/laser_gun -x -v

# Run last failed tests
pytest tests/laser_gun --lf -v

# Coverage report
pytest tests/laser_gun --cov=tests.laser_gun --cov-report=html

# Specific test
pytest tests/laser_gun/sanity/test_sanity_mock.py::TestLaserGunSanityMock::test_laser_gun_fire -v
```

## Using in Another Project

### 1. Add to requirements.txt
```
laser_gun @ file:///path/to/laser_ci/tests/laser_gun
```

### 2. Install
```bash
pip install -r requirements.txt
```

### 3. Use in Your Tests
```python
from tests.laser_gun.sanity import SanityTestBase

class MyCustomSanityTest(SanityTestBase):
    def test_my_scenario(self):
        lg = self.create_laser_gun()
        # Your test logic here
```

## Test Output Example

```
tests/laser_gun/sanity/test_sanity_mock.py::TestLaserGunSanityMock::test_laser_gun_initialization PASSED
[STEP] INIT - Creating laser gun
[STEP] VERIFY - Checking initialization state
✓ Laser gun initialized successfully

tests/laser_gun/performance/test_performance_mock.py::TestLaserGunPerformanceMock::test_laser_gun_fire_speed PASSED
[STEP] INIT - Creating laser gun
[STEP] BENCHMARK - Measuring fire speed
Timer 'fire_speed': 0.0045s
[STEP] VERIFY - Checking fire speed threshold
✓ Fire speed: 22222 shots/second
```

## Conftest Fixtures

Available pytest fixtures in `conftest.py`:

```python
@pytest.fixture
def mock_laser_gun():
    """Pre-configured mock laser gun instance"""
    
@pytest.fixture
def logger():
    """Logger instance for tests"""
    
@pytest.fixture(scope="session")
def test_data_dir():
    """Path to test data directory"""
```

## Base Test Methods

All test classes inherit these helpful methods:

### Logging
- `log_step(name, message="")`
- `log_info(message)`
- `log_warning(message)`
- `log_error(message)`

### Assertions
- `assert_not_none(value, message="")`
- `assert_equals(actual, expected, message="")`
- `assert_true(value, message="")`
- `assert_false(value, message="")`
- `assert_greater_than(actual, threshold, message="")`
- `assert_less_than(actual, threshold, message="")`
- `assert_in_range(value, min, max, message="")`

### Lifecycle
- `setup_method()` - Runs before each test
- `teardown_method()` - Runs after each test

## Example: Create Custom Sanity Test

```python
import pytest
from tests.laser_gun.sanity import SanityTestBase

@pytest.mark.sanity
class TestCustomScenario(SanityTestBase):
    def test_custom_firing_pattern(self):
        # Setup
        self.log_step("INIT", "Creating laser gun")
        lg = self.create_laser_gun()
        
        # Configure
        self.log_step("CONFIG", "Setting power")
        lg.set_power(85.0)
        
        # Execute
        self.log_step("FIRE", "Firing at sequence")
        for i in range(10):
            lg.fire(target=f"target_{i}")
        
        # Verify
        self.log_step("VERIFY", "Checking results")
        self.assert_equals(lg.fired_count, 10, "Should fire 10 times")
        self.log_info("✓ Custom firing pattern successful")
```

Run it:
```bash
pytest tests/laser_gun/sanity/test_sanity_mock.py::TestCustomScenario::test_custom_firing_pattern -v
```

