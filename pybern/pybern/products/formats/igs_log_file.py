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
#from bernsta_station import StationRecord
from bernsta_003 import Type003Record
from bernsta_002 import Type002Record, merge_t2_intervals, MAX_STA_DATE
from bernsta_001 import Type001Record

def parse_log_date(dstr):
    if re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}Z\s*$", dstr):
        return datetime.datetime.strptime(dstr, "%Y-%m-%dT%H:%MZ")
    elif re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\s*$", dstr):
        return datetime.datetime.strptime(dstr, "%Y-%m-%d")
    elif re.match(r"^\s*\(?CCYY-MM-DDThh:mmZ\)?\s*$", dstr):
        return MAX_STA_DATE ##datetime.datetime.max
    elif re.match(r"^\s*$", dstr):
        return MAX_STA_DATE ##datetime.datetime.max
    errmsg = '[ERROR] Invalid log datetime string: {:}'.format(dstr)
    raise RuntimeError(errmsg)

def filter_template_block_lines(line_list):
  """ Given a list of lines parsed from a single block of an igs log file, e.g
    line_list=[
    5.  Tied Marker Name         : GOP4
     Tied Marker Usage        : EXCENTRIC PILLAR for GNSS TIME receiver
     Tied Marker CDP Number   : GOP6
                              : average form 44 days of measurement.

    5.x  Tied Marker Name         : 
     Tied Marker Usage        : (SLR/VLBI/LOCAL CONTROL/FOOTPRINT/etc)
     Additional Information   : (multiple lines)
    ]
    that is, as parsed from the function IgsLogFile::parse_block2line_list(),
    this function will remove any block of lines that are generic/templace (e.g
    in the above example all lines from '5.x  Tied Marker Name' to the end)
  """
  repeat = True
  block_open = False
  filtered_list = line_list

  while repeat:
    line_list = filtered_list
    repeat = False
    for i,l in enumerate(line_list):
      if re.match(r"^\s*[0-9]+\.x", l.strip()):
        block_open = True
        start_idx = i
      elif re.match(r"^\s*[0-9]+\.[0-9]+\.x", l.strip()):
        block_open = True
        start_idx = i
      elif l.strip() == '' and block_open:
        stop_idx = i
        del filtered_list[start_idx:stop_idx]
        block_open = False
        repeat = True
        break
  
  if block_open:
    del filtered_list[start_idx:stop_idx]

  return filtered_list

def num_leading_spaces(str):
  """ Return the number of leading whitespaces of given string """
  for i, c in enumerate(str):
    if c != ' ': return i
  return len(str)

def line_matches_block(line, iblock):
  """ Given an integer (iblock), this function will return False if:
      the string 'line' starts with a number followed by a dot, but the number 
      is not iblock.
      This is useful to check if a new line in a log file, is a line that 
      changes the current block
  """
  g = re.match(r"^\s*([0-9]+)\.", line)
  if not g: return True
  nb = int(g.group(1))
  return nb == iblock


def split_field(line):
  """ Split a string on the first ':' character """
  ## beware of lines that hold dates!!
  ## e.g. Date Installed           : 1995-05-13T00:00Z
  l = line.split(':')
  if len(l) > 1:
    ## handle cases where the default (driver) string is there, e.g.
    ## (A*, but note the first A5 is used in SINEX), or
    ## (A20, from rcvr_ant.tab; see instructions)
    ## replace with empty string
    value = '' if re.match(r"^\(A[0-9\*]+.*\)$", ':'.join(l[1:]).strip()) else ':'.join(l[1:]).strip()
    #return l[0].strip(), ':'.join(l[1:]).strip()
    return l[0].strip(), value
  else:
    return line.strip(), None


def add2dict(dict, parent_list, key, value):
  """ Add a key/value pair to a dictionary; the pair is added following the
      hierarchy of 'parents' as define in the parent_list list. That is
      if parent list is: ['5', '1'], and key='k', value='v', then the new, 
      returned dictionary will have a value:
      dict['5']['1'][k] = v
  """
  d = dict
  for p in parent_list:
    if p not in d:
      d[p] = {}
    d = d[p]
  d[key] = value
  return dict

