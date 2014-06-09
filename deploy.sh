#!/usr/bin/env bash
# Derived from http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html

BRANCH=master
TARGET_REPO=iKevinY/iKevinY.github.io.git
PELICAN_OUTPUT_FOLDER=output

echo -e "Deploying site to GitHub Pages.\n"
if [ "$TRAVIS" == "true" ]; then
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis CI"
fi

# Clone and sync newly generated site files
git clone --quiet --branch=$BRANCH https://${GH_TOKEN}@github.com/$TARGET_REPO built_website > /dev/null
cd built_website
rsync -rv --exclude=.git  ../$PELICAN_OUTPUT_FOLDER/* .

# Add, commit, and push files
git add -f .
git commit -m "Travis build $TRAVIS_BUILD_NUMBER pushed to Github Pages"
git push -fq origin $BRANCH > /dev/null
echo -e "Deploy completed.\n"
