#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys


def merge_dicts_impl(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def merge_dicts(dicta, dictb,accept_none=False):
    ## see https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-taking-union-of-dictiona
    if not accept_none:
        return {**dicta, **dictb}
    
    else:
        if dicta is None and dictb is None:
            return None
        elif dicta is None and dictb is not None:
            return dictb
        elif dicta is not None and dictb is None:
            return dicta
        else:
            return {**dicta, **dictb}
