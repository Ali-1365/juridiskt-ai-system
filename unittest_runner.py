"""
Script to run security unit tests for the Juridiskt AI System
"""

import unittest
import os
import sys
from pathlib import Path

# Add tests directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

if __name__ == "__main__":
    # Discover and run all tests
    test_suite = unittest.defaultTestLoader.discover('tests', pattern='*_tests.py')
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_runner.run(test_suite)