#!/bin/bash

upload() {
	bash deploy.sh
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
	(sleep 2; cd $developPath; printf "Serving HTTP at \e[1;37m${localIP}:8000\e[0m.\n";
		python -m SimpleHTTPServer 8000 1>/dev/null) &
	wait
}

rootPath="$HOME/kevinyap.ca"
cd $rootPath

case $1 in
	"-d"|"-p")
		develop ;;
	"-u")
		upload ;;
	*)
		read -n1 -p "Development or upload site? [D/U] " input
		printf "\n"

		case $input in
			[dDpP])
				develop ;;
			[uU])
				upload ;;
			*)
				echo "Unknown input."
				exit 1
		esac
esac
