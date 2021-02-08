#!/usr/bin/env python3
# encoding: utf-8

"""
Module to extract user settings from vim.
"""


from . import key_functions

import vim


def get_fold_to_sort_key(sort_line):
    ignore_case = vim.eval("g:sort_folds_ignore_case")
    if ignore_case == "0":
        return lambda f: f[sort_line]
    else:
        return lambda f: f[sort_line].casefold()


def get_key_function():
    """
    Checks if a cusotm key-function is defined.

    :return: key-function if defined, else None.
    """
    if vim.eval("exists('g:sort_folds_key_function')") == "1":
        function_name = vim.eval("g:sort_folds_key_function")
        try:
            return key_functions.get(function_name)
        except KeyError:
            raise RuntimeError(
                "Could not find custom key-function: {}".format(function_name)
            )
    else:
        print("No key-function defined")
        return None
