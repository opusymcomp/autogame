#!/bin/bash
ORDER=$1
IP=$2
BRANCH=$3
OPT=${@:3}

cd `dirname $0`

ssh username@$IP "cd rcss && ./autolog.sh $OPT"
wait

DIR=${ORDER}_${BRANCH}_${IP}

mkdir -p ../log/${DIR}
scp username@$IP:~/rcss/log/*.csv ../log/${DIR}
wait

python loganalyzerAve.py ${ORDER} ${BRANCH} ${DIR}
