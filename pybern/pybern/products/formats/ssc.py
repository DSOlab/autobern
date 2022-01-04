#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
import sys
import re

class SscSite:

    def __init__(self, **kwargs):
        self.domes = kwargs['domes']
        self.site_name = kwargs['site_name']
        self.id = kwargs['id']
        self.data_start = kwargs['data_start']
        self.data_stop = kwargs['data_stop']
        self.ref_epoch = kwargs['ref_epoch']
        self.soln = int(kwargs['soln'])
        self.x = float(kwargs['x'])
        self.sx = float(kwargs['sx']) if 'sx' in kwargs else 0e0
        self.y = float(kwargs['y'])
        self.sx = float(kwargs['sy']) if 'sy' in kwargs else 0e0
        self.z = float(kwargs['z'])
        self.sz = float(kwargs['sz']) if 'sz' in kwargs else 0e0
        self.vx = float(kwargs['vx'])
        self.svx = float(kwargs['svx']) if 'svx' in kwargs else 0e0
        self.vy = float(kwargs['vy'])
        self.svx = float(kwargs['svy']) if 'svy' in kwargs else 0e0
        self.vz = float(kwargs['vz'])
        self.svz = float(kwargs['svz']) if 'svz' in kwargs else 0e0

    def extrapolate(self, dt):
        # print('\t>> extrapolating from SOLN={:}'.format(self.soln))
        days = float((dt-self.ref_epoch).days)
        years = days / 365.25e0
        return self.x + self.vx*years, self.y + self.vy*years, self.z + self.vz*years

def parse_ssc_date(dstr, default=datetime.datetime.min):
    if dstr.strip() == '00:000:00000':
        return default
    flds = dstr.split(':')
    return datetime.datetime.strptime(':'.join(flds[0:2]), '%y:%j') + datetime.timedelta(seconds=int(flds[2]))

def min_of_ssc_records_of_same_site(ssc_recs):
    rec = ssc_recs[0]
    for i in ssc_recs[1:]:
        if i.soln < rec.soln:
            rec = i
    return rec

def max_of_ssc_records_of_same_site(ssc_recs):
    rec = ssc_recs[0]
    for i in ssc_recs[1:]:
        if i.soln > rec.soln:
            rec = i
    return rec

def match_site_in_rec_list(site, list):
    for s in list:
        if s.site_name == site.site_name:
            return True
    return False

def unique_records(ssc_records, dt):
    ssc_unique_records = []
    for site in ssc_records:
        if not match_site_in_rec_list(site, ssc_unique_records):
            # print('>> processing site {:}'.format(site.id))
            site_recs = [s for s in ssc_records if s.site_name == site.site_name]
            # print('\t>> num of entries = {:}'.format(len(site_recs)))
            rec = None
            max_date = datetime.datetime.min
            min_date = datetime.datetime.max
            
            for s in site_recs:
                if s.data_start < min_date: min_date = s.data_start
                if s.data_stop > max_date: max_date = s.data_stop
                if dt >= s.data_start and dt <= s.data_stop:
                    ssc_unique_records.append(s)
                    rec = s
                    # print('\t>> matched interval! breaking ....')
                    break
            if rec is None:
                if dt < min_date:
                    ssc_unique_records.append(min_of_ssc_records_of_same_site(site_recs))
                    # print('\t>> interval unmatched, adding min soln ...')
                elif dt > max_date:
                    ssc_unique_records.append(max_of_ssc_records_of_same_site(site_recs))
                    # print('\t>> interval unmatched, adding max soln ...')
                else:
                    ## probably no dt is between intervals ....
                    print('[WRNNG] No solution interval contains epoch {:} for site {:}_{:}; site skipped, don\'t know what to do!'.format(dt.strftime('%Y-%jT%H:%M'), site.id, site.domes), file=sys.stderr)

    return ssc_unique_records

