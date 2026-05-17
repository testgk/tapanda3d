cmake_minimum_required(VERSION 3.10)
project(laserproject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set install prefix to laser_ci/install if not specified
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(CMAKE_INSTALL_PREFIX "${CMAKE_CURRENT_SOURCE_DIR}/install" CACHE PATH "Install path" FORCE)
endif()

# Add install directory to CMAKE_PREFIX_PATH to find installed packages
list(APPEND CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/install")

# Find all required packages (must be built and installed separately first)
find_package(lasergun REQUIRED)
find_package(lasershark REQUIRED)
