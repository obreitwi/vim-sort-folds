#!/usr/bin/env python3
# encoding: utf-8

import itertools as it
import vim

from . import fold, config


def sort_folds(sort_line=0):
    """
    Get all folds in the current buffer and sort them.

    :param sort_line: Line by which to sort each fold.
    """
    sorted_folds = sorted(fold.get_folds(), key=config.get_fold_to_sort_key(sort_line))

    sorted_lines = list(it.chain(*list(map(lambda f: f, sorted_folds))))
    vim.current.range[:] = sorted_lines