def parse_ssc(ssc_fn, station_list=[], dt=None):
    ssc_records = []

    with open(ssc_fn, 'r') as fin:
        line = fin.readline()
        while line and not line.lstrip().startswith('DOMES NB. SITE NAME        TECH. ID.'):
            line = fin.readline()
        
        ## 2 header lines
        if not line:
            errmsg = '[ERROR] Failed to find header line in SSC file {:}'.format(ssc_fn)
            print(errmsg, file=sys.stderr)
            raise RuntimeError(errmsg)
        # assert(line.strip() == 'DOMES NB. SITE NAME        TECH. ID.       X/Vx         Y/Vy         Z/Vz.          Sigmas      SOLN  DATA_START     DATA_END   REF. EPOCH')
        assert(re.match(r"DOMES\s+NB\.\s+SITE NAME\s+TECH\. ID\.\s+X/Vx\s+Y/Vy\s+Z/Vz\.\s+Sigmas\s+SOLN\s+DATA_START\s+DATA_END\s+REF\.\s+EPOCH", line.strip()))
        line = fin.readline()
        #assert(line.strip()=='CLASS                   ----------------------------m/m/Y-------------------------')
        assert(re.match(r"[A-ZCLASS]*\s*-*m/m/Y-*", line.strip()))
        line = fin.readline()
        assert(line.strip().startswith('----------------------'))

        ## done with header, parse data
        line = fin.readline()
        while line:
            domes, site_name, tech, id, x, y, z, sx, sy, sz, soln, data_start, data_end, ref_epoch = line.split()
            x, y, z, sx, sy, sz = [float(n) for n in [x, y, z, sx, sy, sz]]
            data_start, data_end, ref_epoch = [parse_ssc_date(d) for d in [data_start, data_end, ref_epoch]]
            if data_end == datetime.datetime.min: data_end = datetime.datetime.max
            
            line = fin.readline()
            domes2, vx, vy, vz, svx, svy, svz = line.split()
            assert(domes2 == domes)
            vx, vy, vz, svx, svy, svz = [float(n) for n in [vx, vy, vz, svx, svy, svz]]

            if site_name.lower() in [s.lower() for s in station_list] or station_list==[] and dt>=data_start :
                ssc_records.append(SscSite(domes=domes, site_name=site_name, id=id, soln=soln, data_start=data_start, data_stop=data_end, ref_epoch=ref_epoch, x=x, y=y, z=z, sx=sx, sy=sy, sz=sz, vx=vx, vy=vy, vz=vz))

            line = fin.readline()


    return ssc_records if dt is None else unique_records(ssc_records, dt)

def ssc2crd(station_list, dt, *ssc_fn, **kwargs):
    sta_list = station_list
    sscsite_list = []
    
    for ssc in ssc_fn:
        # print('>> parsing ssc file {:}'.format(ssc))
        records = parse_ssc(ssc, sta_list, dt)
        for sta in records:
            index = [s.lower() for s in sta_list].index(sta.site_name.lower())
            if index >= 0:
                sta_list[index] = 'xxxx'
        sscsite_list += records

    header = kwargs['header'] if 'header' in kwargs else 'Coordinate Extrapolation from pybern'
    datum = kwargs['datum'] if 'datum' in kwargs else 'IGS_14'
    flag = kwargs['flag'] if 'flag' in kwargs else 'APR'
    with open(bcrd_out, 'w') as bout:
        print("{:}".format(header), file=bout)
        print("--------------------------------------------------------------------------------", file=bout)
        print("LOCAL GEODETIC DATUM: {:}           EPOCH: 2010-01-01 00:00:00".format(datum, dt.strftime("%Y-%m-%d %H:%M:%S")), file=bout)
        print("", file=bout)
        print("NUM  STATION NAME           X (M)          Y (M)          Z (M)     FLAG", file=bout)
        print("", file=bout)
        for record in sscsite_list:
            x, y, z = record.extrapolate(dt)
            print('{:} {:} {:+15.3f} {:+15.3f} {:+15.3f}'.format(record.id, record.domes, x, y, z))
