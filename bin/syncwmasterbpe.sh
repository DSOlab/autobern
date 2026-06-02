#!/bin/bash
## Remote folder R_????
## Local folder L_????

## Help Function
function help {
    echo " Usage  : ./syncwmasterbpe.sh --host xxx.xxx.xxx.xxx --user bpe54"
    exit 1
}

if [ "$#" -ne 4 ]
then
	echo "[ERROR] : No input argument"
	help
fi

while [ $# -eq 4 ]
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
    	*)
            echo "[ERROR] Wronk arguments"
	    help
	    exit 1
    esac
done



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

R_GEN="${USER}@${HOST}:/home/bpe54/data/GPSDATA/CAMPAIGN54/GREECE/GEN"
L_GEN="/home/bpe54/data/GPSDATA/CAMPAIGN54/GREECE/GEN"

rsync -a -z \
    --update \
    --partial \
    --append-verify \
    --human-readable \
    --progress \
    "$R_GEN" "$L_GEN"

