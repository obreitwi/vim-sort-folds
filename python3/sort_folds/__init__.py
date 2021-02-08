#!/usr/bin/env python3
# encoding: utf-8
#
# sort_folds/__init__.py - Sort closed folds based on first line
# Maintainer:   Oliver Breitwieser
#

__all__ = [
    "print_debug_info",
    "register_key_function" "sort_folds",
]

__version__ = "1.1.0"

from . import key_functions
from .sort import sort_folds
from .debug import print_debug_info


def register_key_function(function):
    """
    Register the given function as key function to be used for fold sorting.

    :param function: Function to register as key function.
    """
    key_functions.register(function)
