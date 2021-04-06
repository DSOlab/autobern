#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
import re
from pybern.products.errors.errors import FileFormatError
utils_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) +
             '/utils/')
sys.path.append(utils_dir)
from dctutils import merge_dicts

FILE_FORMAT = 'BASLST .OUT (Bernese v5.2)'


## header must have been parsed already
def parse_baslst_out(istream):
    dct = {}
    line = istream.readline()
    while line and not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        line = istream.readline()
    if not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_baslst_out  Invalid BERNESE BASLST file; Filed to find \'INPUT AND OUTPUT FILENAMES\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('--------------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        '--------------------------------------------------------------------------'
    ))
    line = istream.readline()
    dct['input_and_output_filenames'] = {}
    while not line.lstrip().startswith(
            '--------------------------------------------------------------------------'
    ):
        name, value = [_.strip() for _ in line.split(':')]
        dct['input_and_output_filenames'][name.replace(
            ' ', '_').lower()] = value if value != '---' else None
        line = istream.readline()
    """
     Options for baseline selection
     ------------------------------
     Observations from:            Any system
     Maximum baseline length:         10.0 km
     Minimum baseline length:          0.0 km
     Station receiver name:
     Exclude receiver name pattern:
    """
    while line and not line.lstrip().startswith(
            'Options for baseline selection'):
        line = istream.readline()
    if not line.lstrip().startswith('Options for baseline selection'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_baslst_out  Invalid BERNESE BASLST file; Filed to find \'Options for baseline selection\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('------------------------------'))
    key = 'Options for baseline selection'.lower().replace(' ', '_')
    dct[key] = {}
    line = istream.readline()
    while line and len(line) > 5:
        assert (line.find(':') > -1 and len(line.split(':')) < 3)
        cols = line.split(':')
        descr = cols[0].strip().lower().replace(' ', '_')
        val = cols[1].strip().lower().replace(' ',
                                              '_') if len(cols) == 2 else ''
        dct[key][descr] = val
        line = istream.readline()
    """
     -------------------------------------------------------------------------------
     File  Phase single difference files
     -------------------------------------------------------------------------------
        1  ${P}/GREECE/OBS/A1PK0630.PSH
        2  ${P}/GREECE/OBS/A1PY0630.PSH
    """
    while line and not line.lstrip().startswith(
            'File  Phase single difference files'):
        line = istream.readline()
    if not line.lstrip().startswith('File  Phase single difference files'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_baslst_out  Invalid BERNESE BASLST file; Filed to find \'File  Phase single difference files\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('------------------------------'))
    key = 'Phase single difference files'.lower().replace(' ', '_')
    dct[key] = {}
    line = istream.readline()
    while line and not line.lstrip().startswith(
            '------------------------------'):
        cols = line.split()
        assert (len(cols) == 2)
        file_nr = int(cols[0])
        file_name = cols[1]
        dct[key][file_name] = {'file_nr': file_nr}
        line = istream.readline()
    """
     FL File name       Sta1 Sta2  Length  Receiver1             Receiver2            AR (%) G R
     -------------------------------------------------------------------------------------------
        A1PK0630.PSH    ANI1 PTK1    48.6  TPS NET-G5            LEICA GR25            -1.0  x x
        A1PY0630.PSH    ANI1 PYLO    53.3  TPS NET-G5            LEICA GR10            -1.0  x x
        PNVL0630.PSH    PONT VLSM    49.1  LEICA GRX1200PRO      LEICA GR10            -1.0  x  
    """
    while line and not line.lstrip().startswith(
            'FL File name       Sta1 Sta2  Length  Receiver1             Receiver2            AR (%) G R'
    ):
        line = istream.readline()
    if not line.lstrip().startswith(
            'FL File name       Sta1 Sta2  Length  Receiver1             Receiver2            AR (%) G R'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_baslst_out  Invalid BERNESE BASLST file; Filed to find \'FL File name       Sta1 Sta2  Length  Receiver1             Receiver2            AR (%) G R\''
        )
    header = [
        'File name', 'Sta1', 'Sta2', 'Length', 'Receiver1', 'Receiver2',
        'AR (%)', 'G', 'R'
    ]
    indexes = [line.find(s) for s in header]
    indexes[-1] = line.rfind('R')
    indexes += [len(line)]
    line = istream.readline()
    assert (line.lstrip().startswith('------------------------------'))
    line = istream.readline()
    while line and len(line) > 20:
        cols = [
            line[indexes[i]:indexes[i + 1]].strip() for i in range(len(header))
        ]
        nd = {
            header[i].replace(' ', '_'): cols[i].strip()
            for i in range(len(header))
        }
        filename_key = None
        for flnm in dct[key]:
            if os.path.basename(flnm) == cols[0].strip():
                filename_key = flnm
                break
        if not filename_key:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] parse_baslst_out  Invalid BERNESE BASLST file; Filed to find baseline {:} in Phase single difference files'
                .format(cols[0].strip()))
        dct[key][flnm] = merge_dicts(dct[key][flnm], nd)
        line = istream.readline()

    return dct
