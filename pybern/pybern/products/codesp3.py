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


def get_sp3_final_target(**kwargs):
    """ Final Orbit information in SP3 format from COD

      CODwwwwd.EPH.Z    CODE final GNSS orbits
      COXwwwwd.EPH.Z    CODE final GLONASS orbits (for GPS weeks
                        0990 to 1066)

      kwargs that matter:
      format='sp3' Optional but if given it must be sp3
      type='final' Optional but if given must be 'final'
      acid='cod' to get the GNSS solution, 'cox' to get GLONASS only solution.
        The latter (cox) are only available within the interval for GPS weeks
        0990 to 1066
      To provide a date, use either:
        * pydt=datetime.datetime(...) or 
        * year=... and doy=...

      Default values:
      kwargs['format'] = sp3
      kwargs['acid'] = cod
      kwargs['type'] = final

  """
    if 'format' in kwargs and kwargs['format'] not in ['sp3']:
        raise ArgumentError('[ERROR] code::get_sp3_final Invalid format',
                            'format', **kwargs)
    if 'acid' in kwargs and kwargs['acid'] not in ['cod', 'cox']:
        raise ArgumentError('[ERROR] code::get_sp3_final Invalid acid', 'acid',
                            **kwargs)
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise ArgumentError('[ERROR] code::get_sp3_final Invalid type', 'type',
                            **kwargs)

    if 'format' not in kwargs:
        kwargs['format'] = 'sp3'
    if 'type' not in kwargs:
        kwargs['type'] = 'final'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    pydt = _date(**kwargs)  ## this may throw
    week, sow = pydt2gps(pydt)
    acn = 'COD' if kwargs['acid'] == 'cod' else 'COX'
    sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))
    frmt = 'EPH'
    url_dir = '{:}'.format(pydt.strftime('%Y'))

    eph = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, ion)
    return target


def get_sp3_rapid_target(**kwargs):
    """ Rapid or Ultra-rapid orbit information in SP3 format from COD

      kwargs that matter:
      format='sp3' Optional but if given it must be sp3
      type='frapid' Cn be any of current, current-5d, .... (see Table below)
      acid='cod' Optional but if given it must be 'cod'
      To provide a date, use either:
        * pydt=datetime.datetime(...) or 
        * year=... and doy=...

      Default values:
      kwargs['format'] = sp3
      kwargs['acid'] = cod
      kwargs['type'] = frapid

      COD.EPH_U         CODE ultra-rapid GNSS orbits
      COD.EPH_5D        Last update of CODE 5-day orbit predictions, from
                        rapid analysis, including all active GLONASS and
                        Galileo satellites
      CODwwwwd.EPH_U    CODE ultra-rapid GNSS orbits from the 24UT solution
                        available until the corresponding early rapid orbit
                        is available (to ensure a complete coverage of orbits
                        even if the early rapid solution is delayed after the
                        first ultra-rapid solutions of the day)
      CODwwwwd.EPH_M    CODE final rapid GNSS orbits
                        (middle day of a long-arc solution where the rapid
                        observations were completed by a subsequent
                        ultra-rapid dataset)
      CODwwwwd.EPH_R    CODE early rapid GNSS orbits
                        (third day of a 72-hour solution)
      CODwwwwd.EPH_P    CODE 24-hour GNSS orbit predictions
      CODwwwwd.EPH_P2   CODE 48-hour GNSS orbit predictions
      CODwwwwd.EPH_5D   CODE 5-day GNSS orbit predictions
      
      type=current               | COD.EPH_U
      type=current-5d            | COD.EPH_5D
      type=urapid or ultra-rapid | CODwwwwd.EPH_U
      type=frapid or final-rapid | CODwwwwd.EPH_M
      type=erapid or early-rapid | CODwwwwd.EPH_R
      type=prediction            | CODwwwwd.EPH_P
      type=p2                    | CODwwwwd.EPH_P2
      type=p5                    | CODwwwwd.EPH_5D
    """
    if 'format' in kwargs and kwargs['format'] not in ['sp3']:
        raise RuntimeError('[ERROR] code::get_sp3_rapid Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_sp3_rapid Invalid acid.')
    if 'type' in kwargs and kwargs['type'] not in [
            'current', 'current-5d', 'urapid', 'ultra-rapid', 'frapid',
            'final-rapid', 'erapid', 'early-rapid', 'prediction', 'p2', 'p5'
    ]:
        raise RuntimeError('[ERROR] code::get_sp3_rapid Invalid type.')

    if 'format' not in kwargs:
        kwargs['format'] = 'sp3'
    if 'type' not in kwargs:
        kwargs['type'] = 'frapid'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    acn = 'COD'
    url_dir = 'CODE'
    if kwargs['type'] not in ['current', 'current-5d']:
        pydt = _date(**kwargs)  ## this may throw
        week, sow = pydt2gps(pydt)
        sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))

    if kwargs['type'] == 'current':
        sdate = ''
        frmt = 'EPH_U'
    elif kwargs['type'] == 'current-5d':
        sdate = ''
        frmt = 'EPH_5D'
    elif kwargs['type'] in ['urapid', 'ultra-rapid']:
        frmt = 'EPH_U'
    elif kwargs['type'] in ['frapid', 'final-rapid']:
        frmt = 'EPH_M'
    elif kwargs['type'] in ['erapid', 'early-rapid']:
        frmt = 'EPH_R'
    elif kwargs['type'] == 'prediction':
        frmt = 'EPH_P'
    elif kwargs['type'] == 'p2':
        frmt = 'EPH_P2'
    elif kwargs['type'] == 'p5':
        frmt = 'EPH_5D'
    else:
        raise RuntimeError('[ERROR] code::get_sp3_rapid Invalid type.')

    eph = '{:}{:}.{:}'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, eph)
    return target


