#!/usr/bin/env python3
# encoding: utf-8

"""
Some convenience key functions to set 'sort_folds_key_function' to.
"""


_registered_functions = {}


def get(name):
    """
    Get the key function with the supplied name.

    :param name: Name of the key function to return.
    :return: Key function with name `name` that was previously registered.
    """
    return _registered_functions.get(name, None)


def register(function):
    """
    Register the given function as key function to be used for fold sorting.

    :param function: Function to register as key function.
    :return: Same function so that `register` can be used as decorator.
    """
    global _registered_functions
    _registered_functions[function.__name__] = function
    return function


@register
def get_citekey(fold):
    # very crude extraction without regexes
    return fold[0].split("{")[1].split(",")[0]
