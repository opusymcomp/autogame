#!/bin/bash
DIR=$1
HOST=$2
BRANCH=$3
GAMENUM=$4
OPP=$5

source ../config
cd `dirname $0`

mkdir -p ../log/${DIR}
DATE=`date +%Y%m%d%0k%M`

ssh ${USER_NAME}@${HOST} "cd ${HOST_AUTOGAME_DIR}/gameserver && ./autolog.sh $BRANCH $GAMENUM $OPP" &> ../log/${DIR}/game${GAMENUM}.log
wait

# return $HOST
echo $HOST
