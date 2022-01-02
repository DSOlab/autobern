#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import re
import argparse
import datetime
import pybern.products.bernbpe as bpe

print(bpe.check_bpe_status('/home/bpe/data/GPSDATA/CAMPAIGN52/GREECE/BPE/GRE_.RUN'))
bpe.compile_error_report('/home/bpe/data/GPSDATA/CAMPAIGN52/GREECE/BPE/GRE_.RUN', '/home/bpe/data/GPSDATA/CAMPAIGN52/GREECE/')
