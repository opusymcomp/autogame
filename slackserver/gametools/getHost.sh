#!/bin/bash

hst=$1
source ../config

# Errors depend on the timing, so we try n_trial times
n_trial=5

# check cpu
cpu_util=$(ssh $USER_NAME@$hst "awk '{s += \$1} END {print s}' <( ps -Ao pcpu --sort -pcpu | head -n 6 | tail -n 5 )")
if [ $cpu_util -gt 30 ];
then
  echo "0"
fi
echo "1"

# previous version
# return available host
<< COMMENTOUT
for hst in ${HOST_NAMES[@]};
do
	flag=0
	for (( i=0; i < $n_trial; i++ ));
	do
		# check cpu
		cpu_util=$(ssh $USER_NAME@$hst "awk '{s += \$1} END {print s}' <( ps -Ao pcpu --sort -pcpu | head -n 6 | tail -n 5 )")
		if [ $cpu_util -gt 30 ];
		then
			flag=1
			break
		fi

		# check command
		cmd_util=$(ssh $USER_NAME@$hst "ps -Ao command --sort -pcpu | head -n 6 | tail -n 5" )
		for cmd in ${cmd_util[@]};
		do
			# whether the host is already assigned or not
			if [[ ${cmd} == *rcssserver* ]] \
				   || [[ ${cmd} == *make* ]] \
				   || [[ ${cmd} == *gcc* ]] \
				   || [[ ${cmd} == *cc1plus* ]] \
				   || [[ ${cmd} == *bootstrap* ]] \
				   || [[ ${cmd} == *config* ]] \
				   || [[ ${cmd} == *auto* ]] \
				   || [[ ${cmd} == *python* ]] \
				   || [[ ${cmd} == *loganalyzer3* ]] \
				   || [[ ${cmd} == *ssh* ]] \
				   || [[ ${cmd} == *scp* ]] \
				   || [[ ${cmd} == *tar* ]] \
				   || [[ ${cmd} == *git* ]] \
				   || [[ ${cmd} == *rm* ]] \
				   || [[ ${cmd} == *bash* ]];
			then
				flag=1
				break
			fi
		done
		if [ $flag -eq 1 ];
		then
			break
		fi
	done
	if [ $flag -eq 1 ];
	then
		continue
	fi

	# # check user
	# user_util=(ssh $USER_NAME@$hst "ps -Ao user --sort -pcpu | head -n 31 | tail -n 30" )
	# for usr in ${user_util[@]};
	# do
	# 	if [[ ${usr} == *${USER_NAME}* ]];
	# 	then
	# 		flag=1
	# 		break
	# 	fi
	# done
	# if [ $flag -eq 1 ];
	# then
	# 	continue
	# fi

	# this host can be assigned
	echo ${hst}
	exit

done
echo "null"
COMMENTOUT