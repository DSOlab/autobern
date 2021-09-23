#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import re

def expand_dictionary_vals(dct):
    """ Example:
        for any key/value pair where the value includes a string of type:
        ${VAR}
        try to expand this (substring) based on keys already in the dictionary
        e.g.
        dct = { ...
         'C': '/home/bpe/bern52/BERN52'
         'X': '${C}/GPS'
         ...}
         will become:
        dct = { ...
         'C': '/home/bpe/bern52/BERN52'
         'X': '/home/bpe/bern52/BERN52/GPS'
         ...}
    """
    for key in dct:
        while True:
            ##  there are variables which contain more than one expandable
            ##+ values, i.e. XG="${C}/PGM/EXE_${F_VERS}". Resolve them one at 
            ##+ a time
            g = re.match(r'.*(\$\{.*\}).*', dct[key])
            if g:
                for sexp in g.groups():
                    var_name = re.match(r'\$\{(.*)\}', sexp).group(1)
                    ##  Note! could be an enviromental variable OR a variable set
                    ##+ by BERN52
                    if os.getenv(var_name):
                        dct[key] = dct[key].replace(sexp, os.getenv(var_name))
                    else:
                        dct[key] = dct[key].replace(sexp, dct[var_name])
            if not re.match(r'.*(\$\{.*\}).*', dct[key]):
                break
    return dct

def parse_loadvar(filenm, expand_variables=True):
    """ Example lines:
        export P="${HOME}/data/GPSDATA/CAMPAIGN52"
        export CGROUP="USERS"
        export VERSION="52"

        the following line though, should be ignored:
        export PATH="${PATH}:$1"
    """
    if not os.path.isfile(filenm):
        print('[ERROR] File not found: {:}'.format(filenm), file=sys.stderr)
        raise RuntimeError('File does not exist')

    var_dct = {}

    with open(filenm, 'r') as fvar:
        for line in fvar.readlines():
            if len(line) > 5 and not line.startswith('#'):
                if line.lstrip().startswith('export'):
                    l = line.split()
                    if not l[1].startswith('PATH='):
                        if len(l) != 2 or l[1].find('=')<0:
                            print('[ERROR] Failed to parse LOADVAR line {:}'.format(line.strip()), file=sys.stderr)
                            raise RuntimeError('Failed to parse LOADVAR line')
                        varc = l[1].split('=')
                        var_name = varc[0].strip()
                        var_val = varc[1].strip()
                        if var_val[0] == '\"' or var_val[0] == '\'':
                            assert(var_val[-1] == '\"' or var_val[-1] == '\'')
                            var_val = var_val[1:len(var_val)-1]
                        var_dct[var_name] = var_val
    return var_dct if expand_variables == False else expand_dictionary_vals(var_dct)