def parse_lines2dict(lines, blocks_dct):
  """ Format one (igs log file) block's line list to a dictionary.
      The line list should be the result of call to 
      IgsLogFile::parse_block2line_list()

      It is expected that the first line in the list, matches on of the
      IgsLogFile::blocks values.

      After the first line, each sub- and sub-sub- block, is appended in a
      dictionary hierarchy, e.g.
      {'9.3': 
        {'1': 
          {'Signal Obstructions': 'TREES', 
          'Effective Dates': '1995-05-13/2001-12-17', 
          'Additional Information': '2001-10-25/2001-12-17 reduction obstructions'},
        '2': 
          {'Signal Obstructions': 'TREES', 
          'Effective Dates': '2001-12-17/2019-03-29', 
          'Additional Information': '2019-02-06/2019-03-29 reduction obstructions'
        }
      }
  """
  ## first line should always be block header
  block = None
  for b in blocks_dct:
    if blocks_dct[b] == lines[0].strip():
      block = b
      break

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

def block2intervals(block):
  """" Split a block 3 '3.   GNSS Receiver Information' or 4 
      '4.   GNSS Antenna Information' to intervals and return them.
      The function will return a list of start/stop tuples, aka:
      [(start1, stop1), (start2, stop2), ...]
  """
  intervals = []
  for interval in block:
    start = install_date(block[interval])
    stop = remove_date(block[interval])
    intervals.append([start, stop])
  return intervals

