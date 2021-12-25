#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
from pybern.products.euref.utils import get_m3g_log
import pybern.products.formats.igs_log_file as ilf

## download m3g log file for STEF
#status, target, saveas = get_m3g_log('STEF00GRC')
#print('Downloaded log file to {:}'.format(saveas))

log = ilf.IgsLogFile('gop.log')

## parse blocks (just for testing)
#for blc in range(14):
#  blines = log.parse_block2line_list('{}'.format(blc))

#b4_lines = log.parse_block2line_list(4)
#print(b4_lines)
#
b4_dict = log.parse_block(0)
print(b4_dict)
##
b4_dict = log.parse_block(2)
print(b4_dict)
##
b4_dict = log.parse_block(3)
print(b4_dict)
##
b4_dict = log.parse_block(4)
print(b4_dict)
##
b4_dict = log.parse_block(8)
print(b4_dict)
