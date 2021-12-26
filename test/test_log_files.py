#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
import pybern.products.bernparsers.bernsta as bsta
import pybern.products.formats.igs_log_file as ilog

if len(sys.argv) != 2:
    print('[ERROR] Need to provide a an IGS_LOG_FILE file')
    sys.exit(1)

log = ilog.IgsLogFile(sys.argv[1])
#print(log.parse_block(9))
#print(log.parse_block(6))

t1 = log.to_001type()
print('{}'.format(t1))
#
log.to_002type()
