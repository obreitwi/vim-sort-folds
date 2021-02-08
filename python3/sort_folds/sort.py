#!/usr/bin/env python3
# encoding: utf-8

import itertools as it
import vim

from . import fold, config


def sort_folds(sort_line=0):
    """
    Get all folds in the current buffer and sort them.

    :param sort_line: Line by which to sort each fold.
                      Ignored if 'g:sort_folds_key_function' is defined in vim.
    """
    key_function = config.get_key_function()
    if key_function is None:
        key_function = config.get_fold_to_sort_key(sort_line)

    sorted_folds = sorted(fold.get_folds(), key=key_function)
    sorted_lines = list(it.chain.from_iterable(sorted_folds))
    vim.current.range[:] = sorted_lines
