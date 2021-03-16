#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import re
import sys

##
##  KeyFiles are normal ascii files holding variable name and value pairs, e.g.
##  VAR_NAME = VAR_VALUE  or
##  VAR_NAME = "VAR_VALUE"
##  Any line starting with '#' will be omited and considered a comment line.
##  VAR_NAME can include any of the characters: a-z, A-Z, 0-9, or '_'
##  VAR_VALUE can include pretty much any character.
##


def parse_key_file(fn, parse_error_is_fatal=False):
    result = {}
    lnrgx = re.compile(
        '^\s*(?P<var_name>\w+)\s*=\s*"?(?P<var_value>[ a-zA-Z0-9!@#\$%\^\&*\)\(+=._-]+)"?\s*$'
    )
    with open(fn, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                m = re.match(lnrgx, line.strip())
                if not m and len(line.strip()) > 0:
                    print(
                        '[WRNNG] Line is not a comment but could not be resolved: \'{:}\''
                        .format(line.strip()),
                        file=sys.stderr)
                    if parse_error_is_fatal:
                        msg = '[ERROR] keyholders::parse_key_file unable to parse line: \'{:}\''.format(
                            line.strip())
                        raise RuntimeError(msg)
                if m is not None:
                    result[m.group('var_name')] = m.group('var_value')
    return result