def get_sp3(**kwargs):
    """
      kwargs that matter:
      format: Optional but if it exists it must be 'sp3'
      acid: 'cod' or 'cox' for final, GLONASS only solutions
      type='final', rapid, prediction, .... (see Table)
      save_as: '/some/path/foo.ION' Rename downloaded file to this filename
      save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
          save_as are given, then the local file will be the concatenation
          of these two, aka os.path.join(save_dir, save_as)
      To provide a date, use either:
        * pydt=datetime.datetime(...) or 
        * year=... and doy=...

      Default values:
      kwargs['format'] = sp3
      kwargs['acid'] = cod
      kwargs['type'] = final
      
      type=final
      CODwwwwd.EPH.Z    CODE final GNSS orbits
      COXwwwwd.EPH.Z    CODE final GLONASS orbits (for GPS weeks
                        0990 to 1066)
      type=current               | COD.EPH_U
      type=current-5d            | COD.EPH_5D
      type=urapid or ultra-rapid | CODwwwwd.EPH_U
      type=frapid or final-rapid | CODwwwwd.EPH_M
      type=erapid or early-rapid | CODwwwwd.EPH_R
      type=prediction            | CODwwwwd.EPH_P
      type=p2                    | CODwwwwd.EPH_P2
      type=p5                    | CODwwwwd.EPH_5D
    """
    """ redundant checks; performed in final/rapid functions
    if 'format' in kwargs and kwargs['format'] not in ['sp3']:
        raise ArgumentError('[ERROR] code::get_sp3 Invalid format', 'format',
                            **kwargs)
    if 'acid' in kwargs and kwargs['acid'] not in ['cod', 'cox']:
        raise ArgumentError('[ERROR] code::get_sp3 Invalid acid', 'acid',
                            **kwargs)
    if 'type' in kwargs and kwargs['type'] not in [
            'final', 'current', 'current-5d', 'urapid', 'ultra-rapid', 'frapid',
            'final-rapid', 'erapid', 'early-rapid', 'prediction', 'p2', 'p5'
    ]:
        raise ArgumentError('[ERROR] code::get_sp3 Invalid type', 'type',
                            **kwargs)
    """

    if 'format' not in kwargs:
        kwargs['format'] = 'sp3'
    if 'type' not in kwargs:
        kwargs['type'] = 'final'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    if kwargs['acid'] == 'cox' and kwargs['type'] != 'final':
        msg = '[ERROR] code::get_sp3 COX sp3 files only available for final products'
        raise RuntimeError(msg)

    if kwargs['type'] == 'final':
        target = get_sp3_final_target(**kwargs)
    else:
        target = get_sp3_rapid_target(**kwargs)

    indct = {}
    if 'save_as' in kwargs:
        indct['save_as'] = kwargs['save_as']
    if 'save_dir' in kwargs:
        indct['save_dir'] = kwargs['save_dir']
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local


def list_products():
    print(""" Information on Sp3 products available via CODE's ftp site can be 
  found at: {:}. Here is a table of products that can be downloaded via this 
  script:\n

  _Available files in FTP____________________________________________________
  COD.ERP_U         CODE ultra-rapid ERPs belonging to the
                    ultra-rapid orbit product
  COD.EPH_5D        Last update of CODE 5-day orbit predictions, from
                    rapid analysis, including all active GLONASS and
                    Galileo satellites
  CODwwwwd.EPH_U    CODE ultra-rapid GNSS orbits from the 24UT solution
                    available until the corresponding early rapid orbit
                    is available (to ensure a complete coverage of orbits
                    even if the early rapid solution is delayed after the
                    first ultra-rapid solutions of the day)
  CODwwwwd.EPH_M    CODE final rapid GNSS orbits
                    (middle day of a long-arc solution where the rapid
                    observations were completed by a subsequent
                    ultra-rapid dataset)
  CODwwwwd.EPH_R    CODE early rapid GNSS orbits
                    (third day of a 72-hour solution)
  CODwwwwd.EPH_P    CODE 24-hour GNSS orbit predictions
  CODwwwwd.EPH_P2   CODE 48-hour GNSS orbit predictions
  CODwwwwd.EPH_5D   CODE 5-day GNSS orbit predictions

  yyyy/
  CODwwwwd.EPH.Z    CODE final GNSS orbits
  COXwwwwd.EPH.Z    CODE final GLONASS orbits (for GPS weeks
                    0990 to 1066)
  yyyy_M/
  CODwwwwd.EPH_M.Z  CODE final rapid GNSS orbits (**)
    
  _Arguments for Products____________________________________________________
  type=final, acid=cod       | CODwwwwd.EPH.Z
  type=final, acid=cox       | COXwwwwd.EPH.Z
  type=current               | COD.EPH_U
  type=current-5d            | COD.EPH_5D
  type=urapid or ultra-rapid | CODwwwwd.EPH_U
  type=frapid or final-rapid | CODwwwwd.EPH_M
  type=erapid or early-rapid | CODwwwwd.EPH_R
  type=prediction            | CODwwwwd.EPH_P
  type=p2                    | CODwwwwd.EPH_P2
  type=p5                    | CODwwwwd.EPH_5D

  (**) Not available

  """.format(FTP_TXT))
    return
