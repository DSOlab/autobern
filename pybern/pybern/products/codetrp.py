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


def get_trp_final_target(pydt, **kwargs):
    """ Final tropospheric information in SINEX or Bernese format from COD

      CODwwwwd.TRO.Z  CODE final troposphere product, SINEX format
      CODyyddd.TRP.Z  Troposphere path delays of final solution
      COEyyddd.TRP.Z  Troposphere path delays of EUREF solution

      kwargs that matter:
      format='sinex' or format='tro' to get the Tropospheric SINEX format.
      format='trp' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      type='final' Optional but if given must be 'final'

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod

      kwargs  | format=bernese                   | format=sinex
      --------+----------------------------------+----------------------------
      acid=coe|BSWUSER52/ATM/yyyy/COEyyddd.TRP.Z |
      acid=cod|BSWUSER52/ATM/yyyy/CODyyddd.TRP.Z |CODE/yyyy/CODwwwwd.TRO.Z
  """
    if 'format' in kwargs and kwargs['format'] not in [
            'sinex', 'tro', 'trp', 'bernese'
    ]:
        raise RuntimeError('[ERROR] code::get_trp_final Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod', 'coe']:
        raise RuntimeError('[ERROR] code::get_trp_final Invalid acid.')
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise RuntimeError('[ERROR] code::get_trp_final Invalid type.')

    if 'format' not in kwargs:
        kwargs['format'] = 'bernese'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    frmt = 'TRP' if kwargs['format'] in ['bernese', 'trp'] else 'TRO'

    yy, ddd = _pydt2yydoy(pydt)
    if kwargs['acid'] == 'coe':
      if kwargs['format'] in ['sinex', 'tro']:
        msg = '[ERROR] code::get_trp_final No product in SINEX format for EUREF solution'
        raise RuntimeError(msg)
      url_dir = 'BSWUSER52/ATM/{:}'.format(pydt.strftime("%Y"))
      acn = 'COE'
      sdate = '{:2d}{:03d}'.format(yy, ddd)
    else:
        acn = 'COD'
        if kwargs['format'] in ['bernese', 'ion']:
          url_dir = 'BSWUSER52/ATM/{:}'.format(pydt.strftime("%Y"))
          sdate = '{:2d}{:03d}'.format(yy, ddd)
        else:
            url_dir = 'CODE/{:}'.format(pydt.strftime("%Y"))
            week, sow = pydt2gps(pydt)
            sdate = '{:4d}{:1d}'.format(week, sow2dow(sow))

    tro = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, tro)
    return target


def get_trp_rapid_target(pydt, **kwargs):
    """ Rapid or Ultra-rapid tropospheric information in SINEX or Bernese format 
      from COD
  
        COD.TRO_U         CODE ultra-rapid troposphere product in SINEX
                          format
        COD_TRO.SNX_U.Z   CODE ultra-rapid solution, as above but with 
                          troposphere parameters for selected sites, SINEX 
                          format
        CODwwwwd.TRO_R    CODE troposphere product from the early rapid
                          solution, SINEX format
        ________Unused________________________________________________________
        COD_TRO.SNX_U.Z   CODE ultra-rapid solution, as above but with 
                          troposphere parameters for selected sites, SINEX 
                          format
        CODwwwwd_TRO.SNX_R.Z  CODE early rapid solution, as above but with 
                          troposphere parameters for selected sites, SINEX 
                          format

      Default Values
      kwargs['format'] = 'sinex'
      kwargs['type'] = 'rapid'

      aka:
      kwargs           |format=sinex        | format=bernese      |
      -----------------+--------------------+---------------------+
      type=rapid       | CODwwwwd.TRO_R     |                     |
      type=urapid      | COD.TRO_U          |                     |
      type=urapid-sites| COD_TRO.SNX_U.Z    |                     |

  """
    if 'format' in kwargs and kwargs['format'] not in ['sinex', 'tro']:
        raise RuntimeError('[ERROR] code::get_trp_rapid Invalid format.')
    if 'type' in kwargs and kwargs['type'] not in ['rapid', 'urapid', 'urapid-sites']:
        raise RuntimeError('[ERROR] code::get_trp_rapid Invalid type.')

    if 'format' not in kwargs:
        kwargs['format'] = 'sinex'
    if 'type' not in kwargs:
        kwargs['type'] = 'rapid'

    yy, ddd = _pydt2yydoy(pydt)

    if kwargs['format'] in ['sinex', 'tro']:
      acn = 'COD'
      if kwargs['type'] == 'rapid':
        week, sow = pydt2gps(pydt)
        sdate = '{:4d}{:1d}'.format(week, sow2dow(sow))
        frmt = 'TRO_R'
      elif kwargs['type'] == 'urapid':
        sdate = ''
        frmt = 'TRO_U'
      elif kwargs['type'] == 'urapid-sites':
        sdate = '_TRO'
        frmt = 'SNX_U.Z'
      else:
        raise RuntimeError(
            '[ERROR] code::get_trp_rapid invalid request (#1)')
    else:
        raise RuntimeError(
            '[ERROR] code::get_ion_rapid invalid request (#2)')

    tro = '{:}{:}.{:}'.format(acn, sdate, frmt)
    target = '{:}/CODE/{:}'.format(CODE_URL, tro)
    return target


