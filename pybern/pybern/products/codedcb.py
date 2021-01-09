#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import sys
from pybern.products.gnssdates.gnssdates import pydt2gps, sow2dow
from pybern.products.downloaders.retrieve import web_retrieve

CODE_URL = 'ftp://ftp.aiub.unibe.ch'
CODE_AC = 'COD'
FTP_TXT = 'http://ftp.aiub.unibe.ch/AIUB_AFTP.TXT'


def _pydt2yydoy(pydt):
    return [int(_) for _ in [pydt.strftime("%y"), pydt.strftime("%j")]]


def get_dcb_final_target(pydt, **kwargs):
    """ Final Differential Code Bias (DCB) in DCB format from COD

      *type=final
        span=daily, obs=p1p2             | BSWUSER52/ORB/yyyy/CODyyddd.DCB.Z
        span=monthly, obs=p1c1           | CODE/yyyy/P1C1yymm.DCB.Z
        span=monthly, obs=p1p2           | CODE/yyyy/P1P2yymm.DCB.Z
        span=monthly, obs=p1p2all        | CODE/yyyy/P1P2yymm_ALL.DCB.Z
        span=monthly, obs=p1c1rnx        | CODE/yyyy/P1C1yymm_RINEX.DCB
        span=monthly, obs=p1c2rnx        | CODE/yyyy/P2C2yymm_RINEX.DCB

      kwargs that matter:
      format='dcb' Optional but if given it must be dcb
      type='final' Optional but if given must be 'final'
      acid='cod' Optional but if it exists it must be 'cod'
      span= daily or monthly
      obs= Choose from above table

      Default values:
      kwargs['format'] = dcb
      kwargs['acid'] = cod
      kwargs['type'] = final
      kwargs['span'] = monthly
      kwargs['obs'] = p1c1

  """
    if 'format' in kwargs and kwargs['format'] not in ['dcb']:
        raise RuntimeError('[ERROR] code::get_dcb_final Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_dcb_final Invalid acid.')
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise RuntimeError('[ERROR] code::get_dcb_final Invalid type.')
    if 'span' in kwargs and kwargs['span'] not in ['monthly', 'daily']:
        raise RuntimeError('[ERROR] code::get_dcb_final Invalid span.')
    if 'obs' in kwargs and kwargs['obs'] not in [
            'p1p2', 'p1c1', 'p1p2all', 'p1c1rnx', 'p1c2rnx'
    ]:
        raise RuntimeError('[ERROR] code::get_dcb_final Invalid obs.')

    if 'format' not in kwargs:
        kwargs['format'] = 'dcb'
    if 'type' not in kwargs:
        kwargs['type'] = 'final'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'
    if 'span' not in kwargs:
        kwargs['span'] = 'monthly'
    if 'obs' not in kwargs:
        kwargs['obs'] = 'p1c1'

    yy, ddd = _pydt2yydoy(pydt)
    mm, yyyy = pydt.strftime('%m'), pydt.strftime('%Y')

    spec = ''
    if kwargs['span'] == 'daily' and kwargs['obs'] == 'p1p2':
        acn = 'COD'
        sdate = '{:02d}{:03d}'.format(yy, ddd)
        url_dir = 'BSWUSER52/ORB/{:}'.format(yyyy)
        frmt = 'DCB.Z'
    elif kwargs['span'] == 'monthly':
        sdate = '{:02d}{:}'.format(yy, mm)
        url_dir = 'CODE/{:}'.format(yyyy)
        if kwargs['obs'] == 'p1c1':
            acn = 'P1C1'
            frmt = 'DCB.Z'
        elif kwargs['obs'] == 'p1p2':
            acn = 'P1P2'
            frmt = 'DCB.Z'
        elif kwargs['obs'] == 'p1p2all':
            acn = 'P1P2'
            spec = '_ALL'
            frmt = 'DCB.Z'
        elif kwargs['obs'] == 'p1c1rnx':
            acn = 'P1C1'
            spec = '_RINEX'
            frmt = 'DCB'
        elif kwargs['obs'] == 'p1c2rnx':
            acn = 'P1C2'
            spec = '_RINEX'
            frmt = 'DCB'
    try:
        dcb = '{:}{:}{:}.{:}.Z'.format(acn, sdate, spec, frmt)
        target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, dcb)
    except:
        msg = '[ERROR] code::get_dcb_final Failed to formulate DCB file'
        raise RuntimeError(msg)
    return target


