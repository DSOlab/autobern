#! /usr/bin/python

from pybern.products.gnssdb_query import parse_db_credentials_file, query_sta_in_net, query_tsupd_net


db_credentials_dct = parse_db_credentials_file('/home/bpe/applications/autobern/bin/config.template')
qlist = query_sta_in_net('greece', db_credentials_dct)
for d in qlist:
    print('{:} {:}'.format(d['mark_name_DSO'], d['mark_numb_OFF']))
