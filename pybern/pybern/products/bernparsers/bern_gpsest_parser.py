#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
from pybern.products.errors.errors import FileFormatError

FILE_FORMAT = 'GPSEST .OUT (Bernese v5.2)'


def parse_observation_files(istream, campaign_name, idx=1):
    search_str = '{:d}. OBSERVATION FILES'.format(idx)
    dct = {}
    line = istream.readline()
    file_index_list = []
    tmp_index_list = []
    """
     2. OBSERVATION FILES
     --------------------

     -----------------------------------------------------------------------------------------------------------------------------------
     GREECE          
     -----------------------------------------------------------------------------------------------------------------------------------

     MAIN CHARACTERISTICS:
     --------------------
     
     FILE  OBSERVATION FILE HEADER          OBSERVATION FILE                  SESS     RECEIVER 1            RECEIVER 2
     -----------------------------------------------------------------------------------------------------------------------------------

        1  ${P}/GREECE/OBS/A1PK0630.PSH     ${P}/GREECE/OBS/A1PK0630.PSO      0630     TPS NET-G5            LEICA GR25          
        2  ${P}/GREECE/OBS/A1PY0630.PSH     ${P}/GREECE/OBS/A1PY0630.PSO      0630     TPS NET-G5            LEICA GR10          
        3  ${P}/GREECE/OBS/A8PK0630.PSH     ${P}/GREECE/OBS/A8PK0630.PSO      0630     LEICA GR25            LEICA GR25          
        4  ${P}/GREECE/OBS/A8TU0630.PSH     ${P}/GREECE/OBS/A8TU0630.PSO      0630     LEICA GR25            LEICA GRX1200+GNSS  
        5  ${P}/GREECE/OBS/AAEG0630.PSH     ${P}/GREECE/OBS/AAEG0630.PSO      0630     TPS NET-G3A           TPS NET-G5          
        6  ${P}/GREECE/OBS/AALA0630.PSH     ${P}/GREECE/OBS/AALA0630.PSO      0630     TPS NET-G3A           LEICA GRX1200+GNSS  
     
                                                                                                           AMB.I.+S.      #CLUSTERS
     FILE TYP FREQ.  STATION 1        STATION 2        SESS  FIRST OBSERV.TIME  #EPO  DT #EF #CLK ARC #SAT  W 12    #AMB  L1  L2  L5  RM
     -----------------------------------------------------------------------------------------------------------------------------------

        1  P  L3     ANIK 12666M001   PTKG 12664M001   0630  21-03-04  0:00:00  2880  30   0  E E  1   51   N  Y  N  149  78  78  45   0
        2  P  L3     ANIK 12666M001   PYLO 12637M001   0630  21-03-04  0:00:00  2880  30   0  E E  1   51   N  Y  N  150  70  70  45   0
        3  P  L3     ANKY 18594M001   PTKG 12664M001   0630  21-03-04  0:00:00  2880  30   0  E E  1   51   N  Y  N  138  67  67  49   0
        4  P  L3     ANKY 18594M001   TUC2 12617M003   0630  21-03-04  0:00:00  2880  30   0  E E  1   51   N  Y  N  172  72  72  49   0
        5  P  L3     ATAL 12630M001   EGIO 12658M001   0630  21-03-04  0:00:00  2880  30   0  E E  1   53   N  Y  N  109  34  34  16   0
        6  P  L3     ATAL 12630M001   LARM 12610M002   0630  21-03-04 18:40:00   639  30   0  E E  1   35   N  Y  N   38  34  34  30   0

     SATELLITES:
     ----------
     
     FILE  #SAT  SATELLITES
     -----------------------------------------------------------------------------------------------------------------------------------

        1   51     1   2   3   4   5   6   7   8   9  10  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
                  32 101 102 103 104 105 107 108 109 112 113 114 115 116 117 118 119 120 121 122 124
        2   51     1   2   3   4   5   6   7   8   9  10  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
                  32 101 102 103 104 105 107 108 109 112 113 114 115 116 117 118 119 120 121 122 124
        3   51     1   2   3   4   5   6   7   8   9  10  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
                  32 101 102 103 104 105 107 108 109 112 113 114 115 116 117 118 119 120 121 122 124
        4   51     1   2   3   4   5   6   7   8   9  10  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
                  32 101 102 103 104 105 107 108 109 112 113 114 115 116 117 118 119 120 121 122 124
        5   53     1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30
                  31  32 101 102 103 104 105 107 108 109 111 112 113 114 115 116 117 118 119 120 121 122 124
        6   35     1   3   4   8  10  14  15  16  17  18  20  21  22  23  26  27  28  29  31  32 101 102 103 104 107 108 112 113 114 115
                 116 117 118 119 124


     OBSERVATION SELECTION:
     ---------------------

     SAMPLING RATE FOR OBSERVATIONS                :  180 SEC
     SAMPLING RATE TO RESUBSTITUTE EPOCH PARAMETERS:    0 SEC
     SAMPLING RATE TO PREELIMINATE EPOCH PARAMETERS:    0 SEC
     ELEVATION CUT-OFF ANGLE                       :    3 DEG (STATIONS)     0 DEG (LEOS)
     SATELLITE SYSTEM                              :  GPS/GLO
     SPECIAL DATA SELECTION                        :  NO

    """
    while line and not line.lstrip().startswith(search_str):
        line = istream.readline()
    if not line.lstrip().startswith(search_str):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'{:}\''
            .format(search_str))
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()
    assert (line.lstrip().startswith(campaign_name))
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith('MAIN CHARACTERISTICS:'))
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith(
        'FILE  OBSERVATION FILE HEADER          OBSERVATION FILE                  SESS     RECEIVER 1            RECEIVER 2'
    ))
    assert (['O', 'O', 'S', 'R',
             'R'] == [line[x] for x in [7, 40, 74, 83, 105]])
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    while len(line) > 106 and not line.lstrip().startswith('AMB.'):
        file_index = int(line[0:7])
        dct[file_index] = {}
        dct[file_index]['observation_file_header'] = line[7:40].strip()
        dct[file_index]['observation_file'] = line[40:74].strip()
        dct[file_index]['sess'] = line[74:83].strip()
        dct[file_index]['receiver_1'] = line[83:105].strip()
        dct[file_index]['receiver_2'] = line[105:].strip()
        file_index_list.append(file_index)
        line = istream.readline()
    if not line.lstrip().startswith('AMB.I.+S.      #CLUSTERS'):
        while line and not line.lstrip().startswith('AMB.I.+S.      #CLUSTERS'):
            line = istream.readline()
    assert (line.lstrip().startswith('AMB.I.+S.      #CLUSTERS'))
    line = istream.readline()
    assert (line.lstrip().startswith(
        'FILE TYP FREQ.  STATION 1        STATION 2        SESS  FIRST OBSERV.TIME  #EPO  DT #EF #CLK ARC #SAT  W 12    #AMB  L1  L2  L5  RM'
    ))
    assert ([
        'T', 'F', 'S', 'S', 'S', 'F', '#', 'D', '#', '#', 'A', '#', 'W', '1',
        '#', 'L', 'L', 'L'
    ] == [
        line[x] for x in [
            6, 10, 17, 34, 51, 57, 76, 82, 85, 89, 94, 98, 104, 106, 112, 118,
            122, 126
        ]
    ])
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    tmp_index_list = []
    while len(line) >= 120:
        file_index = int(line[0:6])
        if file_index not in dct:
            raise FileFormatError(
                FILE_FORMAT, line,
                '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; File index \'{:}\' does not match (#2)'
                .format(file_index))
        assert (file_index in dct)
        dct[file_index]['typ'] = line[6:10].strip()
        dct[file_index]['freq'] = line[10:17].strip()
        dct[file_index]['station_1'] = line[17:34].strip()
        dct[file_index]['station_2'] = line[34:51].strip()
        assert (dct[file_index]['sess'] == line[51:57].strip())
        dct[file_index]['first_obs'] = datetime.datetime.strptime(
            ' '.join(line[57:76].strip().split()), '%y-%m-%d %H:%M:%S')

        dct[file_index]['epo'] = int(line[76 - 1:82].strip())
        dct[file_index]['dt'] = int(line[82 - 1:85].strip())
        dct[file_index]['ef'] = int(line[85:89].strip())
        dct[file_index]['clk'] = line[89:94].strip()
        dct[file_index]['arc'] = int(line[94:98].strip())
        dct[file_index]['sat'] = int(line[98:104].strip())
        dct[file_index]['amb'] = int(line[112-1:117].strip())
        dct[file_index]['l1'], dct[file_index]['l2'], dct[file_index][
            'l5'], dct[file_index]['rm'] = [int(x) for x in line[118 - 1:].split()]
        ## some further checks ....
        ## This whole mess happens for two reasons:
        ## 1. First, we do not parse values for 'AMB.I.+S.' cause i don't know 
        ##    what that is.
        ## 2. Second, the value in the '#CLK' column can contain whitespace 
        ##    characters; actually, it is usually something like 'E E'.
        assert([val.replace('_',' ') for val in ' '.join([line[75:90],line[90:94].strip().replace(' ','_'),line[94:104],line[112:]]).split()] == [ str(dct[file_index][key]) for key in ['epo', 'dt', 'ef', 'clk', 'arc', 'sat', 'amb', 'l1', 'l2', 'l5', 'rm'] ])
        tmp_index_list.append(file_index)
        line = istream.readline()
    ## should have parsed all file indexes ....
    if file_index_list != tmp_index_list:
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; File index mismatch (#2)'
            .format(file_index))
    line = istream.readline()
    if not line.lstrip().startswith('SATELLITES:'):
        while line and not line.lstrip().startswith('SATELLITES:'):
            line = istream.readline()
    assert (line.lstrip().startswith('SATELLITES:'))
    line = istream.readline()
    assert (line.lstrip().startswith('----------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith('FILE  #SAT  SATELLITES'))
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    cur_file_idx = -1
    tmp_index_list = []
    while len(line)>15:
        if line[0:13].strip() != '':
            cur_file_idx, num_sats = [int(x) for x in line[0:13].split()]
            dct[cur_file_idx]['sats'] = [int(sv) for sv in line[13:].split()]
            tmp_index_list.append(cur_file_idx)
        else:
            dct[cur_file_idx]['sats'] += [int(sv) for sv in line[13:].split()]
        line = istream.readline()
    ## should have parsed all file indexes ....
    if file_index_list != tmp_index_list:
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; File index mismatch (#3)'
            .format(file_index))
    if not line.lstrip().startswith('OBSERVATION SELECTION:'):
        while line and not line.lstrip().startswith('OBSERVATION SELECTION:'):
            line = istream.readline()
    assert (line.lstrip().startswith('OBSERVATION SELECTION:'))
    line = istream.readline()
    assert (line.lstrip().startswith('----------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    dct['observation_selection'] = {}
    while len(line)>50 and line.find(':')>0:
        cols = [ x.strip() for x in line.split(':')]
        assert(len(cols)==2)
        dct['observation_selection'][cols[0].replace(' ','_').lower()] = cols[1]
        line = istream.readline()
    return dct


def parse_campaigns(istream, idx=1):
    search_str = '{:d}. CAMPAIGNS'.format(idx)
    dct = {}
    line = istream.readline()
    """
     1. CAMPAIGNS
     ------------
     
     CAMPAIGN NAME      NUM STATION NAME       NUM STATION NAME       NUM STATION NAME       NUM STATION NAME       NUM STATION NAME
     -----------------------------------------------------------------------------------------------------------------------------------

     GREECE          :   40 ANIK 12666M001     429 PTKG 12664M001     434 PYLO 12637M001      42 ANKY 18594M001     541 TUC2 12617M003  
                         54 ATAL 12630M001     164 EGIO 12658M001     289 LARM 12610M002     367 NOA1 12620M001      41 ANKR 20805M002  
                        424 PRKV 12636M001      58 AUT1 12619M002     161 DUTH 12621M001     405 PENC 11206M006      79 BOR1 12205M002  
                        538 TRO1 10302M006     453 RLSO 12629M001     189 GLSV 12356M001     413 POLV 12336M001     214 HERS 13212M007  
                        609 ZIMM 14001M004     229 IDI0 12667M001     267 KLOK 12632M001     415 PONT 12626M001     483 SPAN 12628M001  
                        581 VLSM 12625M001  
    """
    while line and not line.lstrip().startswith(search_str):
        line = istream.readline()
    if not line.lstrip().startswith(search_str):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'{:}\''
            .format(search_str))
    line = istream.readline()
    assert (line.lstrip().startswith('------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()
    assert (line.lstrip().startswith('CAMPAIGN NAME'))
    ## how many columns? (aka NUM STATION NAME)
    cols = line.lstrip().count('NUM', len('CAMPAIGN NAME'))
    assert (cols == line.lstrip().count('STATION', len('CAMPAIGN NAME')))
    assert (cols == line.lstrip().count('NAME', len('CAMPAIGN NAME')))
    line = istream.readline()
    assert (line.lstrip().startswith('-----------------------------------'))
    line = istream.readline()  ## empty line
    line = istream.readline()  ## first record line
    dct['campaign'] = line.split(':')[0].strip()
    start_idx = line.find(':') + 1
    while len(line) >= start_idx:
        info = [
            line[start_idx + i * 23:23 + start_idx + i * 23]
            for i in range(cols)
            if len(line) > start_idx + i * 23 + 22
        ]
        tpls = [(int(x.split()[0]), ' '.join(x.split()[1:])) for x in info]
        for t in tpls:
            dct[t[1]] = t[0]
        line = istream.readline()
    return dct


## header must have been parsed already
def parse_gpsest_out(istream):
    dct = {}
    line = istream.readline()
    """
     TABLE OF CONTENTS
     -----------------
     
      1. CAMPAIGNS
      2. OBSERVATION FILES
      3. GENERAL OPTIONS
      4. STATIONS
      5. SATELLITE ORBITS
      6. ATMOSPHERE
      7. CLOCK PARAMETERS
      8. POLE COORDINATES AND TIME INFORMATION
      9. ANTENNA PHASE CENTERS
     10. CONSTANTS
     11. PARAMETER CHARACTERIZATION LIST
     12. TEST OUTPUT
     13. RESULTS (PART 1)
     14. RESULTS (PART 2)
    """
    while not line.lstrip().startswith('TABLE OF CONTENTS'):
        line = istream.readline()
    if not line.lstrip().startswith('TABLE OF CONTENTS'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'TABLE OF CONTENTS\''
        )
    line = istream.readline()
    assert (line.lstrip().startswith('-----------------'))
    line = istream.readline()  ## empty line
    dct['table_of_contents'] = {}
    line = istream.readline()
    while len(line) > 5 and len(line.split('.')) >= 2:
        l = line.split('.')
        idx, name = int(l[0]), '_'.join(l[1:]).strip().replace(' ', '_').lower()
        dct['table_of_contents'][name] = idx
        line = istream.readline()
    """
     INPUT AND OUTPUT FILENAMES
     --------------------------

     -----------------------------------------------------------------------------------------------------------------------------------
     General constants               : ${X}/GEN/CONST.
     Geodetic datum                  : ${X}/GEN/DATUM.
     Difference GPS-UTC              : ${X}/GEN/GPSUTC.
     Earth potential coefficients    : ${X}/GEN/EGM2008_SMALL.
     Satellite problems              : ${X}/GEN/SAT_2021.CRX
     Satellite information           : ${X}/GEN/SATELLIT.I14
     Phase center eccentricities     : ${X}/GEN/PCV_EPN.I14
     Receiver antenna orientation    :  ---
    """
    while not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        line = istream.readline()
    if not line.lstrip().startswith('INPUT AND OUTPUT FILENAMES'):
        raise FileFormatError(
            FILE_FORMAT, line,
            '[ERROR] parse_gpsest_out  Invalid BERNESE GPSEST file; Filed to find \'INPUT AND OUTPUT FILENAMES\''
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
    ## parse CAMPAIGNS if in contents
    if 'campaigns' in dct['table_of_contents']:
        chapter = dct['table_of_contents']['campaigns']
        dct['campaigns'] = parse_campaigns(istream, chapter)
    ## parse OBSERVATION FILES if in contents
    if 'observation_files' in dct['table_of_contents']:
        chapter = dct['table_of_contents']['observation_files']
        dct['observation_files'] = parse_observation_files(
            istream, dct['campaigns']['campaign'], chapter)
    return dct
