#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from pybern.products.errors.errors import FileFormatError, ArgumentError

MIN_STA_DATE = datetime.datetime.min
MAX_STA_DATE = datetime.datetime.max
FILE_FORMAT = '.STA (Bernese v5.2)'


class Type002Record:
    ''' A class to hold type 002 station information records for a single station.
  '''

    @staticmethod
    def dump_header():
        header_str = """
TYPE 002: STATION INFORMATION
-----------------------------

STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK
****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************
                     """
        print(header_str)

    def __init__(self, line):
        self.init_from_line(line)

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

    def __str_format__(self):
        ''' Format the instance as a valid Type 002 record
    '''
        t_start = ' ' * 19
        t_stop = ' ' * 19
        if self.start_date != MIN_STA_DATE:
            t_start = self.start_date.strftime('%Y %m %d %H %M %S')
        if self.stop_date != MAX_STA_DATE:
            t_stop = self.stop_date.strftime('%Y %m %d %H %M %S')
        return '{:<16s}      {:03d}  {:}  {:}  {:<20s}  {:<20s}  {:<6s}  {:<20s}  {:<20s}  {:<6s}  {:8.4f}  {:8.4f}  {:8.4f}  {:22s} {:}'.format(
            self.sta_name, self.flag, t_start, t_stop, self.receiver_t,
            self.receiver_sn, self.receiver_nr, self.antenna_t, self.antenna_sn,
            self.antenna_nr, self.north, self.east, self.up, self.description,
            self.remark)

    def __repr__(self):
        return self.__str_format__()

    def __str__(self):
        return self.__str_format__()
