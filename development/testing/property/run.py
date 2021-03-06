#!/usr/bin/env python
""" Script to start development test battery for the RESPY package.
"""
from datetime import timedelta
from datetime import datetime
import numpy as np
import traceback
import importlib
import argparse
import random
import sys
import os

# RESPY testing codes. The import of the PYTEST configuration file ensures
# that the PYTHONPATH is modified to allow for the use of the tests..
PACKAGE_DIR = os.path.dirname(os.path.realpath(__file__))
PACKAGE_DIR = PACKAGE_DIR.replace('development/testing/property', '')

# PYTEST ensures the path is set up correctly.
sys.path.insert(0, PACKAGE_DIR + 'respy/tests')
sys.path.insert(0, PACKAGE_DIR)
sys.path.insert(0, '../_modules')

from auxiliary_property import cleanup_testing_infrastructure
from auxiliary_property import initialize_record_canvas
from auxiliary_property import finalize_testing_record
from auxiliary_property import update_testing_record
from auxiliary_property import get_random_request
from auxiliary_property import get_test_dict
from auxiliary_property import get_testdir
from auxiliary_shared import send_notification
from auxiliary_shared import compile_package
from auxiliary_shared import cleanup


def run(args):
    """ Run the property test battery.
    """
    cleanup()

    if args.is_compile:
        compile_package(True)

    # Get a dictionary with all candidate test cases.
    test_dict = get_test_dict(PACKAGE_DIR + 'respy/tests')

    # We initialize a dictionary that allows to keep track of each test's
    # success or failure.
    full_test_record = dict()
    for key_ in test_dict.keys():
        full_test_record[key_] = dict()
        for value in test_dict[key_]:
            full_test_record[key_][value] = [0, 0]

    # Start with a clean slate.
    start, timeout = datetime.now(), timedelta(hours=args.hours)
    cleanup_testing_infrastructure(False)
    initialize_record_canvas(full_test_record, start, timeout)

    # Evaluation loop.
    while True:

        # Set seed.
        seed = random.randrange(1, 100000)
        np.random.seed(seed)

        # Construct test case.
        module, method = get_random_request(test_dict)
        mod = importlib.import_module(module)
        test = getattr(mod.TestClass(), method)

        # Run random test
        is_success, msg = None, None

        # Create a fresh test directory.
        tmp_dir = get_testdir(5)

        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)

        try:
            test()
            full_test_record[module][method][0] += 1
            is_success = True
        except Exception:
            full_test_record[module][method][1] += 1
            msg = traceback.format_exc()
            is_success = False

        # The directory is deleted by the cleanup
        os.chdir('../')

        # Record iteration
        update_testing_record(module, method, seed, is_success, msg,
            full_test_record)
        cleanup_testing_infrastructure(True)

        #  Timeout.
        if timeout < datetime.now() - start:
            break

    finalize_testing_record(full_test_record)

    # This allows to call this test from another script, that runs other
    # tests as well.
    if not args.is_background:
        send_notification('property', hours=args.hours)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run development test '
                'battery of RESPY package.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--hours', action='store', dest='hours',
                        type=float, default=1.0, help='run time in hours')

    parser.add_argument('--compile', action='store_true', dest='is_compile',
        default=False, help='compile RESPY package')

    parser.add_argument('--background', action='store_true',
        dest='is_background', default=False, help='background process')

    run(parser.parse_args())