def make_intervals(b3, b4):
  """ Given the already parsed igs block 3 and 4 dictionaries (aka 
      '3.   GNSS Receiver Information' and '4.   GNSS Antenna Information') as
      parsed from an IgsLogFile instance (see IgsLogFile::parse_block), 
      concatenate the intervals based on changes either on the 3 or 4 block.
  """
  b3_intervals = sorted(block2intervals(b3), key=lambda t: t[0])
  b4_intervals = sorted(block2intervals(b4), key=lambda t: t[0])
  ## check if we have any missing intervals ....
  b3_missing = []
  idx = 0
  while idx < len(b3_intervals) - 1:
      if b3_intervals[idx][1] < b3_intervals[idx+1][0]:
          print('[WRNNG] Missing interval {:} to {:} : no receiver info'.format(b3_intervals[idx][1].strftime('%Y/%m/%d %H:%M:%S'), b3_intervals[idx+1][0].strftime('%Y/%m/%d %H:%M:%S')))
          b3_missing.append([b3_intervals[idx][1], b3_intervals[idx+1][0]])
      idx += 1
  b4_missing = []
  idx = 0
  while idx < len(b4_intervals) - 1:
      if b4_intervals[idx][1] < b4_intervals[idx+1][0]:
          print('[WRNNG] Missing interval {:} to {:} : no antenna info'.format(b4_intervals[idx][1].strftime('%Y/%m/%d %H:%M:%S'), b4_intervals[idx+1][0].strftime('%Y/%m/%d %H:%M:%S')))
          b4_missing.append([b4_intervals[idx][1], b4_intervals[idx+1][0]])
      idx += 1

  ## merge lists, dummy sort on first element
  newl = sorted(b3_intervals+b4_intervals, key=lambda t: t[0])
  #for i in newl: print(i)
  #print('--------------------------------------------------------------------')

  idx = 0
  current_start = newl[0][0]
  dummy=0 ## just to be sure we wont be looping for eternity
  while idx < len(newl) and dummy<500:
      if idx+1 < len(newl) :
          #print('\tcomparing {:} and {:}, current start = {:}'.format(newl[idx], newl[idx+1], current_start));
          assert(newl[idx+1][0] >= current_start)
            
          ## intervals are equal, only keep one and go on ...
          if newl[idx] == newl[idx+1]:
              #print('\ttuples are equal ...')
              newl = newl[0:idx] + newl[idx+1:]

          ## intervals are already ordered, go on ...
          elif newl[idx][0] <= newl[idx][1] <= newl[idx+1][0] <= newl[idx+1][1]:
              #print('\tintervals already ordered ...')
              current_start = newl[idx+1][0]
              idx += 1

          ## e.g. [n, n+1],[n+1, n+2]
          elif newl[idx+1][0] == current_start:
              midpoint = min(newl[idx][1], newl[idx+1][1])
              endpoint = max(newl[idx][1], newl[idx+1][1])
              #print('\tnew intervals {:}/{:} instead of {:}/{:}'.format([current_start, midpoint], [midpoint, endpoint], newl[idx], newl[idx+1]))
              newl[idx] = [current_start, midpoint]
              newl[idx+1] = [midpoint, endpoint]
              current_start = midpoint
              idx += 1
            
          ## messed up intervals handled here, e.g. [n, n+2],[n+1, n+2]
          ## will result in [n,n+1],[n+1,n+2]
          elif newl[idx+1][0] < newl[idx][1]:
              midpoint = min(newl[idx][1], newl[idx+1][1])
              endpoint = max(newl[idx][1], newl[idx+1][1])
              newl = newl[0:idx] + [ [newl[idx][0], newl[idx+1][0]], [newl[idx+1][0],midpoint], [midpoint,endpoint] ] +  newl[idx+2:]
              current_start = midpoint
              idx+=2

          #for i in newl: print(i)
          #print('--------------------------------------------------------------------')
      
      #else: break
      dummy += 1
  
  if len(newl) > 1:
    if newl[len(newl)-2] == newl[len(newl)-1]: newl = newl[0:-1]
    if newl[len(newl)-1] == [MAX_STA_DATE, MAX_STA_DATE]: newl = newl[0:-1]

  ## validate
  # for i in newl: print(i)
  newlc=[]
  for i,v in enumerate(newl):
      if v[0] == v[1]:
        pass
      else:
        assert(v[0] < v[1])
        newlc.append(v)
      if i+1 < len(newl):
          assert(v[1] <= newl[i+1][0])
  newl = newlc
  
  ## remove any info-missing intervals
  newlc=[]
  for i,v in enumerate(newl):
      if v in b3_missing or v in b4_missing:
          print('[WRNNG] Removing interval {:} to {:} cause of missing info ...'.format(v[0].strftime('%Y/%m/%d %H:%M:%S'), v[1].strftime('%Y/%m/%d %H:%M:%S')))
      else:
          newlc.append(v)

  return newlc

def install_date(sub_dict):
  return parse_log_date(sub_dict['Date Installed'])

def remove_date(sub_dict):
  return parse_log_date(sub_dict['Date Removed'])

def block_info_at(t, b):
  """ If b is an IgsLogFile-parsed, block 3 or 4 dictionary (aka a result of
      IgsLogFile::parse_block), then this function will return the sub-block/sub-
      dictionary valid for epoch t (aka it will return the sub-dictionary 4.1, 
      or 4.2, or ....)
      If no matching interval is found, it will return None
  """
  for sb in b:
    if install_date(b[sb]) <= t and remove_date(b[sb]) > t:
      return b[sb]
  return None

