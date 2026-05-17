#!/usr/bin/env python3
"""Entry point for integration tests — passes all args through to pytest."""
import os
import sys
import pytest

if __name__ == '__main__':
    sys.exit( pytest.main( [ os.path.dirname( __file__ ), *sys.argv[ 1: ] ] ) )
