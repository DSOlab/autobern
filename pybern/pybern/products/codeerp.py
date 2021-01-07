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


def get_erp_final_target(pydt, **kwargs):
    """ Final Earth Rotation Parameters (ERP) files in from COD

      kwargs that matter:
      span='daily' for daily ERP's or 'weekly' for weekly ERP file
      code_dir='code' to download files from CODE_URL/CODE/yyyy or 'bswuser52' 
                to download from CODE_URL/BSWUSER52/ORB/yyyy
      acid='cod' Optional but if given must be cod
      type='final' Optional but if given must be 'final'
      format='bernese' Optional but if given must be 'bernese'

      Default values:
      kwargs['span'] = daily

      CODwwww7.ERP.Z    Weekly CODE final ERP files as from week 0978 (*)
      CODyyddd.ERP.Z    Daily CODE final ERP files as from week 1706 (*)
      CODwwwwd.ERP.Z    CODE final ERPs belonging to the final orbits (+)
      CODwwww7.ERP.Z    Collection of the 7 daily COD-ERP solutions of the 
                        week (+)

      type=final
                        |span=daily                          | span=weekly                        |
      ------------------+------------------------------------+------------------------------------+
      code_dir=code     | /CODE/yyyy/CODwwwwd.ERP.Z          | /CODE/yyyy/CODwwww7.ERP.Z          |
      code_dir=bswuser52| /BSWUSER52/ORB/yyyy/CODyyddd.ERP.Z | /BSWUSER52/ORB/yyyy/CODwwww7.ERP.Z |


      (*) under /BSWUSER52/ORB/yyyy
      (+) under /CODE/yyyy

      I cannot find any difference between CODwwww7.ERP.Z Vs CODwwww7.ERP.Z,
      and CODyyddd.ERP.Z Vs CODwwwwd.ERP.Z. Hence, we add an optional argument
      'code_dir' which can take the values 'bswuser52' and 'code' and decides 
      which of the two options will be used (aka the remote ftp directory). By 
      default, the value defaults to code_dir=code

  """
    if 'format' in kwargs and kwargs['format'] not in ['bernese']:
        raise RuntimeError('[ERROR] code::get_erp_final Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_erp_final Invalid acid.')
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise RuntimeError('[ERROR] code::get_erp_final Invalid type.')
    if 'span' in kwargs and kwargs['span'] not in ['daily', 'weekly']:
        raise RuntimeError('[ERROR] code::get_erp_final Invalid span.')
    if 'code_dir' in kwargs and kwargs['code_dir'] not in ['bswuser52', 'code']:
        raise RuntimeError('[ERROR] code::get_erp_final Invalid code_dir.')

    if 'span' not in kwargs:
        kwargs['span'] = 'daily'
    if 'code_dir' not in kwargs:
        kwargs['code_dir'] = 'code'

    yy, ddd = _pydt2yydoy(pydt)
    week, sow = pydt2gps(pydt)

    if kwargs['code_dir'] == 'code':
        url_dir = '{:}/{:}'.format('CODE', pydt.strftime('%Y'))
    else:
        url_dir = '{:}/{:}/{:}'.format('BSWUSER52', 'ORB', pydt.strftime('%Y'))

    acn = 'COD'
    frmt = 'ERP'
    if kwargs['span'] == 'weekly':
        sdate = '{:04d}{:1d}'.format(week, 7)
    else:
        if kwargs['code_dir'] == 'code':
            sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))
        else:
            sdate = '{:02d}{:03d}'.format(yy, ddd)

    erp = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, erp)
    return target


