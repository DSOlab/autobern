#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime


class Ionex:

    def __init__(self, filename):
        self.filename = filename
        if not self.check_format():
            msg = '[ERROR] Failed to find/validate IONEX file: {:}'.format(
                self.filename)
            raise RuntimeError(msg)
        self.read_header()

    def check_format(self):
        try:
            with open(self.filename, 'r') as f:
                l = f.readline().split()
                assert (' '.join(l[-4:]) == 'IONEX VERSION / TYPE')
                self.version = float(l[0])
                self.type = l[1]
                self.sys = l[2]
                return True
        except:
            return False

    def read_header(self):
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                if line[60:].strip() == 'END OF HEADER':
                    break
                if line[60:].strip() == 'PGM / RUN BY / DATE':
                    self.pgm = line[0:20].strip()
                    self.run_by = line[20:40].strip()
                    self.date = line[40:60].strip()
                elif line[60:].strip() == 'EPOCH OF FIRST MAP':
                    self.epoch_of_first_map = datetime.datetime.strptime(
                        line[0:37].strip(), '%Y %m %d %H %M %S')
                elif line[60:].strip() == 'EPOCH OF LAST MAP':
                    self.epoch_of_last_map = datetime.datetime.strptime(
                        line[0:37].strip(), '%Y %m %d %H %M %S')
                elif line[60:].strip() == 'INTERVAL':
                    self.interval = int(line[0:6].strip())
        return

    def time_span(self):
        return self.epoch_of_first_map, self.epoch_of_last_map
