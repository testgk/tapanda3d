import os
from conftest import find_files


def test_lasergun_weapon_systems( lib_dir ):
    libs = find_files( lib_dir, '*lasergun*' )
    assert libs, f'no lasergun library found in {lib_dir}'


def test_lasergun_power_management( install_dir ):
    cmake_files = find_files( install_dir, '*lasergun*.cmake' )
    assert cmake_files, 'lasergun cmake config missing — power management config unavailable'


def test_lasergun_safety_systems( lib_dir ):
    libs = find_files( lib_dir, '*lasergun*' )
    assert libs, 'lasergun library missing — safety systems cannot be verified'


def test_lasergun_calibration( install_dir ):
    cmake_files = find_files( install_dir, '*.cmake' )
    assert cmake_files, 'cmake config missing — calibration data unavailable'


def test_lasergun_maintenance_mode( install_dir, lib_dir ):
    libs = find_files( lib_dir, '*lasergun*' )
    assert libs, 'lasergun library missing'
    assert os.path.isdir( install_dir ), 'install directory missing'
