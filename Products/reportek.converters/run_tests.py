#!/usr/bin/env python


if __name__ == '__main__':
    import sys
    import unittest
    from path import Path

    tests_path = str(Path(__file__).parent / 'tests')
    suite = unittest.defaultTestLoader.discover(tests_path, pattern='*_test.py')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