def get_dcb_rapid_target(pydt, **kwargs):
    """ Rapid and Ultra-Rapid Differential Code Bias (DCB) in DCB format from 
      COD

       [1] type=rapid, span=daily, obs=p1p2        | BSWUSER52/ORB/yyyy/CORyyddd.DCB.Z
       [2] type=current, span=monthly, obs=p1c1    | P1C1.DCB (GPS sats only)
       [3] type=current, span=monthly, obs=p1p2    | P1P2.DCB
       [4] type=current, span=monthly, obs=p1p2all | P1P2_ALL.DCB
       [5] type=current, span=monthly, obs=p1p2gps | P1P2_GPS.DCB
       [6] type=current, span=monthly, obs=p1c1rnx | P1C1_RINEX.DCB
       [7] type=current, span=monthly, obs=p2c2rnx | P1C2_RINEX.DCB
       [8] type=current, span=monthly, obs=p1p2p1c1| CODE.DCB (merged [2] and [3])
       [9] type=current, span=monthly, obs=full    | CODE_FULL.DCB (merged [2], [3], [6] and [7])

      kwargs that matter:
      format='dcb' Optional but if given it must be dcb
      type=rapid or current; See table above
      acid='cod' Optional but if it exists it must be 'cod'
      span= daily or monthly
      obs= Choose from above table

      Default values:
      kwargs['format'] = dcb
      kwargs['acid'] = cod
      kwargs['type'] = current
      kwargs['span'] = monthly
      kwargs['obs'] = full

  """
    if 'format' in kwargs and kwargs['format'] not in ['dcb']:
        raise RuntimeError('[ERROR] code::get_dcb_rapid Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_dcb_rapid Invalid acid.')
    if 'type' in kwargs and kwargs['type'] not in ['rapid', 'current']:
        raise RuntimeError('[ERROR] code::get_dcb_rapid Invalid type.')
    if 'span' in kwargs and kwargs['span'] not in ['monthly', 'daily']:
        raise RuntimeError('[ERROR] code::get_dcb_rapid Invalid span.')
    if 'obs' in kwargs and kwargs['obs'] not in [
            'p1p2', 'p1c1', 'p1p2all', 'p1p2gps', 'p1c1rnx', 'p1c2rnx',
            'p1p2p1c1', 'full'
    ]:
        raise RuntimeError('[ERROR] code::get_dcb_rapid Invalid obs.')

    if 'format' not in kwargs:
        kwargs['format'] = 'dcb'
    if 'type' not in kwargs:
        kwargs['type'] = 'current'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'
    if 'span' not in kwargs:
        kwargs['span'] = 'monthly'
    if 'obs' not in kwargs:
        kwargs['obs'] = 'full'

    yy, ddd = _pydt2yydoy(pydt)
    mm, yyyy = pydt.strftime('%m'), pydt.strftime('%Y')

    spec = ''
    if kwargs['type'] == 'rapid' and kwargs['span'] == 'daily' and kwargs[
            'obs'] == 'p1p2':
        url_dir = 'BSWUSER/ORB/{:}'.format(yyyy)
        acn = 'COR'
        sdate = '{:02d}{:03d}'.format(yy, ddd)
        frmt = 'DCB.Z'
    elif kwargs['type'] == 'current' and kwargs['span'] == 'monthly':
        url_dir = 'CODE'
        frmt = 'DCB'
        sdate = ''
        if kwargs['obs'] == 'p1c1':
            acn = 'P1C1'
        elif kwargs['obs'] == 'p1p2':
            acn = 'P1P2'
        elif kwargs['obs'] == 'p1p2all':
            acn = 'P1P2'
            spec = '_ALL'
        elif kwargs['obs'] == 'p1p2gps':
            acn = 'P1P2'
            spec = '_GPS'
        elif kwargs['obs'] == 'p1c1rnx':
            acn = 'P1C1'
            spec = '_RINEX'
        elif kwargs['obs'] == 'p1c2rnx':
            acn = 'P1C2'
            spec = '_RINEX'
        elif kwargs['obs'] == 'p1c2rnx':
            acn = 'CODE'
            spec = ''
        elif kwargs['obs'] == 'full':
            acn = 'CODE'
            spec = '_FULL'
    try:
        dcb = '{:}{:}{:}.{:}.Z'.format(acn, sdate, spec, frmt)
        target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, dcb)
    except:
        msg = '[ERROR] code::get_dcb_rapid Failed to formulate DCB file'
        raise RuntimeError(msg)
    return target


