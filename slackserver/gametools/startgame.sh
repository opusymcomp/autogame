#!/bin/bash
DIR=$1
HOST=$2
OUR=$3
GAMENUM=$4
OPP=$5
BRANCHFLAG=$6
SYNCHFLAG=$7

source ../config
cd `dirname $0`

mkdir -p ../log/${DIR}
DATE=`date +%Y%m%d%0k%M`

if "${BRANCHFLAG}"; then
  rsync -a --delete ${LIBRCSC_DIR}/lib ${USER_NAME}@${HOST}:${LIBRCSC_DIR}
  rsync -a --delete ${OUR_TEAM}/ ${USER_NAME}@${HOST}:${OUR_TEAM}
fi

ssh ${USER_NAME}@${HOST} "cd ${HOST_AUTOGAME_DIR}/gameserver && ./autolog.sh $OUR $GAMENUM $OPP $BRANCHFLAG $SYNCHFLAG" &> ../log/${DIR}/game${GAMENUM}.log
wait

# return $HOST
echo $HOST