class IgsLogFile:

    blocks = {'0': '0.   Form',
      '1': '1.   Site Identification of the GNSS Monument',
      '2': '2.   Site Location Information',
      '3': '3.   GNSS Receiver Information',
      '4': '4.   GNSS Antenna Information',
      '5': '5.   Surveyed Local Ties',
      '6': '6.   Frequency Standard',
      '7': '7.   Collocation Information',
      '8': '8.   Meteorological Instrumentation',
      '9': '9.   Local Ongoing Conditions Possibly Affecting Computed Position',
      '10': '10.  Local Episodic Effects Possibly Affecting Data Quality',
      '11': '11.  On-Site, Point of Contact Agency Information',
      '12': '12.  Responsible Agency (if different from 11.)',
      '13': '13.  More Information'}

    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(filename):
          ermsg = '[ERROR] Failed to find log file {:}!'.format(filename)
          raise RuntimeError(ermsg)

    def parse_block2line_list(self, block_nr):
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
        ermsg = '[ERROR] Igs log files do not have block nr: {:}'.format(
            block_nr)
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
              ret_lines.append(line.rstrip())
              line = fin.readline()

          line = fin.readline()

        return filter_template_block_lines(ret_lines)

    def parse_block(self, block_nr):
      ## block_nr to string if not ...
      try:
        block_nr + 1
        block_nr = '{}'.format(block_nr)
      except:
        pass

      bls = self.parse_block2line_list(block_nr)
      return parse_lines2dict(bls, self.blocks)

    def site_name(self):
      bd = self.parse_block(1)
      name = bd['Four Character ID']
      domes = bd['IERS DOMES Number']
      if re.match(r"^\(A4\)$", name.strip()) or name.strip() == '':
          errmsg = '[ERROR] No valid station name (Four Character ID) field found in log file {:}'.format(self.filename)
          # print(errmsg, file=sys.stderr)
          raise RuntimeError(errmsg)
      if re.match(r"^\(A9\)$", domes.strip()): domes = ''
      installed_at = install_date(bd).date()
      if installed_at == datetime.datetime.max: installed_at = datetime.datetime.min
      return name, domes, installed_at

    def to_001type(self):
      name, domes, installed_at = self.site_name()
      old_name = name + '*'
      return Type001Record(station=(name+' '+domes).strip(), old_name=old_name, start=installed_at, remark=os.path.basename(self.filename))
    
    def to_002type(self):
      bd3 = self.parse_block(3)
      bd4 = self.parse_block(4)
      last_start = datetime.datetime.min
      last_stop = datetime.datetime.min
      
      name, domes, installed_at = self.site_name()
      name = (name + ' ' + domes).strip()

      intervals = make_intervals(bd3, bd4)
      t2records = []
      for t in intervals:
        recinfo = block_info_at(t[0]+datetime.timedelta(minutes=1), bd3)
        antinfo = block_info_at(t[0]+datetime.timedelta(minutes=1), bd4)
        if recinfo is None or antinfo is None:
          if recinfo is None:
            errmsg='[WRNNG] Failed to find a valid Receiver block in log file {:} for epoch {:}'.format(
                self.filename, t[0]+datetime.timedelta(seconds=1))
          if antinfo is None:
            errmsg = '[WRNNG] Failed to find a valid Antenna block in log file {:} for epoch {:}'.format(
                self.filename, t[0]+datetime.timedelta(seconds=1))
          print(errmsg, file=sys.stderr)
          print('[WRNNG] Ommiting time interval {:} to {:} cause of incomplete/missing log information'.format(t[0], t[1]), file=sys.stderr)
          ## raise RuntimeError(errmsg)
        else:
          t2 = Type002Record(station=name, start=t[0], end=t[1], remark='{:}'.format(
              os.path.basename(self.filename)), receiver_type=recinfo['Receiver Type'], receiver_serial=recinfo['Serial Number'], antenna_type=antinfo['Antenna Type'],
              antenna_serial=antinfo['Serial Number'], delta_north=float(antinfo['Marker->ARP North Ecc(m)']), delta_east=float(antinfo['Marker->ARP East Ecc(m)']), delta_up=float(antinfo['Marker->ARP Up Ecc. (m)']))
          t2records.append(t2)
 
      #print('T2 Records:')
      #print('-----------------------------------------------------------------------')
      #for i in t2records: print(i)
      #print('Last date is {:} (max={:})'.format(t2records[len(t2records)-1].stop_date, t2records[len(t2records)-1].stop_date==MAX_STA_DATE))
      #print('-----------------------------------------------------------------------')
      return merge_t2_intervals(t2records)
