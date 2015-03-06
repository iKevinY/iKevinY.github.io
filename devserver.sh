#!/usr/bin/env bash
rootPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
developPath=${rootPath}/develop
port=8000

local_ip=$(ifconfig | grep 'inet ' | awk 'NR==2 {print $2}')
serve_msg="Serving HTTP at \e[1;37m${local_ip}:${port}\e[0m."

trap 'cd $rootPath && rm -r develop && kill 0' SIGINT
cd "$rootPath" && pelican -s pelicanconf.py > /dev/null # seed directory with site content

(pelican -rs pelicanconf.py) &
(cd "$developPath"; echo -e "$serve_msg"; python -m SimpleHTTPServer $port 1> /dev/null) &
wait
