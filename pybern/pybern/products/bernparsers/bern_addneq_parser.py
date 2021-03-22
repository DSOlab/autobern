#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
from pybern.products.errors.errors import FileFormatError

FILE_FORMAT = 'ADDNEQ2 .OUT (Bernese v5.2)'


def nq_index_to_file(dct, idx):
    # dct[input_normal_equation_files][${P}/GREECE/SOL/DSO0630001.NQ0] = { 'file': 1, ...}
    if not 'input_normal_equation_files' in dct:
        return None
    d = dct['input_normal_equation_files']
    for key, val in d.items():
        for key2, val2 in val.items():
            if key2 == 'file' and val2 == idx:
                return key
    return None

def max_nq_index(dct):
    # dct[input_normal_equation_files][${P}/GREECE/SOL/DSO0630001.NQ0] = { 'file': 1, ...}
    if not 'input_normal_equation_files' in dct:
        return None
    d = dct['input_normal_equation_files']
    max_idx = 0
    nr_files = 0
    for key, val in d.items():
        nr_files+=1
        if val['file'] > max_idx: max_idx = val['file']
    assert(max_idx == nr_files)
    return max_idx


## header must have been parsed already
def parse_addneq_out(istream):
    dct = {}
    line = istream.readline()
    while not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        line = istream.readline()
    if not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'INPUT AND OUTPUT FILENAMES\''
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
     INPUT NORMAL EQUATION FILES
     ---------------------------

     -----------------------------------------------------------------------------------------------------------------------------------
     File  Name                             
     -----------------------------------------------------------------------------------------------------------------------------------
        1  ${P}/GREECE/SOL/DSO0630001.NQ0   
     -----------------------------------------------------------------------------------------------------------------------------------
    """
    key = 'INPUT NORMAL EQUATION FILES'.lower().replace(' ', '_')
    dct[key] = {}
    while not line.lstrip().startswith('INPUT NORMAL EQUATION FILES'):
        line = istream.readline()
    if not line.lstrip().startswith('INPUT NORMAL EQUATION FILES'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'INPUT NORMAL EQUATION FILES\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('---------------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        '--------------------------------------------------------------------------'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith('File  Name'))
    line = istream.readline()
    assert (line.lstrip().startswith(
        '--------------------------------------------------------------------------'
    ))
    line = istream.readline()
    while line and not line.lstrip().startswith(
            '--------------------------------------------------------------------------'
    ):
        cols = line.split()
        assert (len(cols) == 2)
        dct[key][cols[1]] = {
            'file': int(cols[0])
        }  ## aka dct[input_normal_equation_files][${P}/GREECE/SOL/DSO0630001.NQ0] = { 'file': 1, ...}
        line = istream.readline()
    assert (line.lstrip().startswith(
        '--------------------------------------------------------------------------'
    ))
    """
     Main characteristics of normal equation files:
     ---------------------------------------------

     File  From                 To                   Number of observations / parameters / degree of freedom
     -----------------------------------------------------------------------------------------------------------------------------------
        1  2021-03-04 00:00:00  2021-03-05 00:00:00                 119303         2072       117231
    """
    while not line.lstrip().startswith(
            'Main characteristics of normal equation files:'):
        line = istream.readline()
    if not line.lstrip().startswith(
            'Main characteristics of normal equation files:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'Main characteristics of normal equation files:\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('---------------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        'File  From                 To                   Number of observations / parameters / degree of freedom'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith('---------------------------'))
    line = istream.readline()
    tmp_index_list = []
    while line and len(line) > 90:
        cols = line.split()
        assert (len(cols) == 8)
        nq_file_name = nq_index_to_file(dct, int(cols[0]))
        dct[key][nq_file_name]['from'] = datetime.datetime.strptime(
            ' '.join([cols[1], cols[2]]), '%Y-%m-%d %H:%M:%S')
        dct[key][nq_file_name]['to'] = datetime.datetime.strptime(
            ' '.join([cols[3], cols[4]]), '%Y-%m-%d %H:%M:%S')
        dct[key][nq_file_name]['number_of_observations'] = int(cols[5])
        dct[key][nq_file_name]['number_of_parameters'] = int(cols[6])
        dct[key][nq_file_name]['degree_of_freedom'] = int(cols[7])
        line = istream.readline()
    """
     Number of parameters:
     --------------------

     Parameter type                                1
     -----------------------------------------------------------------------------------------------------------------------------------
     Station coordinates                          78
     Site-specific troposphere parameters        754
     -----------------------------------------------------------------------------------------------------------------------------------
     Total number of explicit parameters         832
     Total number of implicit parameters        1240
     -----------------------------------------------------------------------------------------------------------------------------------
     Total number of adjusted parameters        2072
    """
    while not line.lstrip().startswith('Number of parameters:'):
        line = istream.readline()
    if not line.lstrip().startswith('Number of parameters:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'Number of parameters:\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('--------------------'))
    line = istream.readline()  ## empty line
    while line and len(line) > 45:
        if not line.lstrip().startswith(
                '--------------------------------------------------------------------------'
        ):
            name, value = line[0:40].strip().lower().replace(' ', '_'), int(
                line[40:].strip())
            dct[name] = value
        line = istream.readline()
    """
    A priori sigma of unit weight:                    0.0010 m
    """
    while not line.lstrip().startswith('A priori sigma of unit weight:'):
        line = istream.readline()
    if not line.lstrip().startswith('A priori sigma of unit weight:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'A priori sigma of unit weight:\''
        )
    dct['a_priori_sigma_of_unit_weight'] = float(line.split()[-2])
    assert (line.split()[-1] == 'm')
    line = istream.readline()
    """
     A priori station coordinates:              ${P}/GREECE/STA/APR210630.CRD
    """
    while not line.lstrip().startswith('A priori station coordinates:'):
        line = istream.readline()
    if not line.lstrip().startswith('A priori station coordinates:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_addneq_out  Invalid BERNESE ADDNEQ file; Filed to find \'A priori station coordinates:\''
        )
    dct['a_priori_station_coordinates'] = line.split(':')[1].strip()
    line = istream.readline()
    """
                                                A priori station coordinates                 A priori station coordinates
                                                          IGS14                          Ellipsoidal in local geodetic datum
    ------------------------------------------------------------------------------------------------------------------------------------
     num  Station name     obs e/f/h        X (m)           Y (m)           Z (m)        Latitude       Longitude    Height (m)
    ------------------------------------------------------------------------------------------------------------------------------------
       1  ANIK 12666M001    Y  ESTIM   4729934.24724   1938158.24406   3801984.49618     36.8260208     22.2820675     47.75303
       2  ANKR 20805M002    Y  ESTIM   4121948.39664   2652187.85380   4069023.88153     39.8873728     32.7584702    976.00388
       3  ANKY 18594M001    Y  ESTIM   4752742.59963   2046958.05616   3716342.57387     35.8669631     23.3010547    176.22475
   """
    dct['stations'] = {}
    while line and not line.lstrip().startswith(
            'A priori station coordinates                 A priori station coordinates'
    ):
        line = istream.readline()
    if not line.lstrip().startswith(
            'A priori station coordinates                 A priori station coordinates'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'A priori station coordinates\''
        )
    line = istream.readline()
    dct['reference_frame'] = line.split()[0]
    line = istream.readline()
    assert (line.lstrip().startswith(
        '---------------------------------------------------------------------------'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith(
        'num  Station name     obs e/f/h        X (m)           Y (m)           Z (m)        Latitude       Longitude    Height (m)'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith(
        '---------------------------------------------------------------------------'
    ))
    line = istream.readline()
    while line and len(line) > 115:
        sta_num, sta_nam = int(line[0:5]), line[5:22].strip()
        cols = line[22:].split()
        assert (len(cols) == 8)
        dct['stations'][sta_num] = {
            'station_name': sta_nam,
            'obs': cols[0],
            'e/f/h': cols[1]
        }
        for k, v in zip(['X', 'Y', 'Z', 'Latitude', 'Longitude', 'Height'],
                        [float(c) for c in cols[2:]]):
            dct['stations'][sta_num][k] = v
        line = istream.readline()
    """
     Network constraints: 

     Component                      A priori sigma  Unit
     -----------------------------------------------------------------------------------------------------------------------------------
     DX    Translation  Coordinates     0.00001     m
     DY    Translation  Coordinates     0.00001     m
     DZ    Translation  Coordinates     0.00001     m
    """
    key = 'network_constraints'
    dct[key]={}
    while line and not line.lstrip().startswith(
            'Network constraints:'
    ):
        line = istream.readline()
    if not line.lstrip().startswith(
            'Network constraints:'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Network constraints:\''
        )
    line = istream.readline() ## empty
    line = istream.readline()
    assert(line.lstrip().startswith('Component                      A priori sigma  Unit'))
    line = istream.readline()
    assert(line.lstrip().startswith('-----------------------------------------------------------------------'))
    for i in range(3):
        line = istream.readline()
        cols = line.split()
        assert('Translation Coordinates m'==' '.join([cols[1], cols[2], cols[4]]))
        dct[key][cols[0]] = float(cols[3])
    line = istream.readline()
    assert(len(line.strip())==0)
    """"
     Site-specific troposphere parameters:        used in NEQ-files:     1 to     1
     ------------------------------------

     A priori troposphere model:                  VMF, dry part only
     Meteo/Trop.delay values:                     Extrapolated

     Mapping function used for delay estimation:  Wet VMF
     Troposphere gradient estimation:             Chen/Herring
    """
    key = 'Site-specific troposphere parameters'.lower().replace(' ','_')
    dct[key] = {}
    num_of_nq = max_nq_index(dct)
    while line and not line.lstrip().startswith(
            'Site-specific troposphere parameters:'
    ):
        line = istream.readline()
    if not line.lstrip().startswith(
            'Site-specific troposphere parameters:'
    ):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Site-specific troposphere parameters:\''
        )
    mline = 'Site-specific troposphere parameters:        used in NEQ-files:     1 to{:6d}'.format(num_of_nq)
    if line.strip() != mline:
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file;\n\tExpected line \'{:}\'\n\tgot line     \'{:}\''.format(mline, line.strip())
        )
    line = istream.readline()
    assert(line.lstrip().startswith('------------------------------------'))
    line = istream.readline()
    while line and not line.lstrip().startswith(
            'Component'
    ):
        if len(line.strip()) > 0:
            cols = line.split(':')
            assert(len(cols)==2)
            dct[key][cols[0].strip().lower().replace(' ','_')] = cols[1].strip()
        line = istream.readline()
    """
     Component                      A priori sigma  Unit
     -----------------------------------------------------------------------------------------------------------------------------------
     U     absolute                     0.00000     m
     N     absolute                     0.00000     m
     E     absolute                     0.00000     m
     U     relative                     5.00000     m
     N     relative                     5.00000     m
     E     relative                     5.00000     m
    """
    assert(line.lstrip().startswith('Component                      A priori sigma  Unit'))
    line = istream.readline()
    assert(line.lstrip().startswith('-----------------------------------------------------------------------'))
    for i in range(6):
        line = istream.readline()
        cols = line.split()
        assert(len(cols)==4 and cols[3]=='m')
        dct[key]['_'.join([cols[0],cols[1]])] = float(cols[2])
    line = istream.readline()
    assert(len(line.strip())==0)

    ## all done
    return dct
