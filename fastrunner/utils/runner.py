#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import subprocess
import tempfile
from fastrunner.utils import loader

EXEC = sys.executable

if 'uwsgi' in EXEC:
    EXEC = "/usr/bin/python3"


class DebugCode(object):

    def __init__(self, code):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix='FasterRunner')

    def run(self):
        """ dumps debugtalk.py and run
        """
        try:
            file_path = os.path.join(self.temp, "debugtalk.py")
            loader.FileLoader.dump_python_file(file_path, self.__code)
            self.resp = decode(subprocess.check_output([EXEC, file_path], stderr=subprocess.STDOUT, timeout=60))

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = 'RunnerTimeOut'

        shutil.rmtree(self.temp)


def decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')
