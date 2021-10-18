#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
from pybern.products.fileutils.keyholders import parse_key_file, extract_key_values, extract_rename_key_values

var_dct = parse_key_file('/home/bpe/applications/autobern/data/example_key_file')
print(var_dct)

# try to find given keys:
d = extract_key_values('/home/bpe/applications/autobern/data/example_key_file', VAR1=None, VAR_1=2, VAR_3="var3", VAR6=True, VAR99="var99")
print(d)

# try to find and rename given keys:
renamedct = {'var1': 'VAR1', 'var2': 'foo2'}
kargsdct = {'var1': None, 'var2': 2, 'var3': 1, 'var4': None}
d = extract_rename_key_values('/home/bpe/applications/autobern/data/example_key_file2', renamedct, **kargsdct)
print(d)
