#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
import sys
import os
import subprocess
import tempfile

EXEC = sys.executable


class DebugCode(object):

    def __init__(self, code):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix='debugtalk_')

    def run(self):
        """
        run code
        """
        try:
            file_path = write_py("debugtalk", self.__code, self.temp)
            self.resp = decode(subprocess.check_output([EXEC, file_path], stderr=subprocess.STDOUT, timeout=60))

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = 'RunnerTimeOut'

        shutil.rmtree(self.temp)


def write_py(name, code, path):
    """
    name: str
    code: str
    """
    file_path = os.path.join(path, '%s.py' % name)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)

    return file_path


def decode(s):
    try:
        return s.decode('utf-8')

    except UnicodeDecodeError:
        return s.decode('gbk')
