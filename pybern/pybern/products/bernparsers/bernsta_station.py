#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
from pybern.products.errors.errors import FileFormatError, ArgumentError, PybernError
from utils.dateutils import date_ranges_overlap
if version_info.major == 2:
  from bernsta_001 import Type001Record as Type001Record
  from bernsta_002 import Type002Record as Type002Record
  from bernsta_003 import Type003Record as Type003Record
else:
  from .bernsta_001 import Type001Record as Type001Record
  from .bernsta_002 import Type002Record as Type002Record
  from .bernsta_003 import Type003Record as Type003Record


MIN_STA_DATE = datetime.datetime.min
MAX_STA_DATE = datetime.datetime.max
FILE_FORMAT = '.STA (Bernese v5.2)'

class StationInformationError(PybernError):
  def __init__(self, station, message, StationRecord, ErrorRecord):
    message = '\n\tFile Format       : {:}'.format(FILE_FORMAT)
    message+= '\n\tError for station :\'{:}\''.format(station)
    message+= '\n\tStation Record    :\'{:}\''.format(StationRecord.compact_str())
    message+= '\n\tErronuous Record  :\'{:}\''.format(ErrorRecord)
    if version_info.major == 2:
      super(ArgumentError, self).__init__(message)
    else:
      super().__init__(message)

class StationRecord:
    def __init__(self, Type001Record, Type002Records=[], Type003Records=[]):
      self.t001rec = Type001Record
      self.t002recs = Type002Records
      self.t003recs = Type003Records

    def compact_str(self):
      str_ = '{:}'.format(self.t001rec)
      for t002 in self.t002rec: str_ += '\n{:}'.format(t002)
      return str_

    def add_002_record(t002rec):
      if t002rec.sta_name != self.t001rec.sta_name:
        raise StationInformationError(self.t001rec.sta_name, '[ERROR] StationRecord::add_002_record Station name does not match', self, t002rec)
      if t002rec.start_date < self.t001rec.start_date or t002rec.stop_date > self.t001rec.stop_date:
        raise StationInformationError(self.t001rec.sta_name, '[ERROR] StationRecord::add_002_record Type002 info has invalid date bounds (#1)', self, t002rec)
      for rec in self.t002rec:
        if date_ranges_overlap(t002rec.start_date, t002rec.stop_date, rec.start_date, rec.stop_date):
          raise StationInformationError(self.t001rec.sta_name, '[ERROR] StationRecord::add_002_record Time overlap in new Type002 record', self, t002rec)
      self.t002recs.append(t002rec)
    
    def add_003_record(t003rec):
      if t003rec.sta_name != self.t001rec.sta_name:
        raise StationInformationError(self.t001rec.sta_name, '[ERROR] StationRecord::add_003_record Station name does not match', self, t003rec)
      if t003rec.start_date < self.t001rec.start_date or t003rec.stop_date > self.t001rec.stop_date:
        raise StationInformationError(self.t001rec.sta_name, '[ERROR] StationRecord::add_003_record Type003 info has invalid date bounds (#1)', self, t003rec)
      self.too3recs.append(t003rec)
