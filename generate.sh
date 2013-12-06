#!/bin/bash
cd ~/Sites/Kevin\ Yap
pelican -q -s settings.py

# Run file copying/deletion commands
cd ~/Sites/Kevin\ Yap/output
cp ../favicon.ico favicon.ico
cp ../robots.txt robots.txt
cp ../.htaccess .htaccess
cp ../CNAME CNAME
cp -R ../uploads/ uploads/
find . -name '*.DS_Store' -type f -delete || echo "Error deleting .DS_Store files."

printf "\e[0;32mSite generated successfully.\e[0m\n"

confirm() {
	read -n1 -p "$1" input
	printf "\n"

	case $input in
	  y|Y)
			return 0 ;;
	  n|N)
			return 1 ;;
	  *)
			printf "Unknown input. "
			confirm "$1" ;;
	esac
}

# Check for backup/upload options
if [ -z "$1" ]; then # no flag
	exit
elif [ $1 = "-p" ]; then
	python -m SimpleHTTPServer
fi