def get_erp_rapid_target(pydt, **kwargs):
    """ Rapid , Ultra-Rapid and Predicted Final Earth Rotation Parameters (ERP) 
      files in from COD
        
      kwargs that matter:
      acid='cod' Optional but if given must be cod
      format='bernese' Optional but if given must be 'bernese'
      type=[...] If not given, default value is 'frapid'

      CODwwwwd.ERP_M.Z  CODE final rapid ERPs belonging to the final rapid 
                          orbits (-)
      COD.ERP_U         CODE ultra-rapid ERPs belonging to the ultra-rapid 
                          orbit product
      CODwwwwd.ERP_U    CODE ultra-rapid ERPs belonging to the ultra-rapid 
                          orbits
      CODwwwwd.ERP_M    CODE final rapid ERPs belonging to the final rapid 
                          orbits
      CODwwwwd.ERP_R    CODE early rapid ERPs belonging to the early rapid 
                          orbits
      CODwwwwd.ERP_P    CODE predicted ERPs belonging to the predicted
                          24-hour orbits
      CODwwwwd.ERP_P2   CODE predicted ERPs belonging to the predicted
                          48-hour orbits
      CODwwwwd.ERP_5D   CODE predicted ERPs belonging to the predicted
                          5-day orbits

      (-) under /CODE/yyyy_M

      type=urapid or ultra-rapid | CODwwwwd.ERP_U or COD.ERP_U
      type=frapid or final-rapid | CODwwwwd.ERP_M or CODwwwwd.ERP_M.Z
      type=erapid or early-rapid | CODwwwwd.ERP_R
      type=prediction            | CODwwwwd.ERP_P
      type=p2                    | CODwwwwd.ERP_P2
      type=p5                    | CODwwwwd.ERP_5D
  """
    if 'format' in kwargs and kwargs['format'] not in ['bernese']:
        raise RuntimeError('[ERROR] code::get_erp_rapid Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod']:
        raise RuntimeError('[ERROR] code::get_erp_rapid Invalid acid.')
    if 'type' in kwargs and kwargs['type'] not in [
            'urapid', 'ultra-rapid', 'frapid', 'final-rapid', 'erapid',
            'early-rapid', 'prediction', 'p2', 'p5'
    ]:
        raise RuntimeError('[ERROR] code::get_erp_rapid Invalid type.')

    if 'type' not in kwargs:
        kwargs['type'] = 'frapid'

    week, sow = pydt2gps(pydt)
    sdate = '{:04d}{:01d}'.format(week, sow2dow(sow))
    acn = 'COD'
    url_dir = 'CODE'

    if kwargs['type'] in ['urapid', 'ultra-rapid']:
        frmt = 'ERP_U'
    elif kwargs['type'] in ['frapid', 'final-rapid']:
        frmt = 'ERP_M'
    elif kwargs['type'] in ['erapid', 'early-rapid']:
        frmt = 'ERP_R'
    elif kwargs['type'] in ['prediction']:
        frmt = 'ERP_P'
    elif kwargs['type'] in ['p2']:
        frmt = 'ERP_P2'
    elif kwargs['type'] in ['p5']:
        frmt = 'ERP_5D'

    erp = '{:}{:}.{:}'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, erp)
    return target


