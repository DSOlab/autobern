#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from pybern.products.gnssdates.gnssdates import mjd2pydt


class Erp:

    def __init__(self, filename):
        self.filename = filename
        self.date, self.nutation_model, self.subdaily_pole_model = [None] * 3
        if not self.check_format():
            msg = '[ERROR] Failed to find/validate ERP file: {:}'.format(
                self.filename)
            raise RuntimeError(msg)

    def check_format(self):
        try:
            with open(self.filename, 'r') as f:
                line = f.readline()
                assert (line.strip() == 'VERSION 2')
                max_lines = 100
                line_nr = 0
                while not line.lstrip().startswith('MJD'):
                    line = f.readline()
                    l = line.split()
                    # 'NUTATION MODEL       : IAU2000R06               SUBDAILY POLE MODEL: IERS2010'
                    if len(l) >= 7:
                        if line.lstrip().startswith('NUTATION MODEL'):
                            self.nutation_model = l[3]
                        if ' '.join(l[4:7]) == 'SUBDAILY POLE MODEL:':
                            self.subdaily_pole_model = l[7]
                    # ODE ULTRA-RAPID SOLUTION, VERSION 30, DAY 361, YEAR 2020        27-DEC-20 08:0
                    if len(l) > 3:
                        try:
                            self.comment = ' '.join(l[0:-2])
                            self.date = datetime.datetime.strptime(
                                ' '.join(l[-2:]), '%d-%b-%y %H:%M')
                        except:
                            pass
                    line_nr += 1
                    if line_nr >= max_lines:
                        msg = '[ERROR] Failed to parse ERP file {:} (#1)'.format(
                            filename)
                        raise RuntimeError(msg)
                return True
        except:
            return False

    def read_epochs(self):
        epochs = []
        try:
            with open(self.filename, 'r') as f:
                line = f.readline()
                while not line.lstrip().startswith('MJD'):
                    line = f.readline()
                line = f.readline()
                line = f.readline()
                while line:
                    l = line.split()
                    #print('mjd={:}'.format(l[0]))
                    epochs.append(mjd2pydt(float(l[0])))
                    #print('epoch appended')
                    line = f.readline()
            return epochs
        except:
            msg = '[ERROR] Failed to parse ERP file dates {:}'.format(
                self.filename)
            raise RuntimeError(msg)

    def time_span(self):
        epochs = self.read_epochs()
        return epochs[0], epochs[-1]
