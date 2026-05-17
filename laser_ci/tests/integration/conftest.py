import os
import pytest

INSTALL_DIR = os.environ.get( 'INSTALL_DIR', 'install' )

@pytest.fixture( scope='session' )
def install_dir():
    if not os.path.isdir( INSTALL_DIR ):
        pytest.skip( f'install directory not found: {INSTALL_DIR}' )
    return INSTALL_DIR

@pytest.fixture( scope='session' )
def lib_dir( install_dir ):
    d = os.path.join( install_dir, 'lib' )
    if not os.path.isdir( d ):
        pytest.skip( 'install/lib not found' )
    return d

@pytest.fixture( scope='session' )
def include_dir( install_dir ):
    d = os.path.join( install_dir, 'include' )
    if not os.path.isdir( d ):
        pytest.skip( 'install/include not found' )
    return d

def find_files( directory, pattern ):
    import fnmatch
    matches = []
    for root, _, files in os.walk( directory ):
        for f in files:
            if fnmatch.fnmatch( f, pattern ):
                matches.append( os.path.join( root, f ) )
    return matches
