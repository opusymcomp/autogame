#!/bin/bash

BRANCH=$1
GAMENUM=$2

cd $HOME/rcss/teamname/teamdir
git fetch
git checkout master
git branch | grep -vE '^\*|master$|develop$' | xargs -I % git branch -D %
git checkout -B $BRANCH $BRANCH
git pull
./bootstrap
./configure
make

#your team directory
TEAM_L='"$HOME/rcss/teamname/teamdir/src/start.sh"'

#opponent teams directory
TEAM_R_ARRAY=(
        '"$HOME/rcss/teams/fiftystorms/start.sh "'
        '"$HOME/rcss/teams/helios/start.sh "'
        '"$HOME/rcss/teams/hillstone/start.sh"'
		'"$HOME/rcss/teams/opuscom/start.sh "'
        '"$HOME/rcss/teams/rione/start.sh"'
		'"$HOME/rcss/teams/toyosugalaxy/start.sh "'
		'"$HOME/rcss/HELIOS/helios/src/start.sh "'
		'"$HOME/rcss/Gliders2d/G2d-1.6/src/start.sh"'
		'"$HOME/rcss/agent2d-3.1.1/src/start.sh"'
        '"$HOME/rcss/teams/jyosen/start.sh"')

LOGDIR="$HOME/rcss/log"

mkdir -p ${LOGDIR}
rm ${LOGDIR}/*

OPPLIST=3

echo "check : $BRANCH, $GAMENUM, $#"

# start loop
while [ $OPPLIST -le $# ] ; do
    OPP=${!OPPLIST}
    echo "opp : $OPP"
    TEAM_R=${TEAM_R_ARRAY[$OPP]}
    echo "$TEAM_R"
    SYNCH="true"
    count=0
    while [ $count -lt $GAMENUM ] ; do
		DATE=`date +%Y%m%d%0k%M`
		rcssserver server::auto_mode = 1 \
				   server::synch_mode = $SYNCH \
				   server::team_l_start = ${TEAM_L} server::team_r_start = ${TEAM_R} \
				   server::kick_off_wait = 50 \
				   server::half_time = 300 \
				   server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 \
				   server::penalty_shoot_outs = 0 \
				   server::game_logging = 1 server::text_logging = 1 \
				   server::game_log_dir = "${LOGDIR}" server::text_log_dir = "${LOGDIR}" \
				   server::game_log_compression = 1 \
				   server::text_log_compression = 1 \
				   2>&1 | tee ${LOGDIR}/${DATE}.log
		sleep 1

		#counting
		echo "${TEAM_R} : ${count} games finished."
		count=$(($count+1))
	done
	OPPLIST=$(($OPPLIST+1))
done

git fetch
git checkout master
git branch -D $BRANCH

sleep 1

cd ~/rcss/log/
loganalyzer3 ~/rcss/log/ --side l
