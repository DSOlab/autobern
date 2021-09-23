#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import pybern.products.bernparsers.bloadvar as blvar


if len(sys.argv) != 2:
    print('[ERROR] Need to provide a LOADVAR file')
    sys.exit(1)

dvars = blvar.parse_loadvar(sys.argv[1])
for key in dvars:
    print('\t{:20s}:{:30s}'.format(key, dvars[key]))
