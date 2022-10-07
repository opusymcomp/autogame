#!/bin/bash
SCRIPT_DIR=`pwd`
BRANCH=$1

source ../config
#cd ${LIBRCSC_DIR}/librcsc
#git fetch && git checkout $BRANCH && git pull
#./bootstrap
#./configure --prefix=$LIBRCSC_DIR
#make
#make install

cd ${OUR_TEAM}
git fetch && git checkout $BRANCH && git pull
./bootstrap
./configure --with-librcsc=$LIBRCSC_DIR
make

cd ${SCRIPT_DIR}
