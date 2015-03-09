#!/usr/bin/env bash

usage="Usage: $(basename "$0") (deploy | diff | serve)

Commands:
  deploy     Upload site to Github Pages
  diff       Compare locally generated site to remote site
  serve      Generate and host site locally"

TARGET_REPO=iKevinY/iKevinY.github.io
GH_PAGES_BRANCH=master
OUTPUT_DIR=output
REMOTE_DIR=remote-site
PORT=8000

rootPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
  'deploy'|'diff')
    # Based on http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html
    if [ "$TRAVIS" == "true" ]; then
      echo "Deploying site to $GH_PAGES_BRANCH branch of $TARGET_REPO."
      git config --global user.email "travis@travis-ci.org"
      git config --global user.name "Travis CI"
    else
      GH_TOKEN="git"
      cd "$rootPath"
      pelican -s publishconf.py
    fi

    # Pull hash and commit message of the most recent commit
    commitHash=$(git rev-parse HEAD)
    commitMessage=$(git log -1 --pretty=%B)

    # Clone the GitHub Pages branch and rsync it with the newly generated files
    GITHUB_REPO=https://${GH_TOKEN}@github.com/${TARGET_REPO}.git
    git clone --branch=$GH_PAGES_BRANCH --depth 1 $GITHUB_REPO $REMOTE_DIR
    rsync -r --exclude=.git --delete $OUTPUT_DIR/ $REMOTE_DIR/
    pushd $REMOTE_DIR > /dev/null

    git add -A
    git status -s

    if [ "$TRAVIS" == "true" ]; then
      longMessage="Generated by $commitHash; pushed by build #$TRAVIS_BUILD_NUMBER."
      git commit -m "$commitMessage" -m "$longMessage"
      git push -fq origin $GH_PAGES_BRANCH > /dev/null
    else
      if [ "$1" == "diff" ]; then
        git --no-pager diff --cached --color-words
      else
        read -p "Push changes to GitHub Pages? [y/N] " response
        if [[ "$response" =~ ^[Yy]$ ]]; then
          git commit -m "$commitMessage" -m "Generated by $commitHash."
          git push -f origin $GH_PAGES_BRANCH
        fi
      fi
      popd > /dev/null
      rm -rf -- $REMOTE_DIR $OUTPUT_DIR && echo "Removed $REMOTE_DIR and $OUTPUT_DIR."
    fi
    ;;

  'serve')
    developPath=${rootPath}/develop
    local_ip=$(ifconfig | grep 'inet ' | awk 'NR==2 {print $2}')
    serve_msg="Serving HTTP at \e[1;37m${local_ip}:${PORT}\e[0m."

    trap 'cd $rootPath && rm -r develop && kill 0' SIGINT
    cd "$rootPath" && pelican -s pelicanconf.py > /dev/null # seed directory with site content

    (pelican -rs pelicanconf.py) &
    (cd "$developPath"; echo -e "$serve_msg"; python -m SimpleHTTPServer $PORT 1> /dev/null) &
    wait
    ;;

  *)
    echo "$usage"
    exit 1
    ;;

esac
