#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
from pybern.products.errors.errors import FileFormatError
from sys import version_info as version_info
if version_info.major == 2:
    from bernsta_001 import Type001Record
    from bernsta_002 import Type002Record
    from bernsta_003 import Type003Record
    from bernsta_station import StationRecord
else:
    from .bernsta_001 import Type001Record
    from .bernsta_002 import Type002Record
    from .bernsta_003 import Type003Record
    from .bernsta_station import StationRecord
'''
STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2           16-JAN-21 13:11
--------------------------------------------------------------------------------

FORMAT VERSION: 1.01
TECHNIQUE:      GNSS
'''
FILE_FORMAT = '.STA (Bernese v5.2)'


class BernSta:

    def __init__(self, filename):
        self.filename = filename
        self.stations = []
        self.dct = {}

    def __parse_block_001(self, stream):
        ''' Stream should be open and at any line before the line:
        TYPE 001: RENAMING OF STATIONS  
    '''
        line = stream.readline()
        ## read and parse Type001 block
        while not line.startswith('TYPE 001: RENAMING OF STATIONS'):
            line = stream.readline()
        if not line.startswith('TYPE 001: RENAMING OF STATIONS'):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_001 failed to find \'TYPE 001: RENAMING OF STATIONS\' block'
            )
        while not line.startswith(
                'STATION NAME          FLG          FROM                   TO         OLD STATION NAME      REMARK'
        ):
            line = stream.readline()
        if not line.startswith(
                'STATION NAME          FLG          FROM                   TO         OLD STATION NAME      REMARK'
        ):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_001 failed to find header block for Type 001 (#1)'
            )
        line = stream.readline()
        if line.strip(
        ) != '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ************************':
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_001 failed to find header block for Type 001 (#2)'
            )
        line = stream.readline()
        while line and len(line) > 20:
            new_rec = Type001Record(line)
            if int(new_rec.flag) != 1:
                print(
                    '[WRNNG] BernSta::__parse_block_001 Skipping record line with flag != 1',
                    file=sys.stderr)
                print('[WRNNG] line: \'{:}\''.format(line.strip()))
            else:
                if new_rec.sta_name in self.stations:
                    self.dct[new_rec.sta_name]['type001'].append(new_rec)
                else:
                    self.stations.append(new_rec.sta_name)
                    self.dct[new_rec.sta_name] = {'type001': [new_rec]}
                """
                if new_rec.sta_name in self.stations:
                    ## before rasing, there is a slight chance we have the following case:
                    ##GOL2 40405S031        001  1999 07 04 00 00 00  2000 07 07 23 59 59  GOL2*                 STN (RENAMING!)
                    ##GOL2 40405S031        001  2000 07 08 00 00 00                       GOL2*                 STN
                    __old_t001 = self.dct[new_rec.sta_name]['type001']
                    concat_rec = __old_t001.merge(new_rec)
                    if concat_rec is not None:
                        self.dct[new_rec.sta_name] = {'type001': concat_rec}
                        print(
                            '[WRNNG] Dual record found for station {:} Merging ....'
                            .format(new_rec.sta_name))
                        print(
                            '        {:} and \n        {:}\nto      {:}'.format(
                                __old_t001, new_rec, concat_rec))
                    else:
                        raise RuntimeError(
                            '[ERROR] BernSta::__parse_block_001 Station {:} already parsed! Possible double entry.'
                            .format(new_rec.sta_name))
                else:
                    self.stations.append(new_rec.sta_name)
                    self.dct[new_rec.sta_name] = {'type001': new_rec}
                """
            line = stream.readline()

    def __parse_block_002(self, stream, missing_is_error=False):
        ''' Stream should be open and at any line before the line:
        TYPE 002: STATION INFORMATION
    '''
        line = stream.readline()
        ## read and parse Type002 block
        while not line.startswith('TYPE 002: STATION INFORMATION'):
            line = stream.readline()
        if not line.startswith('TYPE 002: STATION INFORMATION'):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_002 failed to find \'TYPE 002: STATION INFORMATION\' block'
            )
        while not line.startswith(
                'STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'
        ):
            line = stream.readline()
        if not line.startswith(
                'STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'
        ):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#1)'
            )
        line = stream.readline()
        if line.strip(
        ) != '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************':
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#2)'
            )
        line = stream.readline()
        while line and len(line) > 20:
            new_rec = Type002Record(line)
            if new_rec.sta_name not in self.stations:
                if missing_is_error:
                    raise RuntimeError(
                        '[ERROR] BernSta::__parse_block_002 Station {:} has Type 002 record but not included in Type 001'
                        .format(new_rec.sta_name))
                else:
                    print(
                        '[WRNNG] BernSta::__parse_block_002 Station {:} has Type 002 record but not included in Type 001'
                        .format(new_rec.sta_name))
                    print('        Record will be skipped!')
            else:
                if 'type002' in self.dct[new_rec.sta_name]:
                    self.dct[new_rec.sta_name]['type002'].append(new_rec)
                else:
                    self.dct[new_rec.sta_name]['type002'] = [new_rec]
            line = stream.readline()

    def __parse_block_003(self, stream, missing_is_error=False):
        ''' Stream should be open and at any line before the line:
    '''
        line = stream.readline()
        ## read and parse Type003 block
        while not line.startswith('TYPE 003: HANDLING OF STATION PROBLEMS'):
            line = stream.readline()
        if not line.startswith('TYPE 003: HANDLING OF STATION PROBLEMS'):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_003 failed to find \'TYPE 003: HANDLING OF STATION PROBLEMS\' block'
            )
        while not line.startswith(
                'STATION NAME          FLG          FROM                   TO         REMARK'
        ):
            line = stream.readline()
        if not line.startswith(
                'STATION NAME          FLG          FROM                   TO         REMARK'
        ):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_003 failed to find header block for Type 003 (#1)'
            )
        line = stream.readline()
        if not line.startswith(
                '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ***********************************************************'
        ):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 003 (#2)'
            )
        line = stream.readline()
        while line and len(line) > 20:
            new_rec = Type003Record(line)
            if new_rec.sta_name not in self.stations:
                if missing_is_error:
                    raise RuntimeError(
                        '[ERROR] BernSta::__parse_block_003 Station {:} has Type 003 record but not included in Type 001'
                        .format(new_rec.sta_name))
                else:
                    print(
                        '[WRNNG] BernSta::__parse_block_003 Station {:} has Type 003 record but not included in Type 001'
                        .format(new_rec.sta_name))
                    print('        Record will be skipped!')
            else:
                if 'type003' in self.dct[new_rec.sta_name]:
                    self.dct[new_rec.sta_name]['type003'].append(new_rec)
                else:
                    self.dct[new_rec.sta_name]['type003'] = [new_rec]
            line = stream.readline()

    def parse(self):
        if not os.path.isfile(self.filename):
            raise RuntimeError(
                '[ERROR] BernSta::parse file does not exist: {:}'.format(
                    self.filename))
        ## could be that the input file is in whatever encoding; replace any
        ## coding errors.
        with open(self.filename, 'r', errors="replace") as f:
            line = f.readline()
            if not line.startswith(
                    'STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'):
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] BernSta::parse expected first line to be {:}'.
                    format(
                        'STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'
                    ))
            self.date = datetime.datetime.strptime(' '.join(
                line.split()[-2:]), '%d-%b-%y %H:%M')  ## e.g. 01-JAN-21 07:31
            line = f.readline()
            if not line.startswith(
                    '--------------------------------------------------------------------------------'
            ):
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] BernSta::parse erronuous second line')
            line = f.readline()
            if not len(line.strip()) == 0:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] BernSta::parse erronuous third line; should be empty'
                )
            line = f.readline()
            if not line.startswith('FORMAT VERSION:'):
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] BernSta::parse expected fourth line to be {:}'.
                    format('FORMAT VERSION:'))
            self.version = float(line.split()[2])
            line = f.readline()
            if not line.startswith('TECHNIQUE:'):
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] BernSta::parse expected fifth line to be {:}'.
                    format('TECHNIQUE:'))
            self.technique = line[line.find(':') + 1:].rstrip()
            ## parse block Type001
            self.__parse_block_001(f)
            ## parse block Type002
            self.__parse_block_002(f)
            ## parse block Type003
            self.__parse_block_003(f)
