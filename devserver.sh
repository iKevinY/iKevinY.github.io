#!/bin/bash

trap killgroup SIGINT
killgroup() {
	cd $rootPath && rm -rf develop && echo "Deleted develop directory successfully."
	kill 0
}

rootPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
developPath=${rootPath}/develop

cd $rootPath

# Local IP function: http://stackoverflow.com/a/13322549/239076
localIP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`

(pelican -rs pelicanconf.py) &
(sleep 2; cd $developPath; printf "Serving HTTP at \e[1;37m${localIP}:8000\e[0m.\n";
	python -m SimpleHTTPServer 8000 1>/dev/null) &
wait
