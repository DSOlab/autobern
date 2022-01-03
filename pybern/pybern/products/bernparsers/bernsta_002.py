#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import sys
from pybern.products.errors.errors import FileFormatError, ArgumentError

MIN_STA_DATE = datetime.datetime.min
MAX_STA_DATE = datetime.datetime.max
FILE_FORMAT = '.STA (Bernese v5.2)'


class Type002Record:
    ''' A class to hold type 002 station information records for a single station.
  '''

    @staticmethod
    def dump_header(ofile=sys.stdout):
        header_str = """TYPE 002: STATION INFORMATION
-----------------------------

STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK
****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************"""
        print(header_str, file=ofile)

    def __init__(self, line=None, **kwargs):
        ''' First resolve and assign any values from kwargs; then, if line is not 
      None, resolve line
    '''
        if kwargs:
            self.init_from_args(**kwargs)
        if line is not None:
            self.init_from_line(line)
    
    def init_from_args(self, **kwargs):
        self.sta_name = kwargs['station'] if 'station' in kwargs else (' ' * 4)
        self.flag = kwargs['flag'] if 'flag' in kwargs else 1
        self.start_date = kwargs['start'] if 'start' in kwargs else MIN_STA_DATE
        self.stop_date = kwargs['end'] if 'end' in kwargs else MAX_STA_DATE
        self.receiver_t = kwargs['receiver_type'] if 'receiver_type' in kwargs else ''
        self.receiver_sn = kwargs['receiver_serial'] if 'receiver_serial' in kwargs else ''
        self.receiver_nr = kwargs['receiver_number'] if 'receiver_number' in kwargs else '999999'
        self.antenna_t = kwargs['antenna_type'] if 'antenna_type' in kwargs else ''
        self.antenna_sn = kwargs['antenna_serial'] if 'antenna_serial' in kwargs else ''
        self.antenna_nr = kwargs['antenna_number'] if 'antenna_number' in kwargs else '999999'
        self.north = kwargs['delta_north'] if 'delta_north' in kwargs else 0e0
        self.east = kwargs['delta_east'] if 'delta_east' in kwargs else 0e0
        self.up = kwargs['delta_up'] if 'delta_up' in kwargs else 0e0
        self.remark = kwargs['remark'] if 'remark' in kwargs else ''
        self.description = kwargs['description'] if 'description' in kwargs else ''

    def init_from_line(self, line):
        ''' Initialize a Type002Record  instance using a type 002 information line. 
       This will set the start and stop date and the station name.

      An example of a .STA file type 002 info line follows::

        STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK
        ****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************
        AFKB                  001                                            LEICA GRX1200GGPRO                          999999  LEIAT504GG      LEIS                        999999    0.0000    0.0000    0.0000  Kabul, AF               NEW
        AZGB 49541S001        001                       2004 07 20 23 59 59  TRIMBLE 4000SSE                             999999  TRM22020.00+GP  NONE                        999999    0.0000    0.0000    0.0000  Globe, US               NEW
        AZGB 49541S001        001  2004 07 21 00 00 00  2004 08 26 23 59 59  TRIMBLE 4700                                999999  TRM33429.00+GP  NONE                        999999    0.0000    0.0000    0.0000  Globe, US               NEW

    '''
        self.sta_name = line[0:16].rstrip()
        self.flag = line[22:25].rstrip()
        self.receiver_t = line[69:89].rstrip()
        self.receiver_sn = line[91:111].rstrip()
        self.receiver_nr = line[113:119].rstrip()
        self.antenna_t = line[121:141].rstrip()
        self.antenna_sn = line[143:163].rstrip()
        self.antenna_nr = line[165:171].rstrip()
        self.north = line[173:181].rstrip()
        self.east = line[183:191].rstrip()
        self.up = line[193:201].rstrip()
        self.description = line[203:225].rstrip()
        self.remark = line[227:].rstrip()
        if len(self.sta_name) < 4:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type002Record::init_from_line Failed to parse station name'
            )
        try:
            self.flag = int(self.flag)
        except:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] Type002Record::init_from_line Failed to parse station flag'
            )
        ## eccentricities to float values
        for k in [self.north, self.east, self.up]:
            try:
                float(k)
            except:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] Type002Record::init_from_line Failed to parse {:}'.
                    format(' '.join([self.north, self.east, self.up])))
        self.north, self.east, self.up = [
            float(x) for x in [self.north, self.east, self.up]
        ]
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
                    '[ERROR] Type002Record::init_from_line Failed to parse start date'
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
                    '[ERROR] Type002Record::init_from_line Failed to parse stop date'
                )
    
    def equal_except_dates(self, type002_instance):
        d1 = vars(self)
        d2 = vars(type002_instance)
        for key in d1:
            if key != 'start_date' and key != 'stop_date':
                if d1[key] != d2[key]: return False
        return True
    
    def equal_except(self, type002_instance, except_list):
        d1 = vars(self)
        d2 = vars(type002_instance)
        for key in d1:
            if key not in except_list:
                if d1[key] != d2[key]: return False
        return True

    def __str_format__(self):
        ''' Format the instance as a valid Type 002 record
    '''
        t_start = ' ' * 19
        t_stop = ' ' * 19
        if self.start_date != MIN_STA_DATE:
            t_start = self.start_date.strftime('%Y %m %d %H %M %S')
        if self.stop_date != MAX_STA_DATE:
            t_stop = self.stop_date.strftime('%Y %m %d %H %M %S')
        return '{:<16s}      {:03d}  {:}  {:}  {:<20s}  {:>20s}  {:>6s}  {:<20s}  {:>20s}  {:>6s}  {:8.4f}  {:8.4f}  {:8.4f}  {:22s} {:}'.format(
            self.sta_name, self.flag, t_start, t_stop, self.receiver_t,
            self.receiver_sn, self.receiver_nr, self.antenna_t, self.antenna_sn,
            self.antenna_nr, self.north, self.east, self.up, self.description,
            self.remark)

    def __repr__(self):
        return self.__str_format__()

    def __str__(self):
        return self.__str_format__()

def merge_t2_intervals(t2_list):
    """ Merge a list of Type002 instances.
        This function is mainly used in the following case: suppose we have a
        list of Type002 records, e.g. as extracted from a log file. It might 
        be the case that two consecutive records have all elements equal (e.g. 
        the may only differ in the cut-off angle which is not recorded in the 
        Type002 records but is recorded in the log files) but are marked as 
        speperate intervals in the log file and in the input list.
        This function will join two such intervals if they are consecutive and
        the end/start datetime of the two intervals are less than 12 hours
        aprart.
    """

    def merget2(t2_list):
        for idx, val in enumerate(t2_list[0:-1]):
            t20 = val
            t21 = t2_list[idx+1]
            if t20.equal_except_dates(t21):
                if t20.stop_date - t21.start_date < datetime.timedelta(hours=12):
                    return idx
        return None
    
    idx = merget2(t2_list)
    while idx is not None:
        t2_list[idx+1].start_date = t2_list[idx].start_date
        t2_list = t2_list[0:idx] + t2_list[idx+1:]
        idx = merget2(t2_list)
    
    return t2_list
