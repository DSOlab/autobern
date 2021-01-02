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


"""
def get_trp(pydt, **kwargs):
   Troposphere path delays of final or EUREF solution from BSWUSER52 yearly
      folder.
      By default the function will download the troposphere path delays of 
      final solution (aka BSWUSER52/yyyy/CODyyddd.TRP.Z). If you want the 
      EUREF solution (aka BSWUSER52/yyyy/COEyyddd.TRP.Z), specify the input 
      argument acid='coe'.

      kwargs that matter:
      acid = 'coe' Will get the EUREF solution
  
  if 'acid' in kwargs and kwargs['acid'] not in ['coe', 'COE']:
      raise RuntimeError('[ERROR] code::get_trp Invalid AC.')
  acn = kwargs['acid'].upper() if 'acid' in kwargs else CODE_AC
  yy, ddd = _pydt2yydoy(pydt)
  trp = '{:}{:2d}{:03d}.TRP.Z'.format(acn, yy, ddd)
  target = '{:}/BSWUSER52/{:}/{:}'.format(CODE_URL, pydt.strftime("%Y"), trp)
"""


def get_ion_final_target(pydt, **kwargs):
    """ Final ionosphere information in IONEX or Bernese format from COD

      kwargs that matter:
      format='ionex' or format='inx' to get the IONEX format.
      format='ion' or format='bernese' to get the Bernese format.
      acid='coe' to get the EUREF solution.
      type='final' Optional but if given must be 'final'

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod

      kwargs  |format=ionex                 | format=bernese               |
      --------+-----------------------------+------------------------------+
      acid=coe|BSWUSER52/ATM/yyyy/COEyyddd.INX.Z| BSWUSER52/ATM/yyyy/COEyyddd.ION.Z|
      acid=cod|CODE/yyyy/CODGddd0.yyI.Z     | CODE/yyyy/CODwwwwd.ION.Z     |
  """
    if 'format' in kwargs and kwargs['format'] not in [
            'ionex', 'inx', 'ion', 'bernese'
    ]:
        raise RuntimeError('[ERROR] code::get_ion_final Invalid format.')
    if 'acid' in kwargs and kwargs['acid'] not in ['cod', 'coe']:
        raise RuntimeError('[ERROR] code::get_ion_final Invalid acid.')
    if 'type' in kwargs and kwargs['type'] != 'final':
        raise RuntimeError('[ERROR] code::get_ion_final Invalid type.')

    if 'format' not in kwargs:
        kwargs['format'] = 'bernese'
    if 'acid' not in kwargs:
        kwargs['acid'] = 'cod'

    yy, ddd = _pydt2yydoy(pydt)
    if kwargs['format'] in ['bernese', 'ion']:
        frmt = 'ION'
    else:
        if kwargs['acid'] == 'coe':
            frmt = 'INX'
        else:
            frmt = '{:2d}I'.format(yy)

    if kwargs['acid'] == 'coe':
        url_dir = 'BSWUSER52/ATM/{:}'.format(pydt.strftime("%Y"))
        acn = 'COE'
        sdate = '{:2d}{:03d}'.format(yy, ddd)
    else:
        url_dir = 'CODE/{:}'.format(pydt.strftime("%Y"))
        if kwargs['format'] in ['bernese', 'ion']:
            acn = 'COD'
            week, sow = pydt2gps(pydt)
            sdate = '{:4d}{:1d}'.format(week, sow2dow(sow))
        else:
            acn = 'CODG'
            sdate = '{:03d}0'.format(ddd)

    ion = '{:}{:}.{:}.Z'.format(acn, sdate, frmt)
    target = '{:}/{:}/{:}'.format(CODE_URL, url_dir, ion)
    return target


def get_ion_rapid_target(pydt, **kwargs):
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
  
      Default Values
      kwargs['format'] = 'bernese'
      kwargs['type'] = 'rapid'

      aka:
      kwargs         |format=ionex        | format=bernese      |
      ---------------+--------------------+---------------------+
      type=rapid     |CODE/CORGddd0.yyI.Z | CODE/CODwwwwd.ION_R |
      type=prediction|CODE/COPGddd0.yyI.Z | CODE/CODwwwwd.ION_P |
      type=current   |                    | CODE/COD.ION_U      |
      type=p2        |                    | CODE/CODwwwwd.ION_P2|
      type=p5        |                    | CODE/CODwwwwd.ION_P5|

  """
    if 'format' in kwargs and kwargs['format'] not in [
            'ionex', 'inx', 'ion', 'bernese'
    ]:
        raise RuntimeError('[ERROR] code::get_ion_rapid Invalid format.')
    if 'type' in kwargs and kwargs['type'] not in [
            'rapid', 'prediction', 'current', 'p2', 'p5'
    ]:
        raise RuntimeError('[ERROR] code::get_ion_rapid Invalid type.')

    if 'format' not in kwargs:
        kwargs['format'] = 'bernese'
    if 'type' not in kwargs:
        kwargs['type'] = 'rapid'

    yy, ddd = _pydt2yydoy(pydt)

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
        week, sow = pydt2gps(pydt)
        sdate = '{:4d}{:1d}'.format(week, sow2dow(sow))
        if kwargs['type'] == 'rapid':
            frmt = 'ION_R'
        elif kwargs['type'] == 'prediction':
            frmt = 'ION_P'
        elif kwargs['type'] == 'p2':
            frmt = 'ION_P2'
        elif kwargs['type'] == 'p5':
            frmt = 'ION_P5'
        elif kwargs['type'] == 'current':
            frmt = 'ION_U'
            sdate = ''
        else:
            raise RuntimeError(
                '[ERROR] code::get_ion_rapid invalid request (#2)')

    ion = '{:}{:}.{:}'.format(acn, sdate, frmt)
    target = '{:}/CODE/{:}'.format(CODE_URL, ion)
    return target


def get_ion(pydt, **kwargs):
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

      Default values:
      kwargs['format'] = bernese
      kwargs['acid'] = cod
      kwargs['type'] = final

      type=final
      kwargs  |format=ionex                 | format=bernese               |
      --------+-----------------------------+------------------------------+
      acid=coe|BSWUSER52/yyyy/COEyyddd.INX.Z| BSWUSER52/yyyy/COEyyddd.ION.Z|
      acid=cod|CODE/yyyy/CODGddd0.yyI.Z     | CODE/yyyy/CODwwwwd.ION.Z     |
      
  
      kwargs         |format=ionex        | format=bernese      |
      ---------------+--------------------+---------------------+
      type=rapid     |CODE/CORGddd0.yyI.Z | CODE/CODwwwwd.ION_R |
      type=prediction|CODE/COPGddd0.yyI.Z | CODE/CODwwwwd.ION_P |
      type=current   |                    | CODE/COD.ION_U      |
      type=p2        |                    | CODE/CODwwwwd.ION_P2|
      type=p5        |                    | CODE/CODwwwwd.ION_P5|
  """
    if 'type' in kwargs and kwargs['type'] in [
            'rapid', 'prediction', 'current', 'p2', 'p5'
    ]:
        target = get_ion_rapid_target(pydt, **kwargs)
    elif 'type' not in kwargs or 'type' in kwargs and kwargs['type'] == 'final':
        target = get_ion_final_target(pydt, **kwargs)

    indct = {}
    if 'save_as' in kwargs: indct['save_as'] = kwargs['save_as']
    if 'save_dir' in kwargs: indct['save_dir'] = kwargs['save_dir']
    status, remote, local = web_retrieve(target, **indct)
    return status, remote, local
