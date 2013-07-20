#!/bin/bash
cd ~/Sites/Kevin\ Yap
pelican -s settings.py

# Run file copying/deletion commands
cp favicon.ico output/favicon.ico
cp robots.txt output/robots.txt
cp .htaccess output/.htaccess
find . -name '*.DS_Store' -type f -delete || echo "Error deleting .DS_Store files."

printf "\e[0;32mSite generated successfully.\e[0m\n"

function confirm {
	read -n1 -p "Confirm upload via rsync (y/n): " confirm
	printf "\n"
	case $confirm in
	  y|Y)
			rsync --recursive --checksum --delete ~/Sites/Kevin\ Yap/output/ keviny_kevinyap@ssh.phx.nearlyfreespeech.net:/home/public/
			printf "\e[0;32mOutput directory updated using rsync.\e[0m\n"
			exit ;;
	  n|N)
			printf "\e[0;31mrsync terminated.\e[0m\n"
			exit ;;
	  *)
			printf "Unknown input. "
			confirm ;;
	esac
}

# Check for options
if [ -z "$1" ]; then # no flag
	exit
elif [ $1 = "-b" ]; then # backup
	rsync -a ~/Sites/Kevin\ Yap/ /Volumes/PETITEKEY/Website\ Backup
	printf "\e[0;32mSite files backed up to PetiteKey.\e[0m\n"
	exit
elif [ $1 = "-u" ]; then # upload
	echo "Beginning dry run of rsync."
	rsync --recursive --dry-run --verbose --checksum --human-readable --delete ~/Sites/Kevin\ Yap/output/ keviny_kevinyap@ssh.phx.nearlyfreespeech.net:/home/public/
	confirm
fi
