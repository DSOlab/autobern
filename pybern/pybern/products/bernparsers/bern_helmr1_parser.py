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

FILE_FORMAT = 'HELMR1 .OUT (Bernese v5.2)'


## header must have been parsed already
def parse_helmr1_out(istream):
    dct = {}
    line = istream.readline()
    dct['files'] = {}
    """
    FILE 1: APR210630.CRD: NTUA_DDP_210630: Extrapolate coordinates
    FILE 2: DSO210630.CRD: RNX2SNX_210630: Final coordinate/troposphere results
    """
    while not line.lstrip().startswith('FILE 1:'):
        line = istream.readline()
    if not line.lstrip().startswith('FILE 1:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; Filed to find input files'
        )
    while line.lstrip().startswith('FILE '):
        cols = line.split(':')
        assert (len(cols) >= 2)
        file_nr = int(cols[0].replace('FILE', '').strip())
        file_nm = cols[1].strip()
        file_ds = ' '.join(cols[2:]) if len(cols) > 2 else ''
        dct['files'][file_nr] = {'filename': file_nm, 'description': file_ds}
        line = istream.readline()
    """
    LOCAL GEODETIC DATUM: IGS14
    RESIDUALS IN LOCAL SYSTEM (NORTH, EAST, UP)
    """
    while not line.lstrip().startswith('LOCAL GEODETIC DATUM:'):
        line = istream.readline()
    if not line.lstrip().startswith('LOCAL GEODETIC DATUM:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; Filed to find \'LOCAL GEODETIC DATUM:\''
        )
    cols = line.split(':')
    assert (len(cols) == 2)
    dct[cols[0].strip().replace(' ', '_').lower()] = cols[1].strip()
    line = istream.readline()
    assert (line.strip() == 'RESIDUALS IN LOCAL SYSTEM (NORTH, EAST, UP)')
    """
     ---------------------------------------------------------------------
     | NUM |      NAME        | FLG |     RESIDUALS IN MILLIMETERS   |   |
     ---------------------------------------------------------------------
     |     |                  |     |                                |   |
     |  40 | ANIK 12666M001   | P A |      -2.88      0.99      2.23 | M |
     |  41 | ANKR 20805M002   | P A |      -1.72      5.12      1.93 | M |
     | 413 | POLV 12336M001   | I W |       0.02     -0.16     -8.40 |   |
     | 415 | PONT 12626M001   | P A |      -5.46     -2.68      7.23 | M |
     | 609 | ZIMM 14001M004   | I W |      -1.14     -0.36      1.84 |   |
     |     |                  |     |                                |   |
     ---------------------------------------------------------------------
     |     | RMS / COMPONENT  |     |       3.66      3.25      6.01 |   |
     |     | MEAN             |     |       0.00     -0.00     -0.00 |   |
     |     | MIN              |     |      -5.25     -5.05     -8.40 |   |
     |     | MAX              |     |       4.69      3.50      6.94 |   |
     ---------------------------------------------------------------------
    """
    dct['stations'] = {}
    while not line.lstrip().startswith(
            '---------------------------------------------------------------------'
    ):
        line = istream.readline()
    if not line.lstrip().startswith(
            '---------------------------------------------------------------------'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; Expected first \'-------\' line, found {:}'
            .format(line.strip()))
    line = istream.readline()
    assert (line.lstrip().startswith(
        '| NUM |      NAME        | FLG |     RESIDUALS IN MILLIMETERS   |   |')
           )
    line = istream.readline()
    assert (line.lstrip().startswith(
        '---------------------------------------------------------------------')
           )
    line = istream.readline()
    assert (len(line.split('|')) >= 6 and line.split('|')[0].strip() == '')
    line = istream.readline()
    while line and len(line) > 69:
        cols = [
            c.strip()
            for c in line[line.find('|') + 1:line.rfind('|')].strip().split('|')
        ]
        assert (len(cols) == 5)
        h = [
            'residuals_in_millimeters_north', 'residuals_in_millimeters_east',
            'residuals_in_millimeters_up'
        ]
        ## following block does not work for Python 2.7 ...
        #dct['stations'][cols[1]] = dict([
        #    ('num', int(cols[0])), ('flag', cols[2]),
        #    *[(t[0], float(t[1])) for t in zip(h, cols[3].split())],
        #    ('mark', cols[4])
        #])
        print(('num', int(cols[0])))
        print(('flag', cols[2]))
        print(zip(h, [float(x) for x in cols[3].split()]))
        print(('mark', cols[4]))
        dct['stations'][cols[1]] = dict(
            [('num', int(cols[0])), ('flag', cols[2]),
            ('mark', cols[4])] +
            zip(h, [float(x) for x in cols[3].split()])
        )
        line = istream.readline()
        if line.strip().replace(' ', '') == '||||||':
            break
    line = istream.readline()
    assert (line.lstrip().startswith(
        '---------------------------------------------------------------------')
           )
    for i in range(4):
        line = istream.readline()
        cols = [
            c.strip()
            for c in line[line.find('|') + 1:line.rfind('|')].strip().split('|')
        ]
        assert (len(cols) == 5)
        title = cols[1].lower().replace(' ', '_')
        keys = ['_'.join(t) for t in zip('north east up'.split(), [title] * 3)]
        vals = [float(col) for col in cols[3].split()]
        for t in zip(keys, vals):
            dct[t[0]] = t[1]
    line = istream.readline()
    assert (line.lstrip().startswith(
        '---------------------------------------------------------------------')
           )
    """
     NUMBER OF PARAMETERS  :     3
     NUMBER OF COORDINATES :    15
     RMS OF TRANSFORMATION :    4.48 MM 
    """
    while not line.lstrip().startswith('NUMBER OF PARAMETERS'):
        line = istream.readline()
    if not line.lstrip().startswith('NUMBER OF PARAMETERS'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; failed to find \'NUMBER OF PARAMETERS\''
        )
    cols = [x.strip() for x in line.split(':')]
    assert (len(cols) == 2)
    dct[cols[0].replace(' ', '_').lower()] = int(cols[1])
    line = istream.readline()
    assert (line.lstrip().startswith('NUMBER OF COORDINATES'))
    cols = [x.strip() for x in line.split(':')]
    assert (len(cols) == 2)
    dct[cols[0].replace(' ', '_').lower()] = int(cols[1])
    line = istream.readline()
    assert (line.lstrip().startswith('RMS OF TRANSFORMATION'))
    cols = [x.strip() for x in line.split(':')]
    assert (len(cols) == 2)
    dct[cols[0].replace(' ', '_').lower()] = float(cols[1].split()[0])
    assert (cols[1].split()[1].strip() == 'MM')
    """
      BARYCENTER COORDINATES:

      LATITUDE              :    54 26 23.02
      LONGITUDE             :    15 16  9.47
      HEIGHT                :        -111.852 KM
    """
    dct['barycenter'] = {}
    while not line.lstrip().startswith('BARYCENTER COORDINATES:'):
        line = istream.readline()
    if not line.lstrip().startswith('BARYCENTER COORDINATES:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; failed to find \'BARYCENTER COORDINATES:\''
        )
    line = istream.readline()
    line = istream.readline()
    cols = [y for x in line.split(':') for y in x.split()]
    assert (cols[0] == 'LATITUDE')
    dct['barycenter']['latitude'] = float(
        cols[1]) + float(cols[2]) / 60e0 + float(cols[3]) / 3600e0
    line = istream.readline()
    cols = [y for x in line.split(':') for y in x.split()]
    assert (cols[0] == 'LONGITUDE')
    dct['barycenter']['longitude'] = float(
        cols[1]) + float(cols[2]) / 60e0 + float(cols[3]) / 3600e0
    line = istream.readline()
    cols = [y for x in line.split(':') for y in x.split()]
    assert (cols[0] == 'HEIGHT' and cols[2] == 'KM')
    dct['barycenter']['height'] = float(cols[1])
    """
     PARAMETERS:

     TRANSLATION IN  N     :           0.00     +-  2.00    MM
     TRANSLATION IN  E     :          -0.00     +-  2.00    MM
     TRANSLATION IN  U     :          -0.00     +-  2.00    MM
    """
    while not line.lstrip().startswith('PARAMETERS:'):
        line = istream.readline()
    if not line.lstrip().startswith('PARAMETERS:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; failed to find \'PARAMETERS:\''
        )
    line = istream.readline()
    line = istream.readline()
    key = 'parameters'
    dct[key] = {}
    while line and len(line) > 10:
        cols = line.split(':')
        header = '_'.join(cols[0].split())
        value, symbl, stddev, units = cols[1].split()
        assert (symbl == '+-')
        dct[key][header] = {
            'value': float(value),
            'sigma': float(stddev),
            'units': units
        }
        line = istream.readline()
    """
    NUMBER OF ITERATIONS  :     1
    """
    while not line.lstrip().startswith('NUMBER OF ITERATIONS'):
        line = istream.readline()
    if not line.lstrip().startswith('NUMBER OF ITERATIONS'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_helmr1_out  Invalid BERNESE HELMR1 file; failed to find \'NUMBER OF ITERATIONS:\''
        )
    dct['NUMBER OF ITERATIONS'.lower().replace(' ', '_')] = int(
        line.split(':')[1].strip())

    return dct
