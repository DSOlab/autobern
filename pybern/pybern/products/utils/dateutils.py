#! /usr/bin/python
#-*- coding: utf-8 -*-

from __future__ import print_function
import datetime


def date_ranges_overlap(startA, endA, startB, endB):
    ''' https://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
  '''
    return (StartA <= EndB) and (EndA >= StartB)
