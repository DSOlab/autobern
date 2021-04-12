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
## change a variable that exists
pcf.set_variable('V_GNSSAR', 'CHANGED', None)
## set a variable that does not exist
pcf.set_variable('V_FOO', 'FOOVAR', 'Just for parsing tests')
## if we set the same variable twice, then the last assignment holds
pcf.set_variable('V_RESULT', 'BAR', None)
pcf.set_variable('V_RESULT', 'BAR1', None)
pcf.dump('dumped.pfc')

pcf = bpcf.PcfFile('dumped.pfc')
## assert that we have done the right changes
pcf.assert_variables(['V_GNSSAR', 'V_FOO', 'V_RESULT'], ['CHANGED', 'FOOVAR', 'BAR1'])
## assert some varibale that does not exist; this should throw
try:
    pcf.assert_variables(['V_GNSSAR1'],['FOO'])
    print('[ERROR] Should have thrown!')
except Exception as e:
    print('Exception excepted and thrown; error is:')
    print(e)

os.remove('dumped.pfc')