def get_dcb(pydt, **kwargs):
    """ Get Differential Code Bias (DCB) in DCB format from COD

      *type=final
        span=daily, obs=p1p2             | BSWUSER52/ORB/yyyy/CODyyddd.DCB.Z
        span=monthly, obs=p1c1           | CODE/yyyy/P1C1yymm.DCB.Z
        span=monthly, obs=p1p2           | CODE/yyyy/P1P2yymm.DCB.Z
        span=monthly, obs=p1p2all        | CODE/yyyy/P1P2yymm_ALL.DCB.Z
        span=monthly, obs=p1c1rnx        | CODE/yyyy/P1C1yymm_RINEX.DCB
        span=monthly, obs=p1c2rnx        | CODE/yyyy/P2C2yymm_RINEX.DCB
       [1] type=rapid, span=daily, obs=p1p2        | BSWUSER52/ORB/yyyy/CORyyddd.DCB.Z
       [2] type=current, span=monthly, obs=p1c1    | P1C1.DCB (GPS sats only)
       [3] type=current, span=monthly, obs=p1p2    | P1P2.DCB
       [4] type=current, span=monthly, obs=p1p2all | P1P2_ALL.DCB
       [5] type=current, span=monthly, obs=p1p2gps | P1P2_GPS.DCB
       [6] type=current, span=monthly, obs=p1c1rnx | P1C1_RINEX.DCB
       [7] type=current, span=monthly, obs=p2c2rnx | P1C2_RINEX.DCB
       [8] type=current, span=monthly, obs=p1p2p1c1| CODE.DCB (merged [2] and [3])
       [9] type=current, span=monthly, obs=full    | CODE_FULL.DCB (merged [2], [3], [6] and [7])

      kwargs that matter:
      format:'dcb' Optional but if given it must be dcb
      type: Choose from table above (e.g. final, current, rapid)
      acid:'cod' Optional but if it exists it must be 'cod'
      span: daily or monthly
      obs: Choose from above table
      save_as: '/some/path/foo.ION' Rename downloaded file to this filename
      save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
          save_as are given, then the local file will be the concatenation
          of these two, aka os.path.join(save_dir, save_as)

      Default values:
      kwargs['format'] = dcb
      kwargs['acid'] = cod
      kwargs['type'] = final
      kwargs['span'] = monthly
      kwargs['obs'] = p1c1

  """
    if 'format' in kwargs and kwargs['format'] not in ['dcb']:
        raise RuntimeError('[ERROR] code::get_dcb Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_dcb Invalid acid.')
    if 'type' in kwargs and kwargs['type'] not in ['final', 'rapid', 'current']:
        raise RuntimeError('[ERROR] code::get_dcb Invalid type.')
    if 'span' in kwargs and kwargs['span'] not in ['monthly', 'daily']:
        raise RuntimeError('[ERROR] code::get_dcb Invalid span.')
    if 'obs' in kwargs and kwargs['obs'] not in (
        ['p1p2', 'p1c1', 'p1p2all', 'p1c1rnx', 'p1c2rnx'] + [
            'p1p2', 'p1c1', 'p1p2all', 'p1p2gps', 'p1c1rnx', 'p1c2rnx',
            'p1p2p1c1', 'full'
        ]):
        raise RuntimeError('[ERROR] code::get_dcb Invalid obs.')

    if 'format' not in kwargs:
        kwargs['format'] = 'dcb'
    if 'type' not in kwargs:
        kwargs['type'] = 'final'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'
    if 'span' not in kwargs:
        kwargs['span'] = 'monthly'
    if 'obs' not in kwargs:
        kwargs['obs'] = 'p1c1'

    if kwargs['type'] == 'final':
        target = get_dcb_final_target(pydt, **kwargs)
    else:
        target = get_dcb_rapid_target(pydt, **kwargs)

    indct = {}
    if 'save_as' in kwargs:
        indct['save_as'] = kwargs['save_as']
    if 'save_dir' in kwargs:
        indct['save_dir'] = kwargs['save_dir']
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local


