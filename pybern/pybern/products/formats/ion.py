#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime


class BernIon:

    def __init__(self, filename):
        self.filename = filename
        if not self.check_format():
            msg = '[ERROR] Failed to find/validate ION file: {:}'.format(
                self.filename)
            raise RuntimeError(msg)

    def check_format(self):
        try:
            with open(self.filename, 'r') as f:
                line = f.readline()
                self.header = line.strip()
                self.created_at = datetime.datetime.strptime(
                    ' '.join(line.split()[-2:]),
                    '%d-%b-%y %H:%M')  ## e.g. 01-JAN-21 07:31
                line = f.readline()
                assert (line.lstrip().startswith('-'))
                line = f.readline()
                assert (line.lstrip().startswith('MODEL NUMBER / STATION NAME'))
                line = f.readline()
                assert (line.lstrip().startswith(
                    'MODEL TYPE (1=LOCAL,2=GLOBAL,3=STATION)'))
                return True
        except:
            return False

    def get_epochs(self):
        epochs = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                if line.lstrip().startswith('FROM EPOCH'):
                    _str = 'FROM EPOCH / REFERENCE EPOCH (Y,M,D,H,M,S)'
                    assert (line.lstrip()[0:len(_str)] == _str)
                    epochs.append(
                        datetime.datetime.strptime(
                            line.split(':')[1].strip(), '%Y %m %d %H %M %S'))
        return epochs

    def time_span(self):
        epochs = self.get_epochs()
        return epochs[0], epochs[-1]
