#! /usr/bin/python3
#-*- coding: utf-8 -*-

from __future__ import print_function
import os
import datetime
import sys
from pybern.products.fileutils.keyholders import extract_key_values
from pybern.products.downloaders.retrieve import web_retrieve
import mysql.connector
from mysql.connector import errorcode

g_verbose_rnxdwnl = False

sta_in_net_query=(
    """SELECT station.station_id, 
        station.mark_name_DSO, 
        stacode.mark_name_OFF, 
        stacode.station_name, 
        stacode.long_name,
        network.network_name 
        FROM station 
        JOIN stacode ON station.stacode_id=stacode.stacode_id 
        JOIN sta2nets ON sta2nets.station_id=station.station_id 
        JOIN network ON network.network_id=sta2nets.network_id 
        WHERE network.network_name=%s""")

def parse_db_credentials_file(credentials_file):
    ## parse credentials to a dictionary (from file)
    credentials_dct = {'GNSS_DB_USER':None, 'GNSS_DB_PASS':None, 'GNSS_DB_HOST':None, 'GNSS_DB_NAME':None}
    credentials_dct = extract_key_values(credentials_file, **credentials_dct)
    return credentials_dct

def execute_query(credentials_dct, query_str, *args):
    """ 
    """
    connection_error = 0 
    ## Connect to the database
    try:
        cnx = mysql.connector.connect(
            host=credentials_dct['GNSS_DB_HOST'], 
            database=credentials_dct['GNSS_DB_NAME'], 
            user=credentials_dct['GNSS_DB_USER'], 
            password=credentials_dct['GNSS_DB_PASS'],
            connect_timeout=10)
        ## get a cursor to perform queries ...
        cursor = cnx.cursor(dictionary=True)
        ## execute query ...
        cursor.execute(query_str, (args))
        ## get response
        rows = cursor.fetchall()
        ## close the cursor
        cursor.close()
    except mysql.connector.Error as err:
        print('[ERROR] Failed to connect to database!', file=sys.stderr)
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("[ERROR] Something is wrong with your user name or password", file=sys.stderr)
            connection_error = 10
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("[ERROR] Database does not exist", file=sys.stderr)
            connection_error = 11
        else:
            print('[ERROR] ' + str(err), file=sys.stderr)
            connection_error = 12
    
    if connection_error > 0:
        msg = '[ERROR] Failed to connect to to database at {:}@{:}; fatal!'.format(credentials_dct['GNSS_DB_NAME'], credentials_dct['GNSS_DB_HOST'])
        raise RuntimeError(msg)

    return rows

def query_sta_in_net(network, credentials_dct):
    """ Returns a dictionary of type:
        [{'station_id': 1, 'mark_name_DSO': 'pdel', ...}, {...}]
    """
    return execute_query(credentials_dct, sta_in_net_query, network)
