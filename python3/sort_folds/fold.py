#!/usr/bin/env python3
# encoding: utf-8

import vim

from . import config
from .utils import normal, cursor_preserving


class Fold(object):
    """
    Object representing a fold in the current buffer.
    """
    def __init__(self, start, *, end=None, length=None, buffer=None):
        """
            Create a new Fold.

            :param start:   starting line (int, 0-indexed)
            :param end:     first line _after_ the fold (int, 0-indexed)
            :param length:  length of the fold.
            :param buffer:  Supply an explicit buffer for which to create the fold.
                            Defaults to vim.current.buffer.
        """
        if end is None and length is None:
            raise ValueError("Need to specify either end or length.")
        elif end is not None and length is not None:
            raise ValueError("Cannot specify both end and length.")

        if buffer is None:
            buffer = vim.current.buffer

        if length is None:
            # NOTE: The range methods expect 1-indexed line numbers -> translate
            self._range = buffer.range(start+1, end)
        else:
            # NOTE: The range methods expect 1-indexed line numbers and is inclusive:
            # the last line included is therefore `<translated start> + length - 1`
            # where `<translated start> = start + 1`.
            self._range = buffer.range(start+1, start+length)

        self._level = get_foldlevel_at(self.start)

    @property
    def start(self):
        ":return: Starting line of fold."
        return self._range.start

    @property
    def end(self):
        ":return: First line not part of fold."
        return self._range.end

    @property
    def level(self):
        ":return: Level of fold."
        return self._level

    def __getitem__(self, idx_or_slice):
        if isinstance(idx_or_slice, slice):
            lines = []
            start, stop, step = idx_or_slice.indices(len(self))
            for idx in range(start, stop, step):
                lines.append(self._range[idx])
        else:
            # regular index
            return self._range[idx_or_slice]

    def __iter__(self):
        return self._range.__iter__()

    def __len__(self):
        return self.end - self.start


def get_foldlevel_at(lineno):
    "Get foldlevel for given line number in current buffer."
    return int(vim.eval("foldlevel({})".format(lineno)))


@cursor_preserving
def get_folds():
    """
    Map visible folds in the appropriate area [start, end].

    We step through the region until we leave it or run out of folds.
    """
    cr = vim.current.range
    # set to starting line
    fold_start = cr.start
    fold_end = -1
    # adjust for line numbers starting at one
    normal(cr.start + 1)

    def move_to_next_fold():
        """
        Advance to next fold and return line number.

        :return: line number of next fold (0-indexed).
        """
        normal("zj")
        # adjust for line numbers starting at one
        return int(vim.eval("line('.')"))-1

    while fold_end < cr.end:
        fold_end = min(move_to_next_fold(), cr.end)

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

        fold = Fold(start=fold_start, end=fold_end)

        if len(fold) > 0:
            yield fold

        fold_start = fold_end
