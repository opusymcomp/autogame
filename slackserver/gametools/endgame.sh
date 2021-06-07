#!/bin/bash
DIR=$1
HOST=$2
BRANCH=$3
GAMENUM=$4
OPP=$5

source ../config
cd `dirname $0`

# copy files from host to this pc
scp ${USER_NAME}@$HOST:${LOG_DIR}/game${GAMENUM}.* ../log/${DIR}

# add information to result.csv
cat ../log/${DIR}/game${GAMENUM}.csv | tail -n 1 | sed -e "s/[0-9]*,/game${GAMENUM},/" >> ../log/${DIR}/results.csv

# delete files in host
ssh ${USER_NAME}@$HOST "rm -r ${LOG_DIR}/game*; rmdir ${LOG_DIR}"
