#!/bin/bash

# ********************************************** #
# Please use this script after `auto_sshkey.sh`
# e.g. ./get_files_from_all_hosts.sh "/from" "/to"
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
	echo "get From:\"${username}@${hst[0]}:${1}\" To:\"${2}\""
	echo ${pswd}| scp -r "${username}@${hst[0]}:${1}" "${2}"
	echo ""
done
