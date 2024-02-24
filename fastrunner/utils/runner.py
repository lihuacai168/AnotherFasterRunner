#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys
import tempfile

from FasterRunner.settings.base import BASE_DIR
from fastrunner.utils import loader

EXEC = sys.executable

if "uwsgi" in EXEC:
    # 修复虚拟环境下，用uwsgi执行时，PYTHONPATH还是用了系统默认的
    EXEC = EXEC.replace("uwsgi", "python")


class DebugCode(object):
    def __init__(self, code):
        self.__code = code
        self.resp = None
        self.temp = tempfile.mkdtemp(prefix="FasterRunner")

    def run(self):
        """dumps debugtalk.py and run"""
        try:
            os.chdir(self.temp)
            file_path = os.path.join(self.temp, "debugtalk.py")
            loader.FileLoader.dump_python_file(file_path, self.__code)
            # 修复驱动代码运行时，找不到内置httprunner包
            run_path = [BASE_DIR]
            run_path.extend(sys.path)
            env = {"PYTHONPATH": ":".join(run_path)}
            self.resp = decode(
                subprocess.check_output([EXEC, file_path], stderr=subprocess.STDOUT, timeout=60, env=env)
            )

        except subprocess.CalledProcessError as e:
            self.resp = decode(e.output)

        except subprocess.TimeoutExpired:
            self.resp = "RunnerTimeOut"
        os.chdir(BASE_DIR)
        shutil.rmtree(self.temp)


def decode(s):
    try:
        return s.decode("utf-8")

    except UnicodeDecodeError:
        return s.decode("gbk")
