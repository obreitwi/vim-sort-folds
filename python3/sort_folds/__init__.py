#!/usr/bin/env python3
# encoding: utf-8
#
# sort_folds/__init__.py - Sort closed folds based on first line
# Maintainer:   Oliver Breitwieser
#

__all__ = [
        "print_debug_info",
        "sort_folds",
    ]

__version__ = "1.1.0"


from .sort import sort_folds
from .debug import print_debug_info
