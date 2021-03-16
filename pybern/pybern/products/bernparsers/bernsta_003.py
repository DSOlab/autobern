#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from pybern.products.errors.errors import FileFormatError, ArgumentError

MIN_STA_DATE = datetime.datetime.min
MAX_STA_DATE = datetime.datetime.max
FILE_FORMAT = '.STA (Bernese v5.2)'


class Type003Record:
    ''' A class to hold type 003 station information records for a single station.
    '''

    def __init__(self, line):
        self.init_from_line(line)

    def init_from_line(self, line):
        ''' Here is a type 003 line:
        ABMF 97103M001        003  2014 07 22 00 00 00  2014 07 25 23 59 59  %RNX_CRX: PPPFIN indicates serious data problems
      '''
        self.sta_name = line[0:16].rstrip()
        if len(self.sta_name) < 4:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type003Record::init_from_line Failed to parse station name'
            )
        try:
            self.flag = int(line[22:25].rstrip())
        except:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type003Record::init_from_line Failed to parse station flag'
            )
        ## resolve the start date (or set to min if empty)
        t_str = line[27:46].strip()
        if len(t_str) == 0:
            self.start_date = MIN_STA_DATE
        else:
            try:
                self.start_date = datetime.datetime.strptime(
                    t_str.strip(), '%Y %m %d %H %M %S')
            except:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] Type003Record::init_from_line Failed to parse start date'
                )
        ## resolve stop date (or set to nax)
        t_str = line[48:67].strip()
        if len(t_str) == 0:
            self.stop_date = MAX_STA_DATE
        else:
            try:
                self.stop_date = datetime.datetime.strptime(
                    t_str.strip(), '%Y %m %d %H %M %S')
            except:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] Type003Record::init_from_line Failed to parse stop date'
                )
        self.remark = line[68:].rstrip()

    def __str_format__(self):
        ''' Format the instance as a valid Type 003 record
      '''
        t_start = ' ' * 19
        t_stop = ' ' * 19
        if self.start_date != MIN_STA_DATE:
            t_start = self.start_date.strftime('%Y %m %d %H %M %S')
        if self.stop_date != MAX_STA_DATE:
            t_stop = self.stop_date.strftime('%Y %m %d %H %M %S')
        return '{:-16s}      {:03d}  {:}  {:} {:-20s}  {:-20s}  {:-s}'.format(
            self.sta_name, self.flag, t_start, t_stop, self.remark)

    def __repr__(self):
        return self.__str_format__()

    def __str__(self):
        return self.__str_format__()
