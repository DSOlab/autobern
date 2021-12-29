#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
import operator
from pybern.products.errors.errors import FileFormatError
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/utils/')
formats_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/formats/')
sys.path.append(utils_dir)
sys.path.append(formats_dir)
from smart_open import smart_open
from igs_log_file import IgsLogFile
from bernsta_001 import Type001Record
from bernsta_002 import Type002Record
from bernsta_003 import Type003Record

'''
STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2           16-JAN-21 13:11
--------------------------------------------------------------------------------

FORMAT VERSION: 1.01
TECHNIQUE:      GNSS
'''
FILE_FORMAT = '.STA (Bernese v5.2)'


class BernStaInfo:

    @staticmethod
    def get_equality_operator(use_four_char_id):

        def compare_four_char_id(left, right):
            return left[0:4] == right[0:4]

        if use_four_char_id:
            return compare_four_char_id
        else:
            return operator.eq

    def __init__(self):
        self.stations = []
        self.dct = {}
        self.source_list = []

    def filter(self, station_list, use_four_char_id=False):
        new_stations = []
        new_dct = {}
        op = BernStaInfo.get_equality_operator(use_four_char_id)
        ## well, we can't use
        #[ new_stations.append(sta) for sta in self.stations if sta in station_list ]
        ## cause we need to overload the 'in' function, so do it explicitely,
        ## see https://docs.python.org/3.6/reference/expressions.html#membership-test-details
        [
            new_stations.append(sta) for sta in self.stations if any(
                op(sta, e) for e in station_list)
        ]
        for sta in new_stations:
            new_dct[sta] = self.dct[sta]
        new_info = BernStaInfo()
        new_info.stations, new_info.dct, new_info.source_list = new_stations, new_dct, self.source_list
        return new_info

    def station_info(self, station, use_four_char_id=False):
        op = BernStaInfo.get_equality_operator(use_four_char_id)
        for key in self.stations:
            if op(station, key):
                return self.dct[key]
        return None
    
    def update_from_log(self, igs_log_file):
        ## create the log file instance
        log = IgsLogFile(igs_log_file)
        ## parse the first block to get name/domes
        name, domes, _ = log.site_name()
        ## check if the site is included in this instance
        binfo = self.station_info(name, True)
        ## we will need to report later, so hold the STA(s) filename(s) in a var
        stafn=','.join([x.filename for x in self.source_list])
        ## if binfo is None, site is not included in STA ....
        if binfo is None:
            self.stations += [name]
            self.dct[name] = {'type001': [
                log.to_001type()], 'type002': log.to_002type()}
            return 0
        else:
            if len(binfo['type001']) > 1:
                print('[ERROR] Too many Type 001 records for station {:} in STA file {:}'.format(name, stafn), file=sys.stderr)
                return 1
            
            t1 = log.to_001type()
            if not binfo['type001'][0].equal_except_remark(t1):
                print('[WRNNG] Failed to join Type 001 records for station {:}; .STA={:}, log={:}'.format(name, stafn, igs_log_file), file=sys.stderr)
                return 2
            
            t2 = log.to_002type()
            if len(t2) != len(binfo['type002']):
                print('[WRNNG] Failed to join Type 002 records for station {:}; .STA={:}, log={:}'.format(name, stafn, igs_log_file), file=sys.stderr)
                return 2
            else:
                for idx, rec in enumerate(binfo['type002']):
                    if not rec.equal_except(t2[idx], 'description', 'remark'):
                        print('[WRNNG] Failed to join Type 002 records for station {:} and index: {:}; .STA={:}, log={:}'.format(
                            name, idx, stafn, igs_log_file), file=sys.stderr)
                        return 2
            

    @staticmethod
    def dump_header(outfile=sys.stdout,
                    dt=datetime.datetime.now(),
                    formatv=1.01,
                    technique='GNSS'):
        date_str = dt.strftime('%d-%b-%y %H:%M')
        header_str = """STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2           {:}
--------------------------------------------------------------------------------

FORMAT VERSION: {:4.2f}
TECHNIQUE:      {:}""".format(date_str, formatv, technique)
        print(header_str, file=outfile)

    def dump_as_sta(self, outfile=None, station_list=None):
        ### None prints to STDOUT
        station_list = self.stations if station_list is None else station_list
        with smart_open(outfile) as outfile:
            BernStaInfo.dump_header(outfile)
            print("", file=outfile)
            Type001Record.dump_header(outfile)
            for sta in station_list:
                [print(inst, file=outfile) for inst in self.dct[sta]['type001']]
            print("", file=outfile)
            Type002Record.dump_header(outfile)
            for sta in station_list:
                [print(inst, file=outfile) for inst in self.dct[sta]['type002']]
            print("", file=outfile)
            Type003Record.dump_header(outfile)
            for sta in station_list:
                if 'type003' in self.dct[sta]:
                    [
                        print(inst, file=outfile)
                        for inst in self.dct[sta]['type003']
                    ]


class BernSta:

    def __init__(self, filename):
        self.filename = filename

    def __parse_block_001(self, stream, bernstainfo):
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
                if new_rec.sta_name in bernstainfo.stations:
                    bernstainfo.dct[new_rec.sta_name]['type001'].append(new_rec)
                else:
                    bernstainfo.stations.append(new_rec.sta_name)
                    bernstainfo.dct[new_rec.sta_name] = {'type001': [new_rec]}
            line = stream.readline()

    def __parse_block_002(self, stream, bernstainfo, missing_is_error=False):
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
            if new_rec.sta_name not in bernstainfo.stations:
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
                if 'type002' in bernstainfo.dct[new_rec.sta_name]:
                    bernstainfo.dct[new_rec.sta_name]['type002'].append(new_rec)
                else:
                    bernstainfo.dct[new_rec.sta_name]['type002'] = [new_rec]
            line = stream.readline()

    def __parse_block_003(self, stream, bernstainfo, missing_is_error=False):
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
                '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  *******'
        ):
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] BernSta::__parse_block_003 failed to find header block for Type 003 (#2)'
            )
        line = stream.readline()
        while line and len(line.strip()) > 20:
            new_rec = Type003Record(line)
            if new_rec.sta_name not in bernstainfo.stations:
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
                if 'type003' in bernstainfo.dct[new_rec.sta_name]:
                    bernstainfo.dct[new_rec.sta_name]['type003'].append(new_rec)
                else:
                    bernstainfo.dct[new_rec.sta_name]['type003'] = [new_rec]
            line = stream.readline()

    def parse(self):
        if not os.path.isfile(self.filename):
            raise RuntimeError(
                '[ERROR] BernSta::parse file does not exist: {:}'.format(
                    self.filename))
        binfo = BernStaInfo()
        ## could be that the input file is in whatever encoding; replace any
        ## coding errors.
        with open(self.filename, 'r', errors="replace") as f:
            line = f.readline()
            self.title = line.strip()
            #if not line.startswith(
            #        'STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'):
            #    raise FileFormatError(
            #        FILE_FORMAT, line,
            #        '[ERROR] BernSta::parse expected first line to be {:}'.
            #        format(
            #            'STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'
            #        ))
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
            self.__parse_block_001(f, binfo)
            ## parse block Type002
            self.__parse_block_002(f, binfo)
            ## parse block Type003
            self.__parse_block_003(f, binfo)
        binfo.source_list.append(self)
        return binfo
