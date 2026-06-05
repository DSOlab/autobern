#! /bin/bash
##  Densification Benchmark for YEAR 2026 DOY 351-357  GPSWEEK 2293

ABPE_DIR="/home/bpe54/applications/autobern"
if ! test -d $ABPE_DIR
  then
  echo "ERROR. Cannot find directory $ABPE_DIR"
  exit 1
fi

CONFIG=config.greece
STATUS_FILE="${ABPE_DIR}/cron/repro26_greece_thales.log"
SERVER_NAME=$(hostname -s 2>/dev/null || hostname)

write_process_status() {
  process_time=$(date '+%Y-%m-%dT%H:%M:%S%z')
  printf '%s %s %s %s %s\n' "$process_time" "$year" "$doy" "$SERVER_NAME" "$1" >> "$STATUS_FILE"
}

## get the date 15 days ago
#year=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%Y\")))")
#yr2=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%y\")))")
#doy=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%j\")))")
year=1995

for doy in 001; do
  echo "Processing year ${year} - doy ${doy}..."
  yr2=${year:2:2}

  idoy=$(echo $doy | sed 's/^0*//g') ## remove leading '0'


  ## we need to make an a-priori crd file for the BPE
  python3 ${ABPE_DIR}/bin/make_apriori_crd.py -n greece \
    -c ${ABPE_DIR}/config/config.greece \
    -o ${HOME}/tables/crd/REG_${yr2}${doy}0.CRD \
    --ssc-files ${HOME}/tables/ssc/EUR0OPSSNX_1996001_2025270_00U_SOL.SSC \
    --crd-files ${HOME}/tables/crd/NTUA54.CRD \
    --date "${year}-${doy}" \
    --date-format '%Y-%j'
  apriori_status=$?
  if [ $apriori_status -ne 0 ]; then
    echo "ERROR. Failed to create a-priori CRD file"
    write_process_status "error"
    continue
  fi

  ## run the DD BPE ...
  python3 ${ABPE_DIR}/bin/rundd.py \
    -c ${ABPE_DIR}/config/config.greece \
    -n greece \
    -y ${year} \
    -d ${idoy} \
    --verbose \
    --use-euref-exclusion-list \
    --min-reference-stations 10 \
    --aprinf REG_${yr2}${doy}0
  rundd_status=$?

  rm -f ${HOME}/tables/crd/REG_${yr2}${doy}0.CRD
  if [ $rundd_status -ne 0 ]; then
     echo "ERROR. BPE and/or rundd script failed!"
     write_process_status "error"
     continue
  else
     write_process_status "solve" 
  fi

done 

exit 0
