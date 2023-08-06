# -*- coding: utf-8 -*-
"""auxiliary library to the python standard library"""
from __future__ import absolute_import, division, print_function
from logging import getLogger, StreamHandler, INFO

# don't mess up logging for users
log = getLogger(__name__)
log.addHandler(StreamHandler())
log.setLevel(INFO)

from .packaging import BuildPyCommand, SDistCommand, Tox, get_version  # NOQA

__all__ = [
    "__title__", "__version__", "__author__",
    "__email__", "__license__", "__copyright__",
    "__summary__", "__homepage__",
    "BuildPyCommand", "SDistCommand", "Tox", "get_version",
]

__version__ = "custom"

__title__ = "auxlib"
__author__ = 'Kale Franz'
__email__ = 'kale@franz.io'
__homepage__ = 'https://github.com/kalefranz/auxlib'
__license__ = "ISC"
__copyright__ = "(c) 2015 Kale Franz. All rights reserved."
__summary__ = __doc__
