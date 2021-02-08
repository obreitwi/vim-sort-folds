#!/usr/bin/env python3
# encoding: utf-8

import functools as ft
import vim
from contextlib import contextmanager


def cursor_preserving(func):
    """
    Decorator for functions so that cursor position is preserved.
    """
    @ft.wraps(func)
    def wrapped(*args, **kwargs):
        with preserve_cursor():
            return func(*args, **kwargs)

    return wrapped


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
