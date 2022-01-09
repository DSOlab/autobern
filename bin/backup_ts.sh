#! /bin/bash

##
## simple script to backup the time-series folder.
## the script expects to find the folder: /home/bpe/data/time-series
## it will compress the directory to /home/bpe/data/time-series-YYMMDD.tar.gz
##

TS_DIR=/home/bpe/data/time-series

if ! test -d $TS_DIR
  then
  echo "ERROR Failed to find times-series dir $TS_DIR"
  exit 1
fi

dstr=$(date +"%y%m%d")
tar_archive=${HOME}/data/time-series-${dstr}.tar.gz

tar -zcvf ${tar_archive} ${TS_DIR}
