#!/bin/bash

upload() {
	# Pull hash and commit message of most recent commit
	cd $rootPath
	commitHash=`git rev-parse HEAD`
	commitMessage=`git log -1 --pretty=%B`

	pelican -s publishconf.py

	cd ${rootPath}/output
	find . -name '*.DS_Store' -type f -delete || echo "Error deleting .DS_Store files."

	printf "\e[0;32mSite generated successfully.\e[0m\n"

	git add -A
	git checkout master

	printf "Last commit: \e[1;37m$commitMessage\e[0m\n"
	read -p "Upload site files? [y/N] " response
	printf "\n"

	case $response in
	  [yY])
	    git commit -m "$commitMessage" -m "Generated by commit $commitHash"
    	git push
    	;;
	  *)
	    echo "Cancelling commit."
	    exit 1
	    ;;
	esac
}

develop() {
	# Determine local IP http://stackoverflow.com/a/13322549/239076
	localIP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
	developPath=${rootPath}/develop

	trap killgroup SIGINT
	killgroup() {
		cd $rootPath && rm -rf develop && echo "Deleted develop directory successfully."
		kill 0
	}

	(pelican -rs pelicanconf.py) &
	(sleep 2; cd $developPath; printf "Serving HTTP at \e[1;37m${localIP}:8000.\e[0m\n";
		python -m SimpleHTTPServer 8000 1>/dev/null) &
	wait
}

rootPath="$HOME/kevinyap.ca"
cd $rootPath

if [[ $1 = "-d" ]] || [[ $1 = "-p" ]]; then
	develop
elif [[ $1 = "-u" ]]; then
	upload
else
	read -n1 -p "Development or upload site? [D/U] " input
	printf "\n"

	case $input in
	  [dD]|[pP])
	    develop ;;
	  [uU])
	    upload ;;
	  *)
	    echo "Unknown input."
	    exit 1
	esac
fi
