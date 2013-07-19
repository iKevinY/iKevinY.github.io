#!/bin/bash
cd ~/Sites/Kevin\ Yap
pelican -s ./settings.py
cp favicon.ico output/favicon.ico && echo "favicon.ico successfully copied."
cp robots.txt output/robots.txt && echo "robots.txt successfully copied."
cp .htaccess output/.htaccess && echo ".htaccess successfully copied."

# If -u flag is used, upload output folder via rsync
if [ -z "$1" ]; then
	echo -e "Site generated successfully."
	exit
elif [ $1 = "-u" ]; then
	echo "Site generated successfully."
	rsync -r --delete ~/Sites/Kevin\ Yap/output/ keviny_kevinyap@ssh.phx.nearlyfreespeech.net:/home/public/
	echo "Output directory updated using rsync."
fi

# Note to self: update ~/.bash_profile file with 'alias generate="bash ~/Sites/Kevin\ Yap/generate.sh"'
