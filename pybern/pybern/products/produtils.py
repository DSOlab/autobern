#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
from pybern.products.gnssdates.gnssdates import mjd2pydt, gps2pydt, SEC_PER_DAY


def utils_pydt2yydoy(pydt):
    ''' Return two-digit year and day-of-year as integers (in a tuple) from a
        python datetime.datetime instance
    '''
    return [int(_) for _ in [pydt.strftime("%y"), pydt.strftime("%j")]]


def utils_whatever2pydt(**kwargs):
    '''
    '''
    ## pydt
    if 'pydt' in kwargs:
        if set(['year', 'doy', 'month', 'day', 'mjd', 'gwk', 'dow'
               ]).intersection(set(kwargs)) != set():
            status = 0
        else:
            return kwargs['pydt']
    ## yyyy, ddd to datetime
    if 'year' in kwargs and 'doy' in kwargs:
        if any([
                x for x in ['pydt', 'month', 'day', 'mjd', 'gwk', 'dow']
                if x in kwargs
        ]):
            status = 1
        else:
            return datetime.datetime(
                '{:} {:}'.format(kwargs['year'], kwargs['doy']), '%Y %j')
    ## yyyy, mm, dd
    elif set(['year', 'month',
              'day']).intersection(set(kwargs)) == set(['year', 'month',
                                                        'day']):
        if any([x for x in ['pydt', 'doy', 'mjd', 'gwk', 'dow'] if x in kwargs
               ]):
            status = 2
        else:
            return datetime.datetime(
                '{:} {:} {:}'.format(kwargs['year'], kwargs['month'],
                                     kwargs['day']), '%Y %m %d')
    ## mjd
    elif 'mjd' in kwargs:
        if set(['pydt', 'year', 'doy', 'month', 'day', 'gwk', 'dow'
               ]).intersection(set(kwargs)) != set():
            status = 3
        else:
            return mjd2pydt(float(kwargs['mjd']))
    ## wwww, d
    elif 'gwk' in kwargs and 'dow' in kwargs:
        if set(['pydt', 'year', 'doy', 'month', 'day', 'mjd']).intersection(
                set(kwargs)) != set():
            status = 4
        else:
            return gps2pydt(int(kwargs['gwk']),
                            float(kwargs['dow']) * SEC_PER_DAY)
    else:
        status = 10
    msg = '[ERROR] produtils::utils_whatever2pydt failed to parse date; status: {:}'.format(
        status)
    raise RuntimeError(msg)
