#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
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

  def __parse_block_001(self, stream):
    ''' Stream should be open and at any line before the line:
        TYPE 001: RENAMING OF STATIONS  
    '''
    ## read and parse Type001 block
    while not line.startswith('TYPE 001: RENAMING OF STATIONS'):
      line = f.readline()
    if not line.startswith('TYPE 001: RENAMING OF STATIONS'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_001 failed to find \'TYPE 001: RENAMING OF STATIONS\' block')
    while not line.startswith('STATION NAME          FLG          FROM                   TO         OLD STATION NAME      REMARK'):
        line = f.readline()
    if not line.startswith('STATION NAME          FLG          FROM                   TO         OLD STATION NAME      REMARK'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_001 failed to find header block for Type 001 (#1)')
    line = f.readline()
    if line.strip() != '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ************************':
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_001 failed to find header block for Type 001 (#2)')
    line = f.readline()
    while line and len(line)>20:
      new_rec = Type001Record(line)
      if new_rec.sta_name in self.stations:
        raise RuntimeError('[ERROR] BernSta::__parse_block_001 Station {:} already parsed! Possible double entry.'.format(new_rec.sta_name))
      self.stations.append(new_rec.sta_name)
      self.dct[new_rec.sta_name]['type001'] = new_rec

  def __parse_block_002(self, stream):
    ''' Stream should be open and at any line before the line:
        TYPE 002: STATION INFORMATION
    '''
    ## read and parse Type002 block
    while not line.startswith('TYPE 002: STATION INFORMATION'):
      line = f.readline()
    if not line.startswith('TYPE 002: STATION INFORMATION'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find \'TYPE 002: STATION INFORMATION\' block')
    while not line.startswith('STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'):
        line = f.readline()
    if not line.startswith('STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#1)')
    line = f.readline()
    if line.strip() != '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************':
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#2)')
    line = f.readline()
    while line and len(line)>20:
      new_rec = Type002Record(line)
      if new_rec.sta_name not in self.stations:
        raise RuntimeError('[ERROR] BernSta::__parse_block_002 Station {:} has Type 002 record but not included in Type 001'.format(new_rec.sta_name))
      if 'type002' in self.dct[new_rec.sta_name]:
        self.dct[new_rec.sta_name]['type002'].append(new_rec)
      else:
        self.dct[new_rec.sta_name]['type002'] = [new_rec]

  def __parse_block_003(self, stream):
    ''' Stream should be open and at any line before the line:
    '''
    ## read and parse Type002 block
    while not line.startswith('TYPE 002: STATION INFORMATION'):
      line = f.readline()
    if not line.startswith('TYPE 002: STATION INFORMATION'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find \'TYPE 002: STATION INFORMATION\' block')
    while not line.startswith('STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'):
        line = f.readline()
    if not line.startswith('STATION NAME          FLG          FROM                   TO         RECEIVER TYPE         RECEIVER SERIAL NBR   REC #   ANTENNA TYPE          ANTENNA SERIAL NBR    ANT #    NORTH      EAST      UP      DESCRIPTION             REMARK'):
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#1)')
    line = f.readline()
    if line.strip() != '****************      ***  YYYY MM DD HH MM SS  YYYY MM DD HH MM SS  ********************  ********************  ******  ********************  ********************  ******  ***.****  ***.****  ***.****  **********************  ************************':
      raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::__parse_block_002 failed to find header block for Type 002 (#2)')
    line = f.readline()
    while line and len(line)>20:
      new_rec = Type002Record(line)
      if new_rec.sta_name not in self.stations:
        raise RuntimeError('[ERROR] BernSta::__parse_block_002 Station {:} has Type 002 record but not included in Type 001'.format(new_rec.sta_name))
      if 'type002' in self.dct[new_rec.sta_name]:
        self.dct[new_rec.sta_name]['type002'].append(new_rec)
      else:
        self.dct[new_rec.sta_name]['type002'] = [new_rec]
  def parse(self):
    if not os.path.isfile(self.filename):
      raise RuntimeError('[ERROR] BernSta::parse file does not exist: {:}'.format(self.filename))
    with open(self.filename, 'r') as f:
      line = f.readline()
      if not line.startswith('STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'):
        raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::parse expected first line to be {:}'.format('STATION INFORMATION FILE FOR BERNESE GNSS SOFTWARE 5.2'))
      self.date = datetime.datetime.strptime(' '.join(line.split()[-2:]), '%d-%b-%y %H:%M')  ## e.g. 01-JAN-21 07:31
      line = f.readline()
      if not line.startswith('--------------------------------------------------------------------------------'):
        raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::parse erronuous second line')
      line = f.readline()
      if not len(line.strip())==0:
        raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::parse erronuous third line; should be empty')
      line = f.readline()
      if not line.startswith('FORMAT VERSION:'):
        raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::parse expected fourth line to be {:}'.format('FORMAT VERSION:'))
      self.version = float(line.split()[2])
      line = f.readline()
      if not line.startswith('TECHNIQUE:'):
        raise FileFormatError(FILE_FORMAT, line, '[ERROR] BernSta::parse expected fifth line to be {:}'.format('TECHNIQUE:'))
      self.technique = line[line.find(':')+1:].rstrip()
      
