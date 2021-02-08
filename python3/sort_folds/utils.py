#!/usr/bin/env python3
# encoding: utf-8

import vim
from contextlib import contextmanager


def normal(cmd):
    "Convenience function for unremapped normal commands."
    return vim.command("normal! {}".format(cmd))


@contextmanager
def preserve_cursor():
    """
    Restore current cursor position after leaving context.
    """
    pos = vim.current.window.cursor

    yield

    # restore cursor position
    vim.current.window.cursor = pos
