#! /usr/bin/python

from pybern.products.utils.dctutils import merge_dicts

d1 = {'a':1, 'b':2, 'c':3}
d2 = {'d':0, 'e':10}
d3 = None

print(merge_dicts(d1,d2))
print(merge_dicts(d1,d3,True))
