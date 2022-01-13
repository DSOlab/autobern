#! /bin/bash

ABPE_DIR="/home/bpe/applications/autobern"
if ! test -d $ABPE_DIR
  then
  echo "ERROR. Cannot find directory $ABPE_DIR"
  exit 1
fi

CONFIG=config.greece

## get the date 15 days ago
year=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%Y\")))")
yr2=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%y\")))")
doy=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = 15)).strftime(\"%j\")))")
idoy=$(echo $doy | sed 's/^0*//g') ## remove leading '0'

## we need to make an a-priori crd file for the BPE
python3 ${ABPE_DIR}/bin/make_apriori_crd.py -n greece \
  -c ${ABPE_DIR}/config/config.greece \
  -o ${HOME}/tables/crd/REG${yr2}${doy}0.CRD \
  --ssc-files ${HOME}/tables/ssc/EPN_A_IGS14.SSC ${HOME}/tables/ssc/EPN_IGb14.SSC ${HOME}/tables/ssc/EPND_D2150_IGS14.SSC \
  --crd-files ${HOME}/tables/crd/NTUA52.CRD \
  --date "${year}-${doy}" \
  --date-format '%Y-%j' \
   || { echo "ERROR. Failed to create a-priori CRD file"; exit 1; }

## run the DD BPE ...
python3 ${ABPE_DIR}/bin/rundd.py \
  -c ${ABPE_DIR}/config/config.greece \
  -n greece \
  -y ${year} \
  -d ${idoy} \
  --verbose \
  --use-euref-exclusion-list \
  --min-reference-stations 10 \
  --aprinf REG${yr2}${doy}0 \
  || { echo "ERROR. BPE and/or rundd script failed!"; exit 1; }

echo "$year $doy"
