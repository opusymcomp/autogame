#!/bin/bash

# ********************************************** #
# Please use this script after `auto_sshkey.sh`
# e.g. ./cmd_to_all_hosts.sh "cd rcss; sudo -S make install"
# Note that you must use `sudo` with option `-S`
# ********************************************** #

source ./hostnames

username="fukushima"
read -sp "Host Password (if you use \"sudo -S\"): " pswd
echo ""

for i in "${hostnames_ids[@]}";
do
	hst=(${i[@]})
	echo "# --------------------------------------------- #"
	echo "execute \"${@}\" at ${username}@${hst[0]}"
	echo ${pswd}| ssh "${username}@${hst[0]}" "${@}"
	echo ""
done
