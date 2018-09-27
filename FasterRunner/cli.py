# encoding: utf-8

import argparse

from httprunner import logger

from FasterRunner.__about__ import __description__, __version__


def main_hrun():
    """ API test: parse command line options and run commands.
    """
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument(
        '-V', '--version', dest='version', action='store_true',
        help="show version")

    args = parser.parse_args()

    if args.version:
        logger.color_print("{}".format(__version__), "GREEN")
        exit(0)
