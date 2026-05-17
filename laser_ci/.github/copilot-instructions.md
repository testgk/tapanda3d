# Laser Project Copilot Instructions

## Architecture Overview
This is a multi-component laser simulation system with C++ core libraries and Python API:

- **creatures**: C++ base classes for aquatic/land creatures (Creature → AquaticCreature/LandCreature → Shark/Whale)
- **lasergun**: C++ laser weapon component
- **brain_implant**: C++ neural interface component  
- **lasershark/laserwhale**: C++ executable creatures with laser capabilities
- **laser_api**: Python FastAPI REST API for controlling lasers (simulation/hardware modes)
- **laser_ci**: CMake orchestration project that links all C++ components
- **laser_tests**: pytest test suite with build/integration testing

## Build System & Dependencies
- **Package Management**: All C++ components use CMake `find_package()` with installed packages in `laser_ci/install/`
- **Build Order**: creatures → lasergun → brain_implant → lasershark → laserwhale → laser_ci
- **Include Style**: Use angle brackets `<LaserGun.h>` (not quotes) - CMake configures paths automatically
- **CMAKE_PREFIX_PATH**: Always set to `laser_ci/install/` when building dependent projects

## Critical Workflows
- **Full Build**: From `laser_ci/`, run `./scripts/local-build-test.sh` (clones and builds all components)
- **Individual Component**: `cd <component>; mkdir build; cd build; cmake -DCMAKE_PREFIX_PATH=../../laser_ci/install ..; cmake --build . --config Release`
- **API Development**: `cd laser_api; pip install -r requirements.txt; python main.py` (runs on port 8000)
- **Testing**: `cd laser_tests; pip install -r requirements.txt; pytest` (supports `--cov` for coverage)
- **CI Build**: Components build as external projects downloading deps from registry via `laser_ci/scripts/download-from-registry.sh`

## Code Patterns
- **C++ Classes**: Follow creature hierarchy - inherit from base classes in `creatures/` library
- **Python API**: Use FastAPI with Pydantic models; simulator supports hardware mode via ctypes DLL loading
- **DLL Integration**: `cpp_integration.py` wraps C++ DLLs (e.g., `lasershark.dll`) using ctypes for hardware control
- **CMake Targets**: Each component exports targets for `find_package()` consumption

## Integration Points
- **Hardware Interface**: API switches to real hardware when `hardware_mode=True` and DLLs available
- **Cross-Component**: lasershark depends on creatures + lasergun; laserwhale depends on creatures
- **CI/CD**: GitLab CI with local testing via `laser_ci/scripts/` build scripts

## Key Files
- `laser_api/main.py`: FastAPI app with laser simulator
- `laser_ci/CMakeLists.txt`: Main project linking all components  
- `creatures/creatures.h`: Creature class hierarchy
- `laser_tests/tests/lasershark/test_lasershark.py`: Example test structure</content>
<parameter name="filePath">c:\Users\GADKL\Projects\laser_project\.github\copilot-instructions.md