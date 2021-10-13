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

def extract_key_values(key_file, **kwargs):
    """
    Parse a key file (aka a file with lines of type: 'VAR_X = foobar') and
    extract values of given keys. If a key is not found, then it's value is
    supposed to be the one passed in.

    key_file: The input key file filename
    **kwargs: A list of arguments of type: 'var1=devault_value'; the function
        wiil try to find the value var1 in the they file. If the key is found,
        then its value (as recorded in the key file) is returned. If the key is
        not found, its default value (aka the one specified at function input)
        is returned.
    returns: A dictionary holding all keys in kwargs; the vaues of the keys are
        the values recorded in the key file if the corresponding keys exist, 
        else the value specified at input

    Note that if a key is found in the key file, its value is always returned
    as a string.
    """
    keys_dict = parse_key_file(key_file)
    return_dict = {}
    for key in kwargs:
        return_dict[key] = keys_dict[key] if key in keys_dict else kwargs[key]
    return return_dict
