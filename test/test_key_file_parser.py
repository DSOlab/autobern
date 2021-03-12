#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
from shutil import copyfileobj
from pybern.products.fileutils.keyholders import parse_key_file

var_dct = parse_key_file('/home/xanthos/Builds/autobern/data/example_key_file')
print(var_dct)
