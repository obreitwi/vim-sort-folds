#!/usr/bin/env python3
# encoding: utf-8

"""
Some convenience key functions to set 'sort_folds_key_function' to.
"""

def get_citekey(fold):
    # very crude extraction without regexes
    return fold[0].split("{")[1].split(",")[0]
