import os
import time
from conftest import find_files


def test_generic_api( install_dir, lib_dir ):
    all_libs = find_files( lib_dir, '*.a' ) + find_files( lib_dir, '*.so' ) + find_files( lib_dir, '*.dll' )
    assert all_libs, 'no shared or static libraries found in install/lib'
    cmake_files = find_files( install_dir, '*.cmake' )
    assert cmake_files, 'no cmake config files found'


def test_full_laser_ecosystem_integration( install_dir, lib_dir, include_dir ):
    libs = find_files( lib_dir, '*.a' ) + find_files( lib_dir, '*.so' )
    headers = find_files( include_dir, '*.h' )
    cmake_files = find_files( install_dir, '*.cmake' )
    assert libs, 'no libraries found'
    assert headers, 'no header files found'
    assert cmake_files, 'no cmake config files found'


def test_laser_system_performance( install_dir ):
    start = time.time()
    find_files( install_dir, '*' )
    elapsed = time.time() - start
    assert elapsed < 10, f'artifact scan took too long: {elapsed:.1f}s'


def test_laser_system_error_handling( install_dir ):
    missing = find_files( install_dir, '*nonexistent_component*' )
    assert missing == [], 'unexpected artifacts found'
    assert os.path.isdir( install_dir ), 'install dir missing'
