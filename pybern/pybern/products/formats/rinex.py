#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import os
import re
import sys

class Rinex:
    def __init__(self, filename):
        self.filename = filename

    def updateMarkerName(self, marker_name):
        field_replaced = False
        temp_file = self.filename + '.scractch-file'
        with open(self.filename, 'r') as fin:
            with open(temp_file, 'w') as fout:
                for line in fin.readlines():
                    if line.rstrip().endswith('MARKER NAME'):
                    # if re.match(r"MARKER NAME *$", line.rstrip()):
                        print('{:60s}{:}'.format(marker_name, 'MARKER NAME'), file=fout)
                        field_replaced = True
                    else:
                        print(line.rstrip(), file=fout)
        if field_replaced:
            os.rename(temp_file, self.filename)
            return True
        else:
            os.remove(temp_file)
            return False
