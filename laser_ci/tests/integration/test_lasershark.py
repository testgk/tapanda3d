import os
from conftest import find_files


def test_lasershark_initialization( install_dir ):
    assert os.path.isdir( install_dir )
    assert any( find_files( install_dir, '*lasershark*' ) ), \
        'no lasershark artifacts found in install dir'


def test_lasershark_build( lib_dir ):
    libs = find_files( lib_dir, '*lasershark*' )
    assert libs, f'no lasershark library found in {lib_dir}'


def test_lasershark_dependencies( lib_dir ):
    lasergun = find_files( lib_dir, '*lasergun*' )
    assert lasergun, f'lasergun dependency not found in {lib_dir}'


def test_lasershark_integration( install_dir, lib_dir, include_dir ):
    libs = find_files( lib_dir, '*lasershark*' )
    headers = find_files( include_dir, '*.h' )
    cmake_files = find_files( install_dir, '*.cmake' )
    assert libs, 'lasershark library missing'
    assert headers, 'header files missing'
    assert cmake_files, 'cmake config files missing'