def get_erp(pydt, **kwargs):
    """
      kwargs that matter:
      format Optional but if it exists it must be 'bernese'
      acid Optional but if it exists it must be 'cod'
      type='final', rapid, prediction, current, .... (see Table)
      save_as: '/some/path/foo.ION' Rename downloaded file to this filename
      save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
          save_as are given, then the local file will be the concatenation
          of these two, aka os.path.join(save_dir, save_as)

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod
      kwargs['type'] = final

      type=final
                        |span=daily                          | span=weekly                        |
      ------------------+------------------------------------+------------------------------------+
      code_dir=code     | /CODE/yyyy/CODwwwwd.ERP.Z          | /CODE/yyyy/CODwwww7.ERP.Z          |
      code_dir=bswuser52| /BSWUSER52/ORB/yyyy/CODyyddd.ERP.Z | /BSWUSER52/ORB/yyyy/CODwwww7.ERP.Z |
      
      type=urapid or ultra-rapid | CODwwwwd.ERP_U or COD.ERP_U
      type=frapid or final-rapid | CODwwwwd.ERP_M or CODwwwwd.ERP_M.Z
      type=erapid or early-rapid | CODwwwwd.ERP_R
      type=prediction            | CODwwwwd.ERP_P
      type=p2                    | CODwwwwd.ERP_P2
      type=p5                    | CODwwwwd.ERP_5D


      (*) under /BSWUSER52/ORB/yyyy
      (+) under /CODE/yyyy
  """
    if 'type' in kwargs and kwargs['type'] in [
            'urapid', 'ultra-rapid', 'frapid', 'final-rapid', 'erapid',
            'early-rapid', 'prediction', 'p2', 'p5'
    ]:
        target = get_erp_rapid_target(pydt, **kwargs)
    elif 'type' not in kwargs or 'type' in kwargs and kwargs['type'] == 'final':
        target = get_erp_final_target(pydt, **kwargs)
    else:
        msg = '[ERROR] codeerp::get_erp Invalid erp type: {:}'.format(
            kwargs['type'])
        raise RuntimeError(msg)

    indct = {'type': kwargs['type']}
    if 'save_as' in kwargs:
        indct['save_as'] = kwargs['save_as']
    if 'save_dir' in kwargs:
        indct['save_dir'] = kwargs['save_dir']
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local


def list_products():
    print(""" Information on EarthRotation Parameters (ERP) products available 
  via CODE's ftp site can be found at: {:}. Here is a table of products that
  can be downloaded via this script:\n
      
  CODwwww7.ERP.Z    Weekly CODE final ERP files as from week 0978 (*)
  CODyyddd.ERP.Z    Daily CODE final ERP files as from week 1706 (*)
  CODwwwwd.ERP.Z    CODE final ERPs belonging to the final orbits (+)
  CODwwww7.ERP.Z    Collection of the 7 daily COD-ERP solutions of the 
                    week (+)

  type=final
                    |span=daily                          | span=weekly                        |
  ------------------+------------------------------------+------------------------------------+
  code_dir=code     | /CODE/yyyy/CODwwwwd.ERP.Z          | /CODE/yyyy/CODwwww7.ERP.Z          |
  code_dir=bswuser52| /BSWUSER52/ORB/yyyy/CODyyddd.ERP.Z | /BSWUSER52/ORB/yyyy/CODwwww7.ERP.Z |
  ------------------+------------------------------------+------------------------------------+
  type=urapid or ultra-rapid | CODwwwwd.ERP_U [or COD.ERP_U] (**)
  type=frapid or final-rapid | CODwwwwd.ERP_M [or CODwwwwd.ERP_M.Z] (**)
  type=erapid or early-rapid | CODwwwwd.ERP_R
  type=prediction            | CODwwwwd.ERP_P
  type=p2                    | CODwwwwd.ERP_P2
  type=p5                    | CODwwwwd.ERP_5D


  CODwwwwd.ERP_M.Z  CODE final rapid ERPs belonging to the final rapid 
                      orbits (-)(**)
  COD.ERP_U         CODE ultra-rapid ERPs belonging to the ultra-rapid 
                      orbit product (**)
  CODwwwwd.ERP_U    CODE ultra-rapid ERPs belonging to the ultra-rapid 
                      orbits
  CODwwwwd.ERP_M    CODE final rapid ERPs belonging to the final rapid 
                      orbits
  CODwwwwd.ERP_R    CODE early rapid ERPs belonging to the early rapid 
                      orbits
  CODwwwwd.ERP_P    CODE predicted ERPs belonging to the predicted
                      24-hour orbits
  CODwwwwd.ERP_P2   CODE predicted ERPs belonging to the predicted
                      48-hour orbits
  CODwwwwd.ERP_5D   CODE predicted ERPs belonging to the predicted
                      5-day orbits

  (*) under /BSWUSER52/ORB/yyyy
  (+) under /CODE/yyyy
  (-) under /CODE/yyyy_M
  (**) files in brackets (aka []) are not considered
  """.format(FTP_TXT))
    return
