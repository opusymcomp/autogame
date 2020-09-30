#!/bin/bash

# ********************************************** #
# Please use this script after `auto_sshkey.sh`
# e.g. ./send_files_to_all_hosts.sh "/from" "/to"
# Note that you must use `sudo` with option `-S`
# ********************************************** #

source ./hostnames

read -sp "Host Password (if you use \"sudo -S\"): " pswd
echo ""

for i in "${hostnames_ids[@]}";
do
	hst=(${i[@]})
	echo "# --------------------------------------------- #"
	echo "send From:\"${1}\" To:\"${username}@${hst[0]}:${2}\""
	echo ${pswd}| scp -r "${1}" "${username}@${hst[0]}:${2}"
	echo ""
done
