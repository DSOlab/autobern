#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
from pybern.products.errors.errors import FileFormatError
## new header for BERN54
"""
===================================================================================================================================
 Bernese GNSS Software, Version 5.4
 -----------------------------------------------------------------------------------------------------------------------------------
 Program        : ADDNEQ2
 Output-version : 1.1
 Purpose        : Combine normal equation systems
 -----------------------------------------------------------------------------------------------------------------------------------
 Campaign       : ${P}/EPNB23
 Default session: 0500 year 2026
 Date           : 21-May-2026 13:50:20
 User name      : bpe54
 ===================================================================================================================================
"""


def parse_generic_out_header(istream):
    FILE_FORMAT = 'Generic .OUT (Bernese v5.4)'
    dct = {}
    line = istream.readline()
    while not line.lstrip().startswith(
            '==============================================================================='
    ):
        line = istream.readline()
    line = istream.readline()
    if not line.lstrip().startswith('Bernese GNSS Software, Version 5.4'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected \'Bernese GNSS Software, Version 5.4\''
        )
    line = istream.readline()
    if not line.lstrip().startswith(
            '-------------------------------------------------------------------------------'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Error (#2)'
        )
    line = istream.readline()
    if not line.lstrip().startswith('Program'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected Program line'
        )
    else:
        dct['program'] = line.split(':')[1].strip()
    line = istream.readline()
    if line.lstrip().startswith('Output-version'):
        dct['output_version'] = line.split(':')[1].strip()
        line = istream.readline()
    if not line.lstrip().startswith('Purpose'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected Purpose line'
        )
    else:
        dct['purpose'] = line.split(':')[1].strip()
    line = istream.readline()
    if not line.lstrip().startswith(
            '-------------------------------------------------------------------------------'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Error (#3)'
        )
    line = istream.readline()
    if not line.lstrip().startswith('Campaign'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected Campaign line'
        )
    else:
        dct['campaign'] = line.split(':')[1].strip()
    line = istream.readline()
    if not line.lstrip().startswith('Default session'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected Session line'
        )
    else:
        dct['session'] = int(line.split(':')[1].strip().split()[0])
        dct['year'] = int(line.split(':')[1].strip().split()[2])
    line = istream.readline()
    if not line.lstrip().startswith('Date'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected Date line'
        )
    else:
        dct['date'] = datetime.datetime.strptime(' '.join(line.split()[2:4]),
                                                 '%d-%b-%Y %H:%M:%S')
    line = istream.readline()
    if not line.lstrip().startswith('User name'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Expected User line'
        )
    else:
        dct['user'] = line.split(':')[1].strip()
    line = istream.readline()
    if not line.lstrip().startswith(
            '==============================================================================='
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_generic_header Invalid BERNESE Generic Header; Error (#4)'
        )
    return dct
