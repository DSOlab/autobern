#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import re
import sys
import os

##
##  KeyFiles are normal ascii files holding variable name and value pairs, e.g.
##  VAR_NAME = VAR_VALUE  or
##  VAR_NAME = "VAR_VALUE"
##  Any line starting with '#' will be omited and considered a comment line.
##  VAR_NAME can include any of the characters: a-z, A-Z, 0-9, or '_'
##  VAR_VALUE can include pretty much any character.
##

def expand_env_vars(line):
    for s in re.finditer(r'\$\{[a-zA-Z0-9_]+\}', line):
        evar = re.match('^\$\{([a-zA-Z0-9_]+)\}', s.group()).group(1)
        line = line.replace(s.group(), os.getenv(evar, evar))
    return line

def parse_key_file(fn, parse_error_is_fatal=False, expand_envvars=True):
    result = {}
    lnrgx = re.compile(
        '^\s*(?P<var_name>\w+)\s*=\s*"?(?P<var_value>[ a-zA-Z0-9!@#;\$%\^\&\.,\/*\)\(+=._-]+)"?\s*$'
    )
    with open(fn, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'):
                if expand_envvars:
                    ## find any substring of type ${VAR} and expand it
                    line = expand_env_vars(line)
                
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
                
                ## catch lines of type 'ATX2PCV = '
                elif re.match(r"^\s*(?P<var_name>\w+)\s*=\s*$", line.strip()):
                    m = re.match(r"^\s*(?P<var_name>\w+)\s*=\s*$", line.strip())
                    result[m.group('var_name')] = None
                    m = None
                
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
        will try to find the value var1 in the they file. If the key is found,
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

def extract_rename_key_values(key_file, renamedct, **kwargs):
    """
    Parse a key file (aka a file with lines of type: 'VAR_X = foobar') and
    extract values of given keys. If a key is not found, then it's value is
    supposed to be the one passed in. This version will also rename the keys 
    in the returned dictionary according to the renamedct dictionary.

    Example:
        key_file = '/foo/bar/keys'
        renamedct = {'var1': 'VAR1', 'var2': 'foo2'}
        kwargs = {'var1': None, 'var2': 2, 'var3': 1, 'var4': None}
        contents of key_file:
            var1 = some value
            var2 = 222
            var3 = 1
            var5 = foobar
        Returns the dictionary:
            {'var4': None, 'VAR1': 'some value', 'foo2': '222', 'var3': '1'}

    key_file: The input key file filename
    **kwargs: A list of arguments of type: 'var1=devault_value'; the function
        will try to find the value var1 in the they file. If the key is found,
        then its value (as recorded in the key file) is returned. If the key is
        not found, its default value (aka the one specified at function input)
        is returned.
    returns: A dictionary holding all keys in kwargs but renamed according to 
        the renamedct dictionary; the vaues of the keys are the values recorded 
        in the key file if the corresponding keys exist, else the value 
        specified at input

    Note that if a key is found in the key file, its value is always returned
    as a string.
    """
    keys_dict = parse_key_file(key_file)
    return_dict = {}
    for key in kwargs:
        new_key = key if key not in renamedct else renamedct[key]
        return_dict[new_key] = keys_dict[key] if key in keys_dict else kwargs[key]
    return return_dict
