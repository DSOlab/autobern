#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
from pybern.products.gnssdates.gnssdates import pydt2gps, sow2dow
from pybern.products.downloaders.retrieve import web_retrieve
from pybern.products.errors.errors import ArgumentError
from sys import version_info as version_info
if version_info.major == 2:
    from produtils import utils_whatever2pydt as _date
    from produtils import utils_pydt2yydoy as pydt2yydoy
else:
    from .produtils import utils_whatever2pydt as _date
    from .produtils import utils_pydt2yydoy as pydt2yydoy

CODE_URL = 'ftp://ftp.aiub.unibe.ch'
CODE_AC = 'COD'
FTP_TXT = 'http://ftp.aiub.unibe.ch/AIUB_AFTP.TXT'


def get_ion_final_target(**kwargs):
    """ Final ionosphere information in IONEX or Bernese format from COD

      kwargs that matter:
      format='ionex' or format='inx' to get the IONEX format.
      format='ion' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      type='final' Optional but if given must be 'final'
      To provide a date, use either:
        * pydt=datetime.datetime(...) or
        * year=... and doy=...

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod

      kwargs  |format=ionex                 | format=bernese               |
      --------+-----------------------------+------------------------------+
      acid=coe|BSWUSER52/ATM/yyyy/COEyyddd.INX.Z| BSWUSER52/ATM/yyyy/COEyyddd.ION.Z|
      acid=cod|CODE/yyyy/CODGddd0.yyI.Z     | CODE/yyyy/CODwwwwd.ION.Z     |

      type=final (from week 2238)
      ---------------+-----------------------------+------------------------+
      acid=cod       |CODE/yyyy/                                            |
      format=ionex   |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.INX.gz   |
      format=bernese |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.ION.gz   |
      ---------------+-----------------------------+------------------------+
  """
    if 'format' in kwargs and kwargs['format'] not in [
            'ionex', 'inx', 'ion', 'bernese'
    ]:
        raise ArgumentError('[ERROR] code::get_ion_final Invalid format',
                            'format', **kwargs)
    if 'acid' in kwargs and kwargs['acid'] not in ['cod', 'coe']:
        raise ArgumentError('[ERROR] code::get_ion_final Invalid acid', 'acid',
                            **kwargs)
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise ArgumentError('[ERROR] code::get_ion_final Invalid type', 'type',
                            **kwargs)

    if 'format' not in kwargs:
        kwargs['format'] = 'bernese'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    pydt = _date(**kwargs)  ## this may throw
    yy, ddd = pydt2yydoy(pydt)
    week, sow = pydt2gps(pydt)
    if kwargs['format'] in ['bernese', 'ion']:
        frmt = 'ION'
    else:
        if kwargs['acid'] == 'coe':
            frmt = 'INX'
        else:
            frmt = '{:02d}I'.format(yy)

    if kwargs['acid'] == 'coe':
        url_dir = 'BSWUSER52/ATM/{:}'.format(pydt.strftime("%Y"))
        acn = 'COE'
        sdate = '{:02d}{:03d}'.format(yy, ddd)
    else:
        url_dir = 'CODE/{:}'.format(pydt.strftime("%Y"))
        if kwargs['format'] in ['bernese', 'ion']:
            acn = 'COD'
            if week <= 2237:
                sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))
                ion = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)
            else:
                sdate = '{:}{:}'.format(pydt.strftime('%Y'), pydt.strftime('%j'))
                ion = '{:}0OPSFIN_{:}0000_01D_01H_GIM.{:}.gz'.format(acn, sdate, frmt)
        else:
            acn = 'CODG'
            sdate = '{:03d}0'.format(ddd)
            ion = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)

    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, ion)
    return target


