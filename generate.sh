#!/bin/bash
cd ~/Sites/Kevin\ Yap
pelican -s ./settings.py
cp favicon.ico output/favicon.ico && echo "favicon.ico successfully copied."
cp robots.txt output/robots.txt && echo "robots.txt successfully copied."
cp .htaccess output/.htaccess && echo ".htaccess successfully copied."
find . -name '*.DS_Store' -type f -delete && echo "Removed .DS_Store files."

printf "\e[0;32mSite generated successfully.\e[0m\n"

# If -u flag is used, upload output folder via rsync
if [ -z "$1" ]; then
	exit
elif [ $1 = "-u" ]; then
	echo "Beginning dry run of rsync."
	rsync -rnvc --delete -e "ssh -i $HOME/.ssh/id_rsa" ~/Sites/Kevin\ Yap/output/ keviny_kevinyap@ssh.phx.nearlyfreespeech.net:/home/public/

	printf "\e[0;36mConfirm upload via rsync (y/n): \e[0m"
	read confirm

	if [ $confirm == 'y' ]; then
		rsync -rc --delete -e "ssh -i $HOME/.ssh/id_rsa" ~/Sites/Kevin\ Yap/output/ keviny_kevinyap@ssh.phx.nearlyfreespeech.net:/home/public/
		printf "\e[0;32mOutput directory updated using rsync.\e[0m\n"
		exit
	else
		printf "\e[0;31mrsync terminated.\e[0m\n"
		exit
	fi
fi

# Note to self: update ~/.bash_profile file with 'alias generate="bash ~/Sites/Kevin\ Yap/generate.sh"'
