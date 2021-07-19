#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
BRANCH=$1

echo "start_branch_pull"
source ../config
cd ${LIBRCSC_DIR}/librcsc
git fetch && git checkout $BRANCH && git pull
./bootstrap
./configure --prefix=$LIBRCSC_DIR
make
make install

cd ${OUR_TEAM}
git fetch && git checkout $BRANCH && git pull
./bootstrap
./configure --with-librcsc=$LIBRCSC_DIR
make

cd ${SCRIPT_DIR}/../slackbot/plugins/

echo "finish_branch_pull"
