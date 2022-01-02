#   -*- coding: utf-8 -*-
import os

from pybuilder.core import use_plugin, init, task

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")

name = "oanda-fxdata-etl"
default_task = "publish"

@init
def set_properties(project):
    os.environ.setdefault('fixtures', "./src/unittest/python/fixtures")