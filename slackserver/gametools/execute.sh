#!/bin/bash

function getOption(){
  ORDER=${1}
  OPT=`cat ../slackbot/order/${ORDER}.txt`
  echo ${OPT}
}

cd `dirname $0`

ORDER=${1}
IP=${2}
OPT=`getOption ${ORDER} | tr ',' ' '`
echo "OPTION: ${OPT}"
./startgame.sh ${ORDER} ${IP} ${OPT}