def get_ion_rapid_target(**kwargs):
    """ Rapid or Ultra-rapid ionosphere information in IONEX or Bernese format
      from COD

      CORGddd0.yyI.Z    CODE rapid ionosphere product, IONEX format
      COPGddd0.yyI.Z    CODE 1-day or 2-day ionosphere predictions,
                        in IONEX format
      CODwwwwd.ION_R    CODE rapid ionosphere product, Bernese format
      CODwwwwd.ION_P    CODE 1-day ionosphere predictions, Bernese format
      CODwwwwd.ION_P2   CODE 2-day ionosphere predictions, Bernese format
      CODwwwwd.ION_P5   CODE 5-day ionosphere predictions, Bernese format
      COD.ION_U         Last update of CODE rapid ionosphere product
                        (1 day) complemented with ionosphere predictions
                        (2 days)

      kwargs that matter:
      format='ionex' or format='inx' to get the IONEX format.
      format='ion' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      To provide a date, use either:
        * pydt=datetime.datetime(...) or
        * year=... and doy=...

      Default Values
      kwargs['format'] = 'bernese'
      kwargs['type'] = 'rapid'

      aka:
      kwargs         |format=ionex        | format=bernese      |
      ---------------+--------------------+---------------------+
      type=rapid     |CODE/CORGddd0.yyI.Z | CODE/CODwwwwd.ION_R |
      type=prediction|CODE/COPGddd0.yyI.Z | CODE/CODwwwwd.ION_P |
      type=current or|                    | CODE/COD.ION_U      |
      urapid or      |                    |
      ultra-rapid    |                    |
      type=p2        |                    | CODE/CODwwwwd.ION_P2|
      type=p5        |                    | CODE/CODwwwwd.ION_P5|

      TODO current should be an alias for urapid or ultra-rapid
  """
    if 'format' in kwargs and kwargs['format'] not in [
            'ionex', 'inx', 'ion', 'bernese'
    ]:
        raise ArgumentError('[ERROR] code::get_ion_rapid Invalid format',
                            'format', **kwargs)
    if 'type' in kwargs and kwargs['type'] not in [
            'rapid', 'prediction', 'current', 'p2', 'p5', 'urapid',
            'ultra-rapid'
    ]:
        raise ArgumentError('[ERROR] code::get_ion_rapid Invalid type', 'type',
                            **kwargs)

    if 'format' not in kwargs:
        kwargs['format'] = 'bernese'
    if 'type' in kwargs and kwargs['type'] in ['urapid', 'ultra-rapid']:
        kwargs['type'] = 'current'
    if 'type' not in kwargs:
        kwargs['type'] = 'rapid'

    if kwargs['type'] != 'current':
        pydt = _date(**kwargs)  ## this may throw
        yy, ddd = pydt2yydoy(pydt)

    if kwargs['format'] in ['ionex', 'inx']:
        sdate = '{:03d}0'.format(ddd)
        frmt = '{:}I.Z'.format(pydt.strftime("%y"))
        if 'type' in kwargs and kwargs['type'] == 'rapid':
            acn = 'CORG'
        elif 'type' in kwargs and kwargs['type'] == 'prediction':
            acn = 'COPG'
        else:
            raise RuntimeError(
                '[ERROR] code::get_ion_rapid invalid request (#1)')

    if kwargs['format'] in ['bernese', 'ion']:
        acn = 'COD'
        if kwargs['type'] == 'current':
            frmt = 'ION_U'
            sdate = ''
        else:
            week, sow = pydt2gps(pydt)
            sdate = '{:04d}{:1d}'.format(week, sow2dow(sow))
            if kwargs['type'] == 'rapid':
                frmt = 'ION_R'
            elif kwargs['type'] == 'prediction':
                frmt = 'ION_P'
            elif kwargs['type'] == 'p2':
                frmt = 'ION_P2'
            elif kwargs['type'] == 'p5':
                frmt = 'ION_P5'
            else:
                raise RuntimeError(
                    '[ERROR] code::get_ion_rapid invalid request (#2)')

    ion = '{:}{:}.{:}'.format(acn, sdate, frmt)
    target = '{:}/CODE/{:}'.format(CODE_URL, ion)
    return target


