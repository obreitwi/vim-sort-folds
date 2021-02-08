#!/usr/bin/env python3
# encoding: utf-8

"""
Module to extract user settings from vim.
"""


import vim


def get_fold_to_sort_key(sort_line):
    ignore_case = vim.eval("g:sort_folds_ignore_case")
    if ignore_case == "0":
        return lambda f: f[sort_line]
    else:
        return lambda f: f[sort_line].casefold()
