"""
LaserGun Test Package

A modular test package for laser gun functionality.
Can be used as a library in other project pipelines.

Test Categories:
- sanity: Basic functionality tests
- performance: Speed and efficiency tests
- memoryleak: Memory leak detection tests
- integration: Component integration tests
- stress: Load and stress tests
- regression: Previously known bug tests
"""

__version__ = "1.0.0"
__author__ = "Laser CI Team"

from .base import BaseLaserGunTest

__all__ = ["BaseLaserGunTest"]