def get_ion(**kwargs):
    """
      kwargs that matter:
      format='ionex' or format='inx' to get the IONEX format.
      format='ion' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      type='final', rapid, prediction, current, p2, p5 (see Table 2)
      save_as: '/some/path/foo.ION' Rename downloaded file to this filename
      save_dir: 'foo/bar' Directory to save remote file; if both save_dir and
          save_as are given, then the local file will be the concatenation
          of these two, aka os.path.join(save_dir, save_as)
      To provide a date, use either:
        * pydt=datetime.datetime(...) or
        * year=... and doy=...

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod
      kwargs['type'] = final

      type=final
      kwargs  |format=ionex                 | format=bernese               |
      --------+-----------------------------+------------------------------+
      acid=coe|BSWUSER52/yyyy/COEyyddd.INX.Z| BSWUSER52/yyyy/COEyyddd.ION.Z|
      acid=cod|CODE/yyyy/CODGddd0.yyI.Z     | CODE/yyyy/CODwwwwd.ION.Z     |

      type=final (from week 2238)
      ---------------+-----------------------------+------------------------+
      acid=cod       |CODE/yyyy/                                            |
      format=ionex   |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.INX.gz   |
      format=bernese |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.ION.gz   |
      ---------------+-----------------------------+------------------------+

      kwargs         |format=ionex        | format=bernese      |
      ---------------+--------------------+---------------------+
      type=rapid     |CODE/CORGddd0.yyI.Z | CODE/CODwwwwd.ION_R |
      type=prediction|CODE/COPGddd0.yyI.Z | CODE/CODwwwwd.ION_P |
      type=current(*)|                    | CODE/COD.ION_U      |
      type=p2        |                    | CODE/CODwwwwd.ION_P2|
      type=p5        |                    | CODE/CODwwwwd.ION_P5|

      (*) current is an alias for 'urapid' and 'ultra-rapid'; any of those three
      strings describes the same type
  """
    if 'type' in kwargs and kwargs['type'] in [
            'rapid', 'prediction', 'current', 'p2', 'p5'
    ]:
        target = get_ion_rapid_target(**kwargs)
    elif 'type' not in kwargs or 'type' in kwargs and kwargs['type'] == 'final':
        target = get_ion_final_target(**kwargs)

    indct = {}
    ## Rename LONG NAME to old names
    ##+not e pemanent solution check again
    pydt = _date(**kwargs)  ## this may throw
    week, sow = pydt2gps(pydt)

    if 'save_as' in kwargs:
        indct['save_as'] = kwargs['save_as']
    elif week >= 2238 and kwargs['type'] == 'final':
        sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))
        frmt = 'ION'
        indct['save_as'] = 'COD{:}.{:}.Z'.format(sdate, frmt)
    if 'save_dir' in kwargs:
        indct['save_dir'] = kwargs['save_dir']

    #print(">> Note rtying to download target ION file: {:}".format(target))
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local


def list_products():
    print(
        """ Information on Ionospheric (and other) products available via CODE's
  ftp site can be found at: {:}. Here is a table of products that can be
  downloaded via this script:\n

  _Available files in FTP____________________________________________________
  COEyyddd.INX.Z    Ionosphere information in IONEX format from EUREF solution
  COEyyddd.ION.Z    Ionosphere information in Bernese format from EUREF solution
  CORGddd0.yyI.Z    CODE rapid ionosphere product, IONEX format
  COPGddd0.yyI.Z    CODE 1-day or 2-day ionosphere predictions,
                    in IONEX format
  CODwwwwd.ION_R    CODE rapid ionosphere product, Bernese format
  CODwwwwd.ION_P    CODE 1-day ionosphere predictions, Bernese format
  CODwwwwd.ION_P2   CODE 2-day ionosphere predictions, Bernese format
  CODwwwwd.ION_P5   CODE 5-day ionosphere predictions, Bernese format
  COD.ION_U         Last update of CODE rapid ionosphere product
                    (1 day) complemented with ionosphere predictions
                    (2 days)

  _Arguments for Products____________________________________________________
  type=final
  kwargs         |format=ionex                 | format=bernese               |
  ---------------+-----------------------------+------------------------------+
  acid=coe       |BSWUSER52/yyyy/COEyyddd.INX.Z| BSWUSER52/yyyy/COEyyddd.ION.Z|
  acid=cod       |CODE/yyyy/CODGddd0.yyI.Z     | CODE/yyyy/CODwwwwd.ION.Z     |
  ---------------+-----------------------------+------------------------------+
  type=final (from week 2238)
  ---------------+-----------------------------+------------------------------+
  acid=cod       |CODE/yyyy/                                                  |
  format=ionex   |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.INX.gz         |
  format=bernese |          COD0OPSFIN_yyyyddd0000_01D_01H_GIM.ION.gz         |
  ---------------+-----------------------------+------------------------------+
  kwargs         |format=ionex                 | format=bernese               |
  ---------------+-----------------------------+------------------------------+
  type=rapid     |CODE/CORGddd0.yyI.Z          | CODE/CODwwwwd.ION_R          |
  type=prediction|CODE/COPGddd0.yyI.Z          | CODE/CODwwwwd.ION_P          |
  type=urapid (*)|                             | CODE/COD.ION_U               |
  type=p2        |                             | CODE/CODwwwwd.ION_P2         |
  type=p5        |                             | CODE/CODwwwwd.ION_P5         |

  (for non-final products, EUREF solutions, aka acid=coe, not available)
  (*) 'urapid' can be used interchangably with 'current' and 'ultra-rapid'

  """.format(FTP_TXT))
    return
