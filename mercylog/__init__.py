# -*- coding: utf-8 -*-

"""Top-level package for mercy."""

__author__ = """Rajiv Abraham"""
__email__ = 'rajiv.abraham@gmail.com'
__version__ = '0.1.0'

from .bashlog import BashlogV1
from mercylog.db import db
from mercylog.types import relation, _,  Variable,V, R, Q
from mercylog.operations import or_
