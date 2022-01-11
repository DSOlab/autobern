#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os, sys
import datetime
import re
import requests
import json

## https://gnss-metadata.eu/__test/site/api-docs#/Tools/get_sitelog_metadata_list
m3gurl = 'https://gnss-metadata.eu/__test/v1'

def get_latest_log(site, dir):
    
    pattern = site + r"_[0-9]{4}[0-9]{2}[0-9]{2}\.log"
    log = None
    t = datetime.datetime.min
    
    for f in os.listdir(dir):
      if re.match(pattern, f):
        g = re.match(site + r"_([0-9]{4}[0-9]{2}[0-9]{2})\.log", f)
        if t < datetime.datetime.strptime(str(g.group(1)), "%Y%m%d"):
          log = f
          t = datetime.datetime.strptime(str(g.group(1)), "%Y%m%d")

    return log, t

def answer2dict(text):
    """ Translate an M3G API request answer to a dictionary (aka 'text' should
        be the the response.text).
        Normaly the answer is not very simple to handle, cause it has the form:
        [header line] 'col0       col1      col2  col3 .....'
        [line1]       'value0     value1          valu3 ....'
        [line2]       ''
        which means that the text is arranged in columns, and some values may
        be missing. If the answer is empty, [line1] is '', in which case an 
        empty dictionary is returned.
        return value: {'col0':value0, 'col1':value1, 'col2':'', 'col3':value3}
    """
    text = text.split("\n")
    header = text[0]
    header_keys = [f.strip() for f in header.split(' ') if not re.match(r"^\s*$", f)]
    header_idxs = [header.find(k) for k in header_keys]
    header_idxs.append(len(text[0]))

    fields = None
    for line in text[1:]:
        header_idxs[-1] = len(line)
        if line.strip() != '':
            assert(fields == None)
            fields = [ line[idx:header_idxs[i+1]].strip() for i, idx in enumerate(header_idxs[0:-1])]

    ## if fields == None, we have no answer, but only the header line
    if fields is None: return {}
    
    dct={}
    assert(len(header_keys) == len(fields))
    for k,v in zip(header_keys, fields): dct[k]=v
    return dct

def request_metadata_list(site, country_code='GRC'):
    """ Get the metadata list (if any) for a given site. This function will
        use the M3G API.
        The input 'site' parameter should be the site's 9-char-id (aka the
        site's  long name). If it is only the 4-char-id, then also the site's
        country code is required.
        The function will return a dictionary holding metadata key/value pairs
        (depending on what is available on M3G)
    """
    g = re.match(r"([A-Z0-9]{4})[0-9]{2}([A-Z]{3})", site)
    if g and len(g.groups()) == 2:
        s4id = g.group(1)
        cid = g.group(2)
        s9id = g.group(0)
    else:
        cid = country_code
        s4id = site
        s9id = s4id + '00' + country_code

    qurl = m3gurl + '/sitelog/metadata-list'
    query = {'stationId': s4id, 'country':cid}
    response = requests.get(qurl, params=query, timeout=10)

    if response.status_code > 200:
        errmsg = '[ERROR] Failed to get station metadata info for site: {:}/{:}'.format(s4id, cid)
        raise RuntimeError(errmsg)

    return answer2dict(response.text)

def get_network_view(netid):
  """ Ask the M3G API about a given network. The function will return a 
      dictionary holding various metadata about the network, including a 
      field named 'included': [['BRUX00BEL', 'AUBG00DEU', 'NOA100GRC',...]
      whilh holds the stations of the network
  """
  qurl = m3gurl + '/network/view'
  query = {'id': netid}
  response = requests.get(qurl, params=query, timeout=10)
  if response.status_code > 200:
      errmsg = '[ERROR] Failed to get M3G network info for NETWORK_ID: {:}'.format(netid)
      raise RuntimeError(errmsg)
  return response.json()

def get_m3g_network_stations(netid, use_4char_ids=False):
    ndict = get_network_view(netid)
    
    if not use_4char_ids: return ndict['included']

    return [s[0:4] for s  in ndict['included']]

def get_exportlog(site, save_dir=os.getcwd(), only_if_newer=False, country_code='GRC'):
  """ Download the latest available M3G igs log file for a given station.
      The input 'site' parameter should be the site's 9-char-id (aka the
      site's  long name). If it is only the 4-char-id, then also the site's
      country code is required.
      save_dir is the directory to save the log file.
      If only_if_newer is set to true, then the function will first check if 
      the save_dir already holds a log file for the given station. It will 
      only download the requested log file if it is newer than the log file 
      (if any) present in the save_dir folder.
      The function will return the filename (including path) of the log file 
      downloaded; if 'only_if_newer' is set to true, then the filename of the 
      latest log file will be returned, either already available or downloaded.
  """
  ## get the correct site log name
  metadata_dct = request_metadata_list(site, country_code)
  if metadata_dct == {} or 'name_sitelog' not in metadata_dct:
    print('[WRNNG] No metadata list/log-file available via M3G for site {:}; skipping log file download'.format(site), file=sys.stderr)
    return None

  saveas = metadata_dct['name_sitelog']

  if only_if_newer:
    sid = metadata_dct['id'].lower()
    latest, t1 = get_latest_log(sid,save_dir)
    if latest is not None:
        g = re.match(sid + r"_([0-9]{4}[0-9]{2}[0-9]{2})\.log", saveas)
        if t1 >= datetime.datetime.strptime(str(g.group(1)), "%Y%m%d"):
          print('[DEBUG] A log file exists for station {:} (aka {:}) and is the latest update; skipping update'.format(site, latest))
          return os.path.join(save_dir,latest)
        else:
          print('[DEBUG] A log file exists for station {:} (aka {:}) but a newer version is available {:}'.format(site, latest, saveas))

  qurl = m3gurl + '/sitelog/exportlog'
  query = {'id': metadata_dct['id']}
  response = requests.get(qurl, params=query, timeout=10)

  if response.status_code > 200:
      errmsg = '[ERROR] Failed to get station log file for site: {:}'.format(metadata_dct['id'])
      raise RuntimeError(errmsg)

  with open(os.path.join(save_dir, saveas), 'w') as fout:
    fout.write(response.text)

  return os.path.join(save_dir, saveas)
