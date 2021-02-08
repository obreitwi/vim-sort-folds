#!/usr/bin/env python3
# encoding: utf-8

import vim
from contextlib import contextmanager

@contextmanager
def preserve_cursor():
    """
    Restore current cursor position after leaving context.
    """
    pos = vim.current.window.cursor

    yield

    # restore cursor position
    vim.current.window.cursor = pos
