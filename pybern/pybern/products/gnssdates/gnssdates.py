#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime
""" Global Variables (Constants)
"""
JAN61980 = 44244
JAN11901 = 15385
SEC_PER_DAY = 86400e0

## First day in month
month_day = [[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365],
             [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366]]


def mjd2pydt(mjd, fmjd=0e0):
    ''' Convert a date given in Modified Julian Date format, to
      a Python datetime.datetime object. The input MJD can be split
      in any convinient way between the parameters mjd and
      fmjd. Or fmjd can be ignored and the date passed
      in mjd.

      :param mjd:  The Modified Julian Date; can be either float 
                   or integer
      :param fmjd: In case the MJD is plit in two parts, this is
                   the second part of the input MJD. E.g. if
                   MJD = 57222.75, then, for increased accuracy,
                   one can use mjd = 57222 and fmjd = .75.

      :returns:    A Python datetime.datetime object, representing the input
                   (MJD) date.
    '''
    jd = mjd + fmjd
    i, d = divmod(jd, 1)
    mjd = int(i)  ## just to be sure !
    fmjd = float(d)

    days_fr_jan1_1901 = mjd - JAN11901
    num_four_yrs = days_fr_jan1_1901 // 1461
    years_so_far = 1901 + 4 * num_four_yrs
    days_left = days_fr_jan1_1901 - 1461 * num_four_yrs
    delta_yrs = days_left // 365 - days_left // 1460

    year = years_so_far + delta_yrs
    yday = days_left - 365 * delta_yrs + 1
    hour = int(fmjd * 24e0)
    minute = int(fmjd * 1440e0 - hour * 60e0)
    second = fmjd * 86400e0 - hour * 3600e0 - minute * 60e0
    leap = int(year % 4 == 0)
    guess = int(yday * 0.032e0)
    if leap > 1 or guess + 1 > len(month_day[0]):
        raise RuntimeError('[ERROR] gnssdates::mjd2pydt Invalid MJD date (#1).')
    more = int((yday - month_day[leap][guess + 1]) > 0)
    month = guess + more + 1
    mday = yday - month_day[leap][guess + more]

    try:
        return datetime.datetime(year,
                                 month,
                                 mday,
                                 hour,
                                 minute,
                                 microsecond=int(second * 1e6))
    except:
        raise RuntimeError('[ERROR] gnssdates::mjd2pydt Invalid MJD date (#2).')


def pydt2ydoy(datetm):
    ''' Transform a Python datetime.datetime instance to year and 
      day of year.

      :param datetm: A Python datetime.datetime or datetime.date isntance

      :returns: A tuple consisting of [year, day_of_year, hour, minute, second]
  '''
    try:
        iyear = int(datetm.strftime('%Y'))
        idoy = int(datetm.strftime('%j'))
    except:
        raise RuntimeError('[ERROR] gnssdates::pydt2ydoy Invalid date.')

    if type(datetm) is datetime.date:
        ihour = 0
        imin = 0
        isec = 0
    elif type(datetm) is datetime.datetime:
        ihour = datetm.hour
        imin = datetm.minute
        isec = datetm.second
    else:
        raise RuntimeError(
            '[ERROR] gnssdates::pydt2ydoy Non-datetime object passed as input')

    return iyear, idoy, ihour, imin, isec


def ydoy2mjd(year, doy, hour=0, minute=0, seconds=0e0):
    ''' Transform a tuple of year and day of year (i.e. doy)
      to Modified Julian Date and fraction of day.
      Optional arguments include hour, minute and seconds.

      :returns: A tuple consisting of [mjd, fmjd], where mjd is the
                (integer) Modified Julian Date and fmjd is the fraction
                of day (float).

  '''
    try:
        iyear = int(year)
        idoy = int(doy)
        ihour = int(hour)
        imin = int(minute)
        fsec = float(seconds)
    except:
        raise RuntimeError('[ERROR] gnssdates::ydoy2mjd Invalid date.')

    status = 0
    if idoy < 1 or idoy > 366:
        status = 1

    if ihour < 0 or ihour > 23 or imin < 0 or imin > 59 or fsec < 0e0 or fsec > 60e0:
        status = 2

    if status != 0:
        raise RuntimeError('[ERROR] gnssdates::ydoy2mjd Invalid date.')

    mjd = ((iyear - 1901) // 4) * 1461 + (
        (iyear - 1901) % 4) * 365 + idoy - 1 + JAN11901
    fmjd = ((fsec / 60.0 + imin) / 60.0 + ihour) / 24.0

    return int(mjd), fmjd


def ydoy2pydt(year, doy, hour=0, minute=0, seconds=0e0):
    ''' Transform a date, given as year and day of year 
      (i.e. doy) to a valid Python datetime instance.
      Optional arguments include hour, minute and seconds,
      all integers.

      :returns: A Python datetime.datetime instance.

  '''
    try:
        iyear = int(year)
        idoy = int(doy)
        ihour = int(hour)
        imin = int(minute)
        isec = int(seconds)
    except:
        raise RuntimeError('[ERROR] gnssdates::ydoy2pydt Invalid date.')

    date_string = '%4i %03i %02i %02i %02i' % (iyear, idoy, ihour, imin, isec)

    try:
        return datetime.strptime(date_string, '%Y %j %H %M %S')
    except:
        raise RuntimeError('[ERROR] gnssdates::ydoy2pydt Invalid date.')


def ydoy2gps(year, doy, hour=0, minute=0, seconds=0e0):
    ''' Transform a tuple of year and day of year (i.e. doy)
      to GpsWeek and SecondsOfWeek.

      :param year: Integer, the year
      :param doy:  Integer, the day of year
      :param hour: Integer, the hour of day (optional)
      :param minute: Integer, the minute of hour (optional)
      :param seconds: Float or integer, the seconds of minute (optional)

      :returns: A tuple of (int, float), consisting of [gps_week, sec_of_week].
  '''
    try:
        [mjd, fmjd] = ydoy2mjd(year, doy, hour, minute, seconds)
    except:
        raise

    gps_week = (mjd - JAN61980) // 7
    sec_of_week = ((mjd - JAN61980) - gps_week * 7 + fmjd) * SEC_PER_DAY
    if sec_of_week < 0 or sec_of_week > 86400e0 * 7:
        raise RuntimeError('[ERROR] gnssdates::ydoy2gps Invalid date.')
    '''
    assert(not any([ not (x).is_integer() for x in [gps_week, sec_of_week] ]))
    return [ int(x) for x in [gps_week, sec_of_week] ]
    '''
    return int(gps_week), sec_of_week


def pydt2gps(datetm):
    ''' Transform a Python datetime.datetime instance to 
      GpsWeek and SecondsOfWeek.

      :param datetm: A Python datetime.datetime or datetime.date isntance

      :returns: A tuple 
  '''
    try:
        year, doy, hour, _min, sec = pydt2ydoy(datetm)
        return ydoy2gps(year, doy, hour, _min, sec)
    except:
        raise


def sow2dow(sow):
    """ GPS seconds of week to day of week
  """
    if sow < 0 or sow > 86400e0 * 7:
        raise RuntimeError('[ERROR] gnssdates::sow2dow Invalid date.')
    return int(sow) // 86400


def two_digit_year(year):
    year = int(year)
    return year - 2000 if year > 2000 else year - 1900
