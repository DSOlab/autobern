#!/bin/bash
## Remote folder R_????
## Local folder L_????

## Help Function
function help {
    echo " Usage  : ./syncwmasterbpe.sh --host xxx.xxx.xxx.xxx --user bpe54 --campaign CAMPAIGN_NAME"
    exit 1
}

if [ "$#" -ne 4 ]
then
	echo "[ERROR] : No input argument"
	help
fi

while [ $# -gt 4 ]
do
    case "$1" in
        --host)
            HOST=${2}
            shift 2
            ;;
        --user)
            USER=${2}
            shift 2
            ;;
        --campaign)
            CAMPAIGN=${2}
            shift 2
            ;;
        *)
            echo "[ERROR] Wrong arguments"
            help
            exit 1
            ;;
    esac
done

if [ -z "${HOST}" ] || [ -z "${USER}" ]; then
    echo "[ERROR] --host and --user are required"
    help
fi

R_TABLES="${USER}@${HOST}:/home/bpe54/tables/"
L_TABLES="/home/bpe54/tables/"

rsync -a -z \
    --update \
    --partial \
    --append-verify \
    --human-readable \
    --progress \
    "$R_TABLES" "$L_TABLES"

R_GPSU="${USER}@${HOST}:/home/bpe54/GPSUSER/"
L_GPSU="/home/bpe54/GPSUSER/"

rsync -a -z \
    --update \
    --partial \
    --append-verify \
    --human-readable \
    --progress \
    "$R_GPSU" "$L_GPSU"


if [ -n "${CAMPAIGN}" ]; then
    R_GEN="${USER}@${HOST}:/home/bpe54/data/GPSDATA/CAMPAIGN54/${CAMPAIGN}/GEN/"
    L_GEN="/home/bpe54/data/GPSDATA/CAMPAIGN54/${CAMPAIGN}/GEN/"

    rsync -a -z \
        --update \
        --partial \
        --append-verify \
        --human-readable \
        --progress \
        "$R_GEN" "$L_GEN"
else
    echo "[INFO] --campaign not provided; skipping GEN synchronization"
fi

