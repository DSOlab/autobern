#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime


class Sp3:

    def __init__(self, filename):
        self.filename = filename
        if not self.check_format():
            msg = '[ERROR] Failed to find/validate SP3 file: {:}'.format(
                self.filename)
            raise RuntimeError(msg)

    def check_format(self):
        try:
            with open(self.filename, 'r') as f:
                ## First line
                line = f.readline()
                if line[0:2] == "#c":
                    version_c = 'c'
                elif line[0:2] == "#d":
                    version_c = 'd'
                else:
                    return False
                self.version = version_c
                return True
        except:
            return False

    def read_header(self):
        with open(self.filename, 'r') as f:
            ## First line
            line = f.readline()
            start_date = datetime.datetime.strptime(line[3:29],
                                                    '%Y %m %d %H %M %S.%f')
            num_epochs = int(line[32:39])
            crd_sys = line[46:51]
            ## Second line
            line = f.readline()
            interval = float(line[24:38])
            ## Third line
            line = f.readline()
            num_sats = int(line[4:6])
            ## Read-in satellites
            svs = []
            while line[0:2] == '+ ' and len(svs) < num_sats:
                for i in range(9, len(line.strip()), 3):
                    if line[i] in ['G', 'R', 'E', 'C', 'S'
                                  ] and int(line[i + 1:i + 3]) > 0:
                        svs.append(line[i:i + 3])
                line = f.readline()
            if len(svs) != num_sats:
                msg = '[ERROR] sp3::read_header Failed to read SVs'
                raise RuntimeError(msg)
            ## Get the time system
            while line and line[0:2] != "%c":
                line = f.readline()
            if line[0:2] != "%c":
                msg = '[ERROR] sp3::read_header Excpected \'%c\' at the start of line!'
                raise RuntimeError(msg)
            else:
                time_sys = line[9:12]
        self.start_date = start_date
        self.num_epochs = num_epochs
        self.crd_sys = crd_sys
        self.interval = interval
        self.num_sats = num_sats
        self.time_sys = time_sys
        self.svs = svs

    def time_span(self):
        try:
            a = self.start_date
        except:
            a = None
        if a is None:
            self.read_header()
        start = self.start_date
        stop = self.start_date + datetime.timedelta(seconds=self.num_epochs *
                                                    self.interval)
        return start, stop
