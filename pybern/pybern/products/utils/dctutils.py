#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys


def merge_dicts_impl(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def merge_dicts(dicta, dictb):
    ## see https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-taking-union-of-dictiona
    #if sys.version_info[0] >= 3:
    #    if sys.version_info[1] >= 9:
    #        return dicta | dictb
    #    elif sys.version_info[1] >= 5:
    #        return {**dicta, **dictb}
    #    else:
    #        return merge_dicts_impl(dicta, dictb)
    #else:
    #    return merge_dicts_impl(dicta, dictb)
    ## Just make it work for Python 2.7 !!
    return merge_dicts_impl(dicta, dictb)
