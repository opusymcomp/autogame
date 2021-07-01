#!/bin/bash

source ./hostnames

read -sp "Password: " pswd

echo ""
echo "# -------------------------------- #"
echo "  server"
echo "  install ssh..."
echo "# -------------------------------- #"
sudo apt-get install ssh openssh-server sshpass

echo "# -------------------------------- #"
echo "  clients"
echo "  add user and install ssh..."
echo "# -------------------------------- #"
for i in "${hostnames_ids[@]}";
do
	hst=(${i[@]})
	echo ${shared_username}@${network}${hst[1]}
	echo ${pswd} | sshpass -p ${pswd} ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password "${shared_username}@${network}${hst[1]}" "sudo -S adduser --disabled-password --gecos '' ${username}; echo ${username}:${pswd} | sudo -S chpasswd; sudo -S gpasswd -a ${username} sudo; sudo -S apt-get install ssh openssh-server;"
	sshpass -p ${pswd} ssh -t -o StrictHostKeyChecking=no -o PreferredAuthentications=password "${username}@${network}${hst[1]}" "mkdir .ssh"
done

echo "# -------------------------------- #"
echo "  server"
echo "  create keys..."
echo "# -------------------------------- #"
cd ~/.ssh/
for i in "${hostnames_ids[@]}";
do
	hst=(${i[@]})
	if [ -f ~/.ssh/id_rsa_${hst[0]} ]; then
		echo "Key authorization is already finished..."
		echo "skip ${hst[0]}"
		continue
	fi
	ssh-keygen -t rsa -f id_rsa_${hst[0]} -P ""
	sshpass -p ${pswd} scp -o PreferredAuthentications=password id_rsa_${hst[0]}.pub ${username}@${network}${hst[1]}:~/.ssh/id_rsa_${hst[0]}.pub
	{
		echo "Host ${hst[0]}"
		echo "  HostName ${network}${hst[1]}"
		echo "  User ${username}"
		echo "  IdentityFile ~/.ssh/id_rsa_${hst[0]}"
		echo "  ServerAliveInterval 60"
	} >> config
done

echo "# -------------------------------- #"
echo "  clients"
echo "  add autholized_keys..."
echo "# -------------------------------- #"
for i in "${hostnames_ids[@]}";
do
	hst=(${i[@]})
	if [ -f ~/.ssh/id_rsa_${hst[0]}.pub ]; then
		sshpass -p ${pswd} ssh -o StrictHostKeyChecking=no -o PreferredAuthentications=password "${username}@${network}${hst[1]}" "cd ~/.ssh/; cat id_rsa_${hst[0]}.pub >> authorized_keys; rm id_rsa_${hst[0]}.pub;"
	else
		echo "Key authorization is already finished..."
		echo "skip ${hst[0]}"
	fi

done
