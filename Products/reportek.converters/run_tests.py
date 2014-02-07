#!/usr/bin/env python


if __name__ == '__main__':
    from path import path
    import nose
    nose.main(argv=['run_tests.py', str(path(__file__).parent / 'tests')])