def list_products():
    print(""" Information on Differential Code Bias (DCB) products available 
  via CODE's ftp site can be found at: {:}. Here is a table of products that 
  can be downloaded via this script:\n

  _Available files in FTP____________________________________________________
  P1C1.DCB          CODE sliding 30-day P1-C1 DCB solution, Bernese
                    format, containing only the GPS satellites
  P1P2.DCB          CODE sliding 30-day P1-P2 DCB solution, Bernese
                    format, containing all GPS and GLONASS satellites
  P1P2_ALL.DCB      CODE sliding 30-day P1-P2 DCB solution, Bernese
                    format, containing all GPS and GLONASS satellites
                    and all stations used
  P1P2_GPS.DCB      CODE sliding 30-day P1-P2 DCB solution, Bernese
                    format, containing only the GPS satellites
  P1C1_RINEX.DCB    CODE sliding 30-day P1-C1 DCB values directly
                    extracted from RINEX observation files, Bernese
                    format, containing the GPS and GLONASS satellites
                    and all stations used
  P2C2_RINEX.DCB    CODE sliding 30-day P2-C2 DCB values directly
                    extracted from RINEX observation files, Bernese
                    format, containing the GPS and GLONASS satellites
                    and all stations used
  CODE.DCB          Combination of P1P2.DCB and P1C1.DCB
  CODE_FULL.DCB     Combination of P1P2.DCB, P1C1.DCB (GPS satellites),
                    P1C1_RINEX.DCB (GLONASS satellites), and P2C2_RINEX.DCB

  BSWUSER52/ORB/yyyy
  CORyyddd.DCB.Z    Daily P1-P2 DCB estimates of rapid where
                    final information is not yet available
  CODyyddd.DCB.Z    Daily P1-P2 DCB estimates of final solution
  
  CODE/yyyy/
  P1C1yymm.DCB.Z    CODE monthly P1-C1 DCB solution, Bernese format,
                    containing only the GPS satellites
  P1P2yymm.DCB.Z    CODE monthly P1-P2 DCB solution, Bernese format,
                    containing all GPS and GLONASS satellites
  P1P2yymm_ALL.DCB.Z
                    CODE monthly P1-P2 DCB solution, Bernese format,
                    containing all GPS and GLONASS satellites and all
                    stations used
  P1C1yymm_RINEX.DCB
                    CODE monthly P1-C1 DCB values directly extracted
                    from RINEX observation files, Bernese format,
                    containing the GPS and GLONASS satellites and all
                    stations used
  P2C2yymm_RINEX.DCB
                    CODE monthly P2-C2 DCB values directly extracted
                    from RINEX observation files, Bernese format,
                    containing the GPS and GLONASS satellites and all
                    stations used

    
  _Arguments for Products____________________________________________________
  *type=final
    span=daily, obs=p1p2             | BSWUSER52/ORB/yyyy/CODyyddd.DCB.Z
    span=monthly, obs=p1c1           | CODE/yyyy/P1C1yymm.DCB.Z
    span=monthly, obs=p1p2           | CODE/yyyy/P1P2yymm.DCB.Z
    span=monthly, obs=p1p2all        | CODE/yyyy/P1P2yymm_ALL.DCB.Z
    span=monthly, obs=p1c1rnx        | CODE/yyyy/P1C1yymm_RINEX.DCB
    span=monthly, obs=p1c2rnx        | CODE/yyyy/P2C2yymm_RINEX.DCB
  *non-final products
 [1] type=rapid, span=daily, obs=p1p2        | BSWUSER52/ORB/yyyy/CORyyddd.DCB.Z
 [2] type=current, span=monthly, obs=p1c1    | P1C1.DCB (GPS sats only)
 [3] type=current, span=monthly, obs=p1p2    | P1P2.DCB
 [4] type=current, span=monthly, obs=p1p2all | P1P2_ALL.DCB
 [5] type=current, span=monthly, obs=p1p2gps | P1P2_GPS.DCB
 [6] type=current, span=monthly, obs=p1c1rnx | P1C1_RINEX.DCB
 [7] type=current, span=monthly, obs=p2c2rnx | P1C2_RINEX.DCB
 [8] type=current, span=monthly, obs=p1p2p1c1| CODE.DCB (merged [2] and [3])
 [9] type=current, span=monthly, obs=full    | CODE_FULL.DCB (merged [2], [3], [6] and [7])

  """.format(FTP_TXT))
    return
