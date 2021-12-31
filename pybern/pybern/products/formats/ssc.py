#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime

class SscSite:

    def __init__(self):
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

    def extrapolate(dt):
        days = float((dt-self.ref_epoch).delta.days)
        years = days / 365.25e0
        return self.x + self.vx*years, self.y + self.vy*years, self.z + self.vz*years

def parse_ssc_date(dstr):
    flds = dstr.split(':')
    return datetime.datetime.strptime(':'.join(flds[0:2]), '%Y:%j') + datetime.timedelta(seconds=int(flds[2]))

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

def unique_records(ssc_records, dt):
    ssc_unique_records = []
    for site in ssc_records:
        site_recs = [s for s in ssc_records if s.site_name == site.site_name]
        rec = None
        max_date = datetime.datetime.min
        min_date = datetime.datetime.max
        
        for s in site_recs:
            if s.data_start < min_date: min_date = s.data_start
            if s.data_stop > max_date: max_date = s.data_stop
            if dt >= s.data_start and dt <= data_stop:
                rec = s
                break
        if rec is None:
            if dt < min_date:
                ssc_unique_records.append(min_of_ssc_records_of_same_site(site_recs))
            elif dt > max_date:
                ssc_unique_records.append(max_of_ssc_records_of_same_site(site_recs))
        else:
            ssc_unique_records.append(rec)

    return ssc_unique_records

def parse_ssc(ssc_fn, station_list=[], dt=None):
    ssc_records = []

    with open(ssc_fn, 'r') as ssc:
        line = fin.readline()
        while line and not line.startswith('DOMES NB. SITE NAME        TECH. ID.'):
            line = fin.readline()
        
        ## 2 header lines
        assert(line == 'DOMES NB. SITE NAME        TECH. ID.       X/Vx         Y/Vy         Z/Vz.          Sigmas      SOLN  DATA_START     DATA_END   REF. EPOCH')
        line = fin.readline()
        assert(line.strip()=='CLASS                   ----------------------------m/m/Y-------------------------')
        line = fin.readline()
        assert(line.strip().startswith('----------------------'))

        ## done with header, parse data
        line = fin.readline()
        while line:
            l = line.split()
            domes, site_name, tech, id, x, y, z, sx, sy, sz, soln, data_start, data_end, ref_epoch = line.split()
            x, y, z, sx, sy, sz = [float(n) for n in [x, y, z, sx, sy, sz]]
            data_start, data_end, ref_epoch = [parse_ssc_date(d) for d in [data_start, data_end, ref_epoch]]
            
            line = fin.readline()
            domes2, x, y, z, sx, sy, sz = line.split()
            assert(domes2 == domes)
            vx, vy, vz, svx, svy, svz = [float(n) for n in [x, y, z, sx, sy, sz]]

            if site_name.lower() in [s.lower() for s in station_list] or station_list==[] and dt>=data_start :
                ssc_records.append(SscSite(domes=domes, site_name=site_name, id=id, soln=soln, x=x, y=y, z=z, sx=sx, sy=sy, sz=sz, vx=vx, vy=vy, vz=vz))


    return ssc_records if dt is None else unique_records(ssc_records)
