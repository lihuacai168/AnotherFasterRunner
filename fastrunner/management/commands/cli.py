# encoding: utf-8

# -*- coding:utf-8 -*-
from django.core.management.base import BaseCommand

from httprunner import logger

from FasterRunner.__about__ import __version__


class Command(BaseCommand):
    def add_arguments(self, parser):
        """ API test: parse command line options and run commands.
            """
        parser.add_argument(
            '-V', '--Version', dest='version', action='store_true',
            help="show version")

    def handle(self, *args, **options):
        if options['version']:
            logger.color_print("{}".format(__version__), "GREEN")
            exit(0)
