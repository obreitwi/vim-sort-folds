#!/usr/bin/env python2
# encoding: utf-8
#
# SortFolds/__init__.py - Sort closed folds based on first line
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

__version__ = "0.2.0"


class Fold(object):
    """
        Object representing a fold in the current buffer.
    """
    def __init__(self, level, start, end=None, length=None):
        """
            Describes fold of `level` at starting line `start` till line `end`
            (0-index) of length `length`.
        """
        assert end is None or length is None
        assert end is not None or length is not None

        self.level = level
        self.start = start

        if length is None:
            self.end = end
        else:
            self.end = self.start + length

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

    sorted_folds = sorted(get_folds(), key=lambda f: f[sorting_line_number])
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


def merge_folds(folds_gen):
    """
        Merge all folds that are more than one level below the lowest foldlevel
        found.

        This function is unneeded now because foldlevel-based method (see
        _get_folds) does not work as intended. The now in-use method of
        identifying folds relies on folds being closed, but on the other hand
        does not require any merger of folds...
    """
    # copy iterator to find minimum fold level
    find_min, folds_gen = it.tee(folds_gen)

    # the folds we want to sort are one fold level above the minumum we found
    level_to_sort = min(it.imap(lambda l: l.level, find_min)) + 1

    # Depending on what range the user selects, vim will report a different
    # foldlevel for the very first line, leading to undesired behavior.
    # The invariant however is that the first fold should be at a fold level
    # one below the sorting level. If it is not, we have to adjust accordingly.

    fold = folds_gen.next()

    to_merge = [fold]
    level_last = fold.level

    def make_fold(to_merge):
        return Fold(level=level_to_sort,
                    start=to_merge[0].start,
                    length=sum(map(len, to_merge)))

    for fold in folds_gen:
        # we check for exact equality because we want to keep the space between
        # folds aligned with the folds themselves. Otherwise we would have all
        # the whitespace between functions in one place etc.
        # The only time we want to merge a fold at sort level is if we return
        # from a subfold to the current one>
        if fold.level != level_to_sort or level_last > level_to_sort:
            # merge this fold with the previous one
            to_merge.append(fold)

        else:
            # this is toplevel fold we want to keep, so yield everything that
            # was merged till here
            yield make_fold(to_merge)

            to_merge = [fold]
        level_last = fold.level

    # yield the last fold as well
    yield make_fold(to_merge)


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


def sort_folds(sort_line=0):
    sorted_folds = sorted(get_folds(), key=lambda f: f[sort_line])

    sorted_lines = list(it.chain(*it.imap(lambda f: f.lines, sorted_folds)))
    vim.current.range[:] = sorted_lines


def _get_folds():
    """
        Get folds in current range.

        Uses foldlevel for every line to identify folds. Unfortunately does not
        find directly adjacent folds in all cases.
    """
    cr = vim.current.range
    foldlevels = line_range_to_foldlevel(cr.start, cr.end)

    lvl_and_length = map(lambda (lvl, items): (lvl, len(list(items))),
                         it.groupby(foldlevels))

    current_start = cr.start
    for i, (lvl, length) in enumerate(lvl_and_length):
        #  print("Current level:", lvl)
        try:
            prev_level_lower = lvl_and_length[i-1][0] < lvl
            #  print("Prev lvl", lvl_and_length[i-1][0])
        except IndexError:
            prev_level_lower = False

        try:
            next_level_higher = lvl_and_length[i+1][0] > lvl
            #  print("Next lvl", lvl_and_length[i+1][0])
        except IndexError:
            next_level_higher = False

        if next_level_higher != prev_level_lower:
            if next_level_higher:
                length -= 1
            else:
                length += 1

        #  print("Resulting length", length)

        if length > 0:
            yield Fold(level=lvl, start=current_start, length=length)
            current_start += length