def get_trp(pydt, **kwargs):
    """
      kwargs that matter:
      format='sinex' or format='tro' to get the (tropospheric) SINEX format.
      format='trp' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      type='final', rapid, urapid, urapid-sites (see Table)
      save_as: '/some/path/foo.TRO' Rename downloaded file to this filename
      save_dir: 'foo/bar' Directory to save remote file; if both save_dir and 
          save_as are given, then the local file will be the concatenation
          of these two, aka os.path.join(save_dir, save_as)

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod
      kwargs['type'] = final

      type=final
      kwargs  | format=bernese                   | format=sinex
      --------+----------------------------------+----------------------------
      acid=coe|BSWUSER52/ATM/yyyy/COEyyddd.TRP.Z |
      acid=cod|BSWUSER52/ATM/yyyy/CODyyddd.TRP.Z |CODE/yyyy/CODwwwwd.TRO.Z
      
      kwargs           |format=sinex        | format=bernese      |
      -----------------+--------------------+---------------------+
      type=rapid       | CODwwwwd.TRO_R     |                     |
      type=urapid      | COD.TRO_U          |                     |
      type=urapid-sites| COD_TRO.SNX_U.Z    |                     |
  
  """
    if 'type' in kwargs and kwargs['type'] in [
            'rapid', 'urapid', 'urapid-sites'
    ]:
        target = get_trp_rapid_target(pydt, **kwargs)
    elif 'type' not in kwargs or 'type' in kwargs and kwargs['type'] == 'final':
        target = get_trp_final_target(pydt, **kwargs)

    indct = {}
    if 'save_as' in kwargs: indct['save_as'] = kwargs['save_as']
    if 'save_dir' in kwargs: indct['save_dir'] = kwargs['save_dir']
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local

def list_products():
  print(""" Information on Topospheric (and other) products available via CODE's 
  ftp site can be found at: {:}. Here is a table of products that can be 
  downloaded via this script:\n
  
  type=final
  -----------------+---------------------------------+--------------------------+
                   | format=bernese                   | format=sinex
  -----------------+----------------------------------+-------------------------+
  acid=coe         |BSWUSER52/ATM/yyyy/COEyyddd.TRP.Z |
  acid=cod         |BSWUSER52/ATM/yyyy/CODyyddd.TRP.Z |CODE/yyyy/CODwwwwd.TRO.Z
  -----------------+----------------------------------+-------------------------+
  kwargs           | format=bernese                   | format=sinex            |
  -----------------+----------------------------------+-------------------------+
  type=rapid       |                                  | CODE/CODwwwwd.TRO_R     |
  type=urapid      |                                  | CODE/COD.TRO_U          |
  type=urapid-sites|                                  | CODE/COD_TRO.SNX_U.Z    |
  
  (for non-final products, EUREF solutions, aka acid=coe, not available)
        
  CODwwwwd.TRO.Z    CODE final troposphere product, SINEX format
  CODyyddd.TRP.Z    Troposphere path delays of final solution
  COEyyddd.TRP.Z    Troposphere path delays of EUREF solution
  COD.TRO_U         CODE ultra-rapid troposphere product in SINEX format
  COD_TRO.SNX_U.Z   CODE ultra-rapid solution, as above but with 
                    troposphere parameters for selected sites, SINEX format
  CODwwwwd.TRO_R    CODE troposphere product from the early rapid solution, 
                    SINEX format
  ________Unused________________________________________________________
  COD_TRO.SNX_U.Z   CODE ultra-rapid solution, as above but with 
                    troposphere parameters for selected sites, SINEX format
  CODwwwwd_TRO.SNX_R.Z  CODE early rapid solution, as above but with 
                    troposphere parameters for selected sites, SINEX format
  """.format(FTP_TXT))
  return
