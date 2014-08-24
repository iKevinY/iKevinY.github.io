#!/usr/bin/env bash
rootPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
developPath=${rootPath}/develop
port=8000

# Local IP function: http://stackoverflow.com/a/13322549/239076
localIP=`ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p'`
serveMsg="Serving HTTP at \e[1;37m${localIP}:${port}\e[0m."

trap "cd $rootPath && rm -r develop && kill 0" SIGINT
cd $rootPath && pelican -s pelicanconf.py > /dev/null # seed directory with site content

(pelican -rs pelicanconf.py) &
(cd $developPath; echo -e $serveMsg; python -m SimpleHTTPServer $port 1> /dev/null) &
wait
