#! /usr/bin/python3
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
        nr_files += 1
        if val['file'] > max_idx:
            max_idx = val['file']
    assert (max_idx == nr_files)
    return max_idx


def station_name_to_index(dct, sta_name):
    # list_of_dct should be dct['stations'], aka
    # {"1":{"station_name": "FOO BAR", ...}, "2": {...} }
    for sta_num, sta_dct in dct.items():
        if sta_dct['station_name'] == sta_name:
            return sta_num
    return None


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
        for k, v in zip([
                'X_a_priori', 'Y_a_priori', 'Z_a_priori', 'Latitude_a_priori',
                'Longitude_a_priori', 'Height_a_priori'
        ], [float(c) for c in cols[2:]]):
            dct['stations'][sta_num][k] = v
        line = istream.readline()
    """ Note that the following block may be missing if we have no contraints !!
    """
    """
     Network constraints: 

     Component                      A priori sigma  Unit
     -----------------------------------------------------------------------------------------------------------------------------------
     DX    Translation  Coordinates     0.00001     m
     DY    Translation  Coordinates     0.00001     m
     DZ    Translation  Coordinates     0.00001     m
    """
    key = 'network_constraints'
    dct[key] = {}
    while line and not line.lstrip().startswith(
            'Network constraints:') and not line.lstrip().startswith(
                'Site-specific troposphere parameters:'):
        line = istream.readline()
    if line.lstrip().startswith('Network constraints:'):
        line = istream.readline()  ## empty
        line = istream.readline()
        assert (line.lstrip().startswith(
            'Component                      A priori sigma  Unit'))
        line = istream.readline()
        assert (line.lstrip().startswith(
            '-----------------------------------------------------------------------'
        ))
        for i in range(3):
            line = istream.readline()
            cols = line.split()
            assert ('Translation Coordinates m' == ' '.join(
                [cols[1], cols[2], cols[4]]))
            dct[key][cols[0]] = float(cols[3])
        line = istream.readline()
        assert (len(line.strip()) == 0)
    """"
     Site-specific troposphere parameters:        used in NEQ-files:     1 to     1
     ------------------------------------

     A priori troposphere model:                  VMF, dry part only
     Meteo/Trop.delay values:                     Extrapolated

     Mapping function used for delay estimation:  Wet VMF
     Troposphere gradient estimation:             Chen/Herring
    """
    key = 'Site-specific troposphere parameters'.lower().replace(' ', '_')
    dct[key] = {}
    num_of_nq = max_nq_index(dct)
    while line and not line.lstrip().startswith(
            'Site-specific troposphere parameters:'):
        line = istream.readline()
    if not line.lstrip().startswith('Site-specific troposphere parameters:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Site-specific troposphere parameters:\''
        )
    mline = 'Site-specific troposphere parameters:        used in NEQ-files:     1 to{:6d}'.format(
        num_of_nq)
    if line.strip() != mline:
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file;\n\tExpected line \'{:}\'\n\tgot line     \'{:}\''
            .format(mline, line.strip()))
    line = istream.readline()
    assert (line.lstrip().startswith('------------------------------------'))
    line = istream.readline()
    while line and not line.lstrip().startswith('Component'):
        if len(line.strip()) > 0:
            cols = line.split(':')
            assert (len(cols) == 2)
            dct[key][cols[0].strip().lower().replace(' ',
                                                     '_')] = cols[1].strip()
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
    assert (line.lstrip().startswith(
        'Component                      A priori sigma  Unit'))
    line = istream.readline()
    assert (line.lstrip().startswith(
        '-----------------------------------------------------------------------'
    ))
    for i in range(6):
        line = istream.readline()
        cols = line.split()
        assert (len(cols) == 4 and cols[3] == 'm')
        dct[key]['_'.join([cols[0], cols[1]])] = float(cols[2])
    line = istream.readline()
    assert (len(line.strip()) == 0)
    """
     SUMMARY OF RESULTS
     ------------------

     Number of parameters:
     --------------------

     Parameter type                               Adjusted   explicitly / implicitly (pre-eliminated)        Deleted     Singular
     -----------------------------------------------------------------------------------------------------------------------------------
     Station coordinates / velocities                  78           78            0                               0            0
     Site-specific troposphere parameters             718            0          718  (before stacking)            0           36
     -----------------------------------------------------------------------------------------------------------------------------------
     Previously pre-eliminated parameters            1240                      1240
     -----------------------------------------------------------------------------------------------------------------------------------
     Total number                                    2036           78         1958                               0           36
    """
    key = 'Number of parameters'.lower().replace(' ', '_')
    dct[key] = {}
    line = istream.readline()
    while line and not line.lstrip().startswith('SUMMARY OF RESULTS'):
        line = istream.readline()
    if not line.lstrip().startswith('SUMMARY OF RESULTS'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'SUMMARY OF RESULTS\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith('Number of parameters:'))
    line = istream.readline()
    assert (line.lstrip().startswith('--------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        'Parameter type                               Adjusted   explicitly / implicitly (pre-eliminated)        Deleted     Singular'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith('--------------------'))
    line = istream.readline()
    while line and len(line) > 45:
        if not line.lstrip().startswith('------------------'):
            description, adjusted, explicitely, implicitly, deleted, singular = [
                x.strip() for x in [
                    line[0:47], line[47:58], line[58:71], line[71:106],
                    line[106:118], line[118:]
                ]
            ]
            r = re.compile('([0-9]+)\s*\w*')
            g = re.match(r, implicitly)
            if not g:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to resolve line \'\''
                    .format(line.strip()))
            implicitly = g.groups(1)[0]
            dct[key][description.lower().replace(' ', '_')] = {}
            for tpl in zip(
                [adjusted, explicitely, implicitly, deleted, singular],
                ['adjusted', 'explicit', 'implicit', 'deleted', 'singular']):
                try:
                    value = int(tpl[0])
                    dct[key][description.lower().replace(' ',
                                                         '_')][tpl[1]] = value
                except ValueError as e:
                    pass
        line = istream.readline()
    """
     Statistics:                           
     ----------                            

     Total number of authentic observations      119303
     Total number of pseudo-observations            643

     Total number of explicit parameters            796
     Total number of implicit parameters           1240

     Total number of observations                119946
     Total number of adjusted parameters           2036
     Degree of freedom (DOF)                     117910

     A posteriori RMS of unit weight            0.00114 m
     Chi**2/DOF                                    1.30

     Total number of observation files               25
     Total number of stations                        26
     Total number of satellites                       0
    """
    key = 'Statistics'.lower().replace(' ', '_')
    dct[key] = {}
    line = istream.readline()
    while line and not line.lstrip().startswith('Statistics:'):
        line = istream.readline()
    if not line.lstrip().startswith('Statistics:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Statistics:\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('----------'))
    line = istream.readline()
    line = istream.readline()
    consecutive_empty_lines = 0
    while line and consecutive_empty_lines < 2:
        if len(line.strip()) == 0:
            consecutive_empty_lines += 1
        else:
            g = re.match(
                re.compile(
                    '^\s*((?:[A-Za-z0-9\*\/()-]+ )+)\s+([0-9]+(?:\.[0-9]*)?)\s*m?\s*$'
                ), line.strip())
            if not g:
                raise FileFormatError(
                    FILE_FORMAT, line,
                    '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to resolve \'Statistics:\' line {:}'
                    .format(line.strip()))
            dct[key][g.group(1).lower().strip().replace(' ', '_')] = float(
                g.group(2))
            consecutive_empty_lines = 0
        line = istream.readline()
    """
     Station coordinates and velocities:
     ----------------------------------

     Sol Station name         Typ Correction  Estimated value  RMS error   A priori value Unit    From                To                  MJD           Num Abb  
     ------------------------------------------------------------------------------------------------------------------------------------------------------------
       1 ANIK 12666M001         X   -0.00325    4729934.24399    0.00121    4729934.24724 meters  2021-03-04 00:00:00 2021-03-04 23:59:30 59277.49983     1 #CRD 
       1 ANIK 12666M001         Y   -0.00191    1938158.24215    0.00062    1938158.24406 meters  2021-03-04 00:00:00 2021-03-04 23:59:30 59277.49983     2 #CRD 
       1 ANIK 12666M001         Z   -0.00014    3801984.49604    0.00117    3801984.49618 meters  2021-03-04 00:00:00 2021-03-04 23:59:30 59277.49983     3 #CRD 
       1 ANKR 20805M002         X   -0.00109    4121948.39555    0.00141    4121948.39664 meters  2021-03-04 00:00:00 2021-03-04 23:59:30 59277.49983     4 #CRD 
       1 ANKR 20805M002         Y   -0.00560    2652187.84820    0.00093    2652187.85380 meters  2021-03-04 00:00:00 2021-03-04 23:59:30 59277.49983     5 #CRD 

        ... or ...

     Station coordinates and velocities:
     ----------------------------------

     Sol Station name         Typ Correction  Estimated value  RMS error   A priori value Unit    From                To                 
     ------------------------------------------------------------------------------------------------------------------------------------
       1 ANIK 12666M001         X   -0.00108    4729934.24616    0.00121    4729934.24724 meters  2021-03-04 00:00:00 2021-03-04 23:59:30
       1 ANIK 12666M001         Y   -0.00144    1938158.24262    0.00062    1938158.24406 meters  2021-03-04 00:00:00 2021-03-04 23:59:30
       1 ANIK 12666M001         Z   -0.00164    3801984.49454    0.00116    3801984.49618 meters  2021-03-04 00:00:00 2021-03-04 23:59:30
       1 ANKR 20805M002         X    0.00097    4121948.39761    0.00141    4121948.39664 meters  2021-03-04 00:00:00 2021-03-04 23:59:30
    """
    line = istream.readline()
    while line and not line.lstrip().startswith(
            'Station coordinates and velocities:'):
        line = istream.readline()
    if not line.lstrip().startswith('Station coordinates and velocities:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Station coordinates and velocities:\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('----------------------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        'Sol Station name         Typ Correction  Estimated value  RMS error   A priori value Unit    From                To                  MJD           Num Abb'
    ) or line.lstrip().startswith(
        'Sol Station name         Typ Correction  Estimated value  RMS error   A priori value Unit    From                To'
    ))
    if line.lstrip().startswith(
            'Sol Station name         Typ Correction  Estimated value  RMS error   A priori value Unit    From                To                  MJD           Num Abb'
    ):
        use_long_header = True
    else:
        use_long_header = False
    line = istream.readline()
    assert (line.lstrip().startswith('----------------------------------'))
    line = istream.readline()
    headers = 'Correction Estimated_value RMS_error Unit From To MJD Abb'.lower(
    ).split(
    ) if use_long_header else 'Correction Estimated_value RMS_error Unit From To'.lower(
    ).split()
    sta_idxs = []
    while line and len(line) > 115:
        if int(line.split()[0]) != 1:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] parse_gpsest_out Sol type is unknown! line: {:}'.
                format(line.strip()))
        station_name = line[5:25].strip()
        l = line[25:].split()
        assert ((use_long_header and (len(l) == 13 and l[-1] == '#CRD')) or
                ((not use_long_header) and (len(l) == 10)))
        station_idx = station_name_to_index(dct['stations'], station_name)
        if not station_idx:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] parse_gpsest_out Station found in \'A-Priori\' block but not in \'Station coordinates and velocities\''
                .format(line.strip()))
        ## verify a-priori value
        assert (dct['stations'][station_idx][l[0] + '_a_priori'] == float(l[4]))
        values = [
            float(l[1]),
            float(l[2]),
            float(l[3]),
            l[5],
            datetime.datetime.strptime(' '.join([l[6], l[7]]),
                                       '%Y-%m-%d %H:%M:%S'),
            datetime.datetime.strptime(' '.join([l[8], l[9]]),
                                       '%Y-%m-%d %H:%M:%S'),
            #float(l[10]), l[12]
        ]
        values += [float(l[10]), l[12]] if use_long_header else values
        tmp_dct = {}
        for tpl in zip(headers, values):
            tkey = '_'.join([l[0], tpl[0]])  ## eg. X_correction
            tmp_dct[tkey] = tpl[1]
        dct['stations'][station_idx] = merge_dicts(dct['stations'][station_idx],
                                                   tmp_dct)
        sta_idxs.append(
            station_idx) if station_idx not in sta_idxs else sta_idxs
        line = istream.readline()
    ## have we parsed all stations ?
    assert (sorted(list(dct['stations'].keys())) == sorted(sta_idxs))
    """
     Station coordinates and velocities:
     ----------------------------------
     Reference epoch: 2021-03-04 12:00:00

     Station name          Typ   A priori value  Estimated value    Correction     RMS error      3-D ellipsoid        2-D ellipse
     ------------------------------------------------------------------------------------------------------------------------------------
     ANIK 12666M001        X      4729934.24724    4729934.24399      -0.00325       0.00121
                           Y      1938158.24406    1938158.24215      -0.00191       0.00062
                           Z      3801984.49618    3801984.49604      -0.00014       0.00117

                           U           47.75303         47.74996      -0.00307       0.00168     0.00169    4.8
                           N         36.8260208       36.8260208       0.00213       0.00047     0.00041   77.0     0.00041   79.7
                           E         22.2820675       22.2820675      -0.00053       0.00041     0.00045   -0.6     0.00047

     ANKR 20805M002        X      4121948.39664    4121948.39555      -0.00109       0.00141
    """
    line = istream.readline()
    while line and not line.lstrip().startswith(
            'Station coordinates and velocities:'):
        line = istream.readline()
    if not line.lstrip().startswith('Station coordinates and velocities:'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'Station coordinates and velocities:\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('----------------------------------'))
    line = istream.readline()
    assert (line.lstrip().startswith('Reference epoch:'))
    dct['Reference epoch'.lower().replace(
        ' ',
        '_')] = datetime.datetime.strptime(line[line.index(':') + 1:].strip(),
                                           '%Y-%m-%d %H:%M:%S')
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        'Station name          Typ   A priori value  Estimated value    Correction     RMS error      3-D ellipsoid        2-D ellipse'
    ))
    line = istream.readline()
    assert (line.lstrip().startswith('----------------------------------'))
    line = istream.readline()
    sta_idxs = []
    while line and len(line.strip()) > 80:
        tmp_dct = {}
        station_idx = station_name_to_index(dct['stations'], line[0:20].strip())
        station_dct = dct['stations'][station_idx]
        l = line[20:].split()
        assert (l[0] == 'X' and station_dct['X_a_priori'] == float(l[1]) and
                station_dct['X_estimated_value'] == float(l[2]) and
                station_dct['X_correction'] == float(l[3]) and
                station_dct['X_rms_error'] == float(l[4]))
        l = istream.readline()[20:].split()
        assert (l[0] == 'Y' and station_dct['Y_a_priori'] == float(l[1]) and
                station_dct['Y_estimated_value'] == float(l[2]) and
                station_dct['Y_correction'] == float(l[3]) and
                station_dct['Y_rms_error'] == float(l[4]))
        l = istream.readline()[20:].split()
        assert (l[0] == 'Z' and station_dct['Z_a_priori'] == float(l[1]) and
                station_dct['Z_estimated_value'] == float(l[2]) and
                station_dct['Z_correction'] == float(l[3]) and
                station_dct['Z_rms_error'] == float(l[4]))
        line = istream.readline()  ## empty line
        l = istream.readline()[20:].split()
        assert (l[0] == 'U' and station_dct['Height_a_priori'] == float(l[1]))
        for tpl in zip(
            ['Height_estimated_value', 'Height_correction', 'Height_rms_error'],
            [2, 3, 4]):
            tmp_dct[tpl[0]] = float(l[tpl[1]])
        l = istream.readline()[20:].split()
        assert (l[0] == 'N' and station_dct['Latitude_a_priori'] == float(l[1]))
        for tpl in zip([
                'Latitude_estimated_value', 'Latitude_correction',
                'Latitude_rms_error'
        ], [2, 3, 4]):
            tmp_dct[tpl[0]] = float(l[tpl[1]])
        l = istream.readline()[20:].split()
        assert (l[0] == 'E' and
                station_dct['Longitude_a_priori'] == float(l[1]))
        for tpl in zip([
                'Longitude_estimated_value', 'Longitude_correction',
                'Longitude_rms_error'
        ], [2, 3, 4]):
            tmp_dct[tpl[0]] = float(l[tpl[1]])
        dct['stations'][station_idx] = merge_dicts(dct['stations'][station_idx],
                                                   tmp_dct)
        sta_idxs.append(
            station_idx) if station_idx not in sta_idxs else sta_idxs
        line = istream.readline()
        assert (not len(line.strip()))
        line = istream.readline()
    ## have we parsed all stations ?
    assert (sorted(list(dct['stations'].keys())) == sorted(sta_idxs))

    ## all done
    return dct
