#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import os
import re
import sys

bernp_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/bernparsers/')
sys.path.append(bernp_dir)
from bernsta_001 import Type001Record
from bernsta_002 import Type002Record
from bernsta_003 import Type003Record
from bernsta_station import StationRecord

def num_leading_spaces(str):
  for i, c in enumerate(str):
    if c != ' ': return i
  return len(str)

def line_matches_block(line, iblock):
  g = re.match(r"^\s*([0-9]+)\.", line)
  if not g: return True
  nb = int(g.group(1))
  return nb == iblock

def split_field(line):
  l = line.split(':')
  if len(l) > 1:
    return l[0].strip(), l[1].strip()
  else:
    return line.strip(), None

def add2dict(dict, parent_list, key, value):
  d = dict
  for p in parent_list:
    if p not in d:
      d[p] = {}
    d = d[p]
  d[key] = value
  return dict

def parse_lines2dict(lines, blocks_dct):
  ## first line should always be block header
  block = None
  for b in blocks_dct:
    if blocks_dct[b] == lines[0].strip():
      block = b
      break;

  assert block is not None

  ret_dict = {}
  parent_list = []

  for line in lines[1:]: 
    if line != '':

      ## check for sub or sub/sub tag, i.e. X.Y or X.Y.Z
      g = re.match(r"^\s*([0-9]+)?\.?([0-9]+)?\.?([0-9]+)?\.?", line)
      key, value = split_field(line)
      
      if g.groups() == (None, None, None):
        ret_dict = add2dict(ret_dict, parent_list, key, value)
      
      elif g[1] != None and g[2] != None:
        sub_header = g[1] + '.' + g[2]
        parent_list = [sub_header]

        if g[3] != None:
          parent_list = [parent_list[0], g[3]]

        key = re.sub(r"^\s*[0-9]*\.?[0-9]*\.?[0-9]*", "", key).lstrip()
        ret_dict = add2dict(ret_dict, parent_list, key, value)

  return ret_dict

class IgsLogFile:
    
    blocks = {'0':'0.   Form', 
      '1': '1.   Site Identification of the GNSS Monument', 
      '2': '2.   Site Location Information', 
      '3': '3.   GNSS Receiver Information', 
      '4': '4.   GNSS Antenna Information', 
      '5': '5.   Surveyed Local Ties', 
      '6': '6.   Frequency Standard', 
      '7': '7.   Collocation Information', 
      '8': '8.   Meteorological Instrumentation', 
      '9': '9.   Local Ongoing Conditions Possibly Affecting Computed Position', 
      '10':'10.  Local Episodic Effects Possibly Affecting Data Quality', 
      '11':'11.  On-Site, Point of Contact Agency Information', 
      '12':'12.  Responsible Agency (if different from 11.)', 
      '13':'13.  More Information'}

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
          ermsg = '[ERROR] Failed to find log file {:}!'.format(filename)
          raise RuntimeError(ermsg)
        #if not self.check_format():
        #    msg = '[ERROR] Failed to find/validate IONEX file: {:}'.format(
        #        self.filename)
        #    raise RuntimeError(msg)
        #self.read_header()

    def parse_block2line_list(self, block_nr, skip_empty_lines=True):
      """ Parse the file; return all lines of the relevant block as a list
          (of lines/strings)
      """
      ## block_nr to string if not ...
      try:
        block_nr + 1
        block_nr = '{}'.format(block_nr)
      except:
        pass

      if block_nr not in self.blocks:
        ermsg = '[ERROR] Igs log files do not have block nr: {:}'.format(block_nr)
        raise RuntimeError(ermsg)

      ib = int(block_nr)
      ret_lines = []
      block_found = False

      with open(self.filename, 'r') as fin:
        line = fin.readline()
        while line and not block_found:
          if line.lstrip().startswith(self.blocks[block_nr]):
            ## found the block we are looking for ....
            ## stop conditions: 
            ## 1. EOF
            ## 2. line starts with number other than block_nr
            while line and line_matches_block(line, ib):
              block_found = True
              if skip_empty_lines and line.strip() == '':
                pass
              else:
                ret_lines.append(line.rstrip())
              line = fin.readline()

          line = fin.readline()

        return ret_lines

    def parse_block(self, block_nr):
      ## block_nr to string if not ...
      try:
        block_nr + 1
        block_nr = '{}'.format(block_nr)
      except:
        pass

      bls = self.parse_block2line_list(block_nr, skip_empty_lines=True)
      return parse_lines2dict(bls, self.blocks)

  def 
