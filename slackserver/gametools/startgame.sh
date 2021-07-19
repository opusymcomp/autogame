#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
DIR=$1
HOST=$2
BRANCH=$3
GAMENUM=$4
OPP=$5

source ../config
cd `dirname $0`

mkdir -p ../log/${DIR}
DATE=`date +%Y%m%d%0k%M`

cd ${LIBRCSC_DIR}
rsync -a --delete ./lib ${USER_NAME}@${HOST}:${LIBRCSC_DIR}

cd ${OUR_TEAM}
rsync -a --delete ./ ${USER_NAME}@${HOST}:${OUR_TEAM}

cd ${SCRIPT_DIR}
echo `dirname $0`
ssh ${USER_NAME}@${HOST} "cd ${HOST_AUTOGAME_DIR}/gameserver && ./autolog.sh $BRANCH $GAMENUM $OPP" &> ../log/${DIR}/game${GAMENUM}.log
wait

# return $HOST
echo $HOST
