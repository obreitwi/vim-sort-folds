#!/usr/bin/env python3
# encoding: utf-8
#
# sort_folds/__init__.py - Sort closed folds based on first line
# Maintainer:   Oliver Breitwieser
#

from __future__ import print_function

import itertools as it

import vim


__all__ = [
        "debug",
        "print_foldlevel"
        "sort_folds",
    ]

__version__ = "1.1.0"


class Fold(object):
    """
        Object representing a fold in the current buffer.
    """
    def __init__(self, level, start, *, end=None, length=None):
        """
            Create a new Fold.

            :param level:   fold level (int)
            :param start:   starting line (int)
            :param end:     first line _after_ the fold
            :param length:  length of the fold.
        """
        if end is None and length is None:
            raise ValueError("Need to specify either end or length.")
        elif end is not None and length is not None:
            raise ValueError("Cannot specify both end and length.")

        self._level = level
        self._start = start

        if length is None:
            self._end = end
        else:
            self._end = self.start + length

    @property
    def start(self):
        ":return: Starting line of fold."
        return self._start

    @property
    def end(self):
        ":return: First line not part of fold."
        return self._end

    @property
    def level(self):
        ":return: Level of fold."
        return self._level

    def __len__(self):
        return self.end - self.start

    def __getitem__(self, line_number):
        return vim.current.buffer[self.start + line_number]

    @property
    def lines(self):
        for line in vim.current.buffer[self.start:self.end]:
            yield line


def debug(sorting_line_number=1):
    """
        Print debug information about how folds are extracted and sorted.
    """
    print("###############")
    print("#  Extracted  #")
    print("###############")

    print_folds(get_folds())

    print("############")
    print("#  Sorted  #")
    print("############")

    sorted_folds = sorted(get_folds(),
                          key=get_fold_to_sort_key(sorting_line_number))
    print_folds(sorted_folds)


def get_foldlevel(lineno):
    "Get foldlevel for given line number in current buffer."
    return int(vim.eval("foldlevel({})".format(lineno)))


def get_folds():
    """
        Map visible folds in the appropriate area [start, end].

        We step through the region until we leave it or run out of folds.
    """
    cr = vim.current.range
    # restore cursor position
    pos = vim.current.window.cursor

    # set to starting line
    fold_start = cr.start
    fold_end = -1
    # adjust for line numbers starting at one
    normal(cr.start + 1)

    def next_fold():
        "Advance to next fold and return line number."
        normal("zj")
        # adjust for line numbers starting at one
        return int(vim.eval("line('.')"))-1

    while fold_end != cr.end:
        fold_end = min(next_fold(), cr.end)

        if fold_end < fold_start:
            # we are iterating on the last fold, which is closed, therefore we
            # seem to jump back in lines -> we are done
            break

        if fold_end == fold_start:
            # If we ran out of folds, just put everything till the end in a
            # pseudo fold
            fold_end = cr.end

        if fold_end == cr.end:
            # adjust for having reached the end
            fold_end += 1

        fold = Fold(level=get_foldlevel(fold_start),
                    start=fold_start,
                    end=fold_end)

        if len(fold) > 0:
            yield fold

        fold_start = fold_end

    # restore cursor position
    vim.current.window.cursor = pos


def line_range_to_foldlevel(start, end):
    """
        Get the fold level for all lines in [start, end] in the current buffer.

        (Unfortunately, this is not enough to find all folds, as adjacent folds
        can have the same line number).
    """
    return map(get_foldlevel, range(start, end+1))


def normal(cmd):
    "Convenience function for unremapped normal commands."
    return vim.command("normal! {}".format(cmd))


def print_foldlevel():
    """
        Print foldlevel of fall lines in current range.
    """
    cr = vim.current.range
    for lvl, line in it.izip(line_range_to_foldlevel(cr.start, cr.end), cr[:]):
        print(lvl, line)


def print_folds(folds):
    """
        Prints all supplied folds for debug purposes.
    """
    for fold in folds:
        print("---")
        for line in fold.lines:
            print(fold.level, line)


def get_fold_to_sort_key(sort_line):
    ignore_case = vim.eval("g:sort_folds_ignore_case")
    if ignore_case == "0":
        return lambda f: f[sort_line]
    else:
        return lambda f: f[sort_line].casefold()


def sort_folds(sort_line=0):
    sorted_folds = sorted(get_folds(), key=get_fold_to_sort_key(sort_line))

    sorted_lines = list(it.chain(*list(map(lambda f: f.lines, sorted_folds))))
    vim.current.range[:] = sorted_lines
