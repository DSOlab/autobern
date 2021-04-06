#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
import pybern.products.bernparsers.bernpcf as bpcf

if len(sys.argv) != 2:
    print('[ERROR] Need to provide a .PCF file')
    sys.exit(1)


pcf = bpcf.PcfFile(sys.argv[1])
pcf.set_variable('V_GNSSAR', 'CHANGED', None)
pcf.set_variable('V_FOO', 'FOOVAR', 'Just for parsing tests')
pcf.set_variable('V_RESULT', 'BAR', None)
pcf.dump()
