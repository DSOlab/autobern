#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import contextlib


""" use 'with open' statement regardless if filename is a file or sys.stdout/err
    see https://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely
    # writes to some_file
    with smart_open('some_file') as fh:
        print('some output', file=fh)

    # writes to stdout
    with smart_open() as fh:
        print('some output', file=fh)

    # writes to stdout
    with smart_open('-') as fh:
        print('some output', file=fh)
"""
@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()
