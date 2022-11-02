#! /bin/bash

args=("$@")
before=${args[0]}
echo "Num days before: $before"

ABPE_DIR="/home/bpe/applications/autobern"
if ! test -d $ABPE_DIR
  then
  echo "ERROR. Cannot find directory $ABPE_DIR"
  exit 1
fi

CONFIG=config.enceladus

## get the date 1 days ago
year=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = $before)).strftime(\"%Y\")))")
yr2=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = $before)).strftime(\"%y\")))")
doy=$(python3 -c "import datetime; print('{:}'.format((datetime.datetime.now()-datetime.timedelta(days = $before)).strftime(\"%j\")))")
idoy=$(echo $doy | sed 's/^0*//g') ## remove leading '0'

## we need to make an a-priori crd file for the BPE
python3 ${ABPE_DIR}/bin/make_apriori_crd.py -n croasp \
  -c ${ABPE_DIR}/config/config.enceladus \
  -o ${HOME}/tables/crd/REG${yr2}${doy}0.CRD \
  --ssc-files ${HOME}/tables/ssc/EPN_A_IGS14.SSC ${HOME}/tables/ssc/EPN_IGb14.SSC ${HOME}/tables/ssc/EPND_D2150_IGS14.SSC \
  --crd-files ${HOME}/tables/crd/NTUA52.CRD \
  --date "${year}-${doy}" \
  --date-format '%Y-%j' \
   || { echo "ERROR. Failed to create a-priori CRD file"; exit 1; }

## run the DD BPE ...
python3 ${ABPE_DIR}/bin/rundd.py \
  -c ${ABPE_DIR}/config/config.enceladus \
  -n croasp \
  -y ${year} \
  -d ${idoy} \
  --verbose \
  --use-euref-exclusion-list \
  --min-reference-stations 8 \
  --aprinf REG${yr2}${doy}0 \
  --download-max-tries 8 \
  --download-sleep-for 300 \
  --ts-file-name '${site_id}/${site_id}.cts_r' \
  || { echo "ERROR. BPE and/or rundd script failed!"; exit 1; }

rm ${HOME}/tables/crd/REG${yr2}${doy}0.CRD

exit 0