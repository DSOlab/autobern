#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import os, sys
from pybern.products.errors.errors import FileFormatError, ArgumentError

utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/utils/')
sys.path.append(utils_dir)
from dateutils import date_ranges_overlap

MIN_STA_DATE = datetime.datetime.min
MAX_STA_DATE = datetime.datetime.max
FILE_FORMAT = '.STA (Bernese v5.2)'


class Type001Record:
    ''' A class to hold type 001 station information records for a single station.
  '''

    def __init__(self, line=None, **kwargs):
        ''' First resolve and assign any values from kwargs; then, if line is not 
      None, resolve line
    '''
        if kwargs:
            self.init_from_args(**kwargs)
        if line is not None:
            self.init_from_line(line)

    def merge(self, other_rec):
        """ merge only if:
        * sta_name is the same,
        * flag is the same
        * old_name is the same
        * dates do not overlap and are continuous
        remarks are concatenated
        if self.sta_name == other_rec.sta_name and self.flag == other_rec.flag and self.old_name == other_rec.old_name:
            first, last = (
                self,
                other_rec) if self.start_date < other_rec.start_date else (
                    other_rec, self)
            if not date_ranges_overlap(self.start_date, self.stop_date,
                                       other_rec.start_date,
                                       other_rec.stop_date):
                if (first.stop_date - last.start_date).days < 2:
                    return Type001Record(station=self.sta_name,
                                         flag=self.flag,
                                         old_name=self.old_name,
                                         start=first.start_date,
                                         end=last.stop_date,
                                         remark='{:} {:}'.format(
                                             self.remark, other_rec.remark))
        return None
        """

    def init_from_args(self, **kwargs):
        self.sta_name = kwargs['station'] if 'station' in kwargs else (' ' * 4)
        self.flag = kwargs['flag'] if 'flag' in kwargs else '1'
        self.old_name = kwargs['old_name'] if 'old_name' in kwargs else (' ' *
                                                                         4)
        self.start_date = kwargs['start'] if 'start' in kwargs else MIN_STA_DATE
        self.stop_date = kwargs['end'] if 'end' in kwargs else MAX_STA_DATE
        self.remark = kwargs['remark'] if 'remark' in kwargs else ''
        if len(self.sta_name) < 4:
            raise ArgumentError(
                '[ERROR] Type001Record::init_from_args Failed to parse station name',
                'station')
        if len(self.old_name) < 4:
            raise ArgumenttError(
                '[ERROR] Type001Record::init_from_args Failed to parse station old name',
                'old_name')
        try:
            self.flag = int(self.flag)
        except:
            raise ArgumentError(
                '[ERROR] Type001Record::init_from_args Failed to parse flag',
                'flag')

    def init_from_line(self, line):
        ''' Initialize an instance using a type 001 information line. This will 
      set the start and stop date and the station name.

      An example of a .STA file type 001 info line follows::

      STATION NAME          FLG          FROM                   TO         OLD STATION NAME      REMARK
      ****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ************************
      AIRA 21742S001        001  1980 01 06 00 00 00  2099 12 31 00 00 00  AIRA*                 MGEX,aira_20120821.log
      ISBA 20308M001        003                                            ISBA                  EXTRA RENAMING
    '''
        self.sta_name = line[0:16].rstrip()
        if len(self.sta_name) < 4:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type001Record::init_from_line Failed to parse station name'
            )
        self.flag = line[22:25].rstrip()
        try:
            self.flag = int(self.flag.lstrip('0'))
        except:
            raise ArgumenttError(
                FILE_FORMAT, line,
                '[ERROR] Type001Record::init_from_line Failed to parse station flag'
            )
        self.old_name = line[69:89].rstrip()
        if len(self.old_name) < 4:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type001Record::init_from_line Failed to parse station old name'
            )
        self.remark = line[91:].rstrip()
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
                    '[ERROR] Type001Record::init_from_line Failed to parse start date'
                )
        ## resolve stop date (or set to now)
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
                    '[ERROR] Type001Record::init_from_line Failed to parse stop date'
                )

    def __str_format__(self):
        ''' Format the instance as a valid Type 001 record
    '''
        t_start = ' ' * 19
        t_stop = ' ' * 19
        if self.start_date != MIN_STA_DATE:
            t_start = self.start_date.strftime('%Y %m %d %H %M %S')
        if self.stop_date != MAX_STA_DATE:
            t_stop = self.stop_date.strftime('%Y %m %d %H %M %S')
        return '{:<16s}      {:03d}  {:}  {:}  {:<20s}  {:}'.format(
            self.sta_name, self.flag, t_start, t_stop, self.old_name,
            self.remark)

    def __repr__(self):
        return self.__str_format__()

    def __str__(self):
        return self.__str_format__()
