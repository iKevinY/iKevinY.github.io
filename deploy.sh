#!/usr/bin/env bash
# Derived from http://zonca.github.io/2013/09/automatically-build-pelican-and-publish-to-github-pages.html

GH_PAGES_BRANCH=master
TARGET_REPO=iKevinY/iKevinY.github.io.git
OUTPUT_DIR=output
REMOTE_DIR=remote-site

if [ "$TRAVIS" == "true" ]; then
  echo "Deploying site to GitHub Pages via Travis CI."
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
else
  # If being run locally, Pelican needs to generate site files first
  rootPath="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  GH_TOKEN="git" # set GH_TOKEN variable to "git" for correct GITHUB_REPO URL
  cd "$rootPath"
  pelican -s publishconf.py
fi

# Pull hash and commit message of most recent commit
commitHash=$(git rev-parse HEAD)
commitMessage=$(git log -1 --pretty=%B)

# Clone the GitHub Pages branch and rsync it with the newly generated files
GITHUB_REPO=https://${GH_TOKEN}@github.com/$TARGET_REPO
git clone --branch=$GH_PAGES_BRANCH --depth 1 $GITHUB_REPO $REMOTE_DIR > /dev/null
rsync -r --exclude=.git --delete $OUTPUT_DIR/ $REMOTE_DIR/
pushd $REMOTE_DIR > /dev/null

# Add, commit, and push files to the GitHub Pages branch
git add -A
git status -s

if [ "$TRAVIS" == "true" ]; then
  longMessage="Generated by commit $commitHash; pushed by Travis build $TRAVIS_BUILD_NUMBER."
  git commit -m "$commitMessage" -m "$longMessage"
  git push -fq origin $GH_PAGES_BRANCH > /dev/null
else
  read -p "Manually push changes to GitHub Pages branch? [y/N] " response
  if [[ "$response" == 'y' ]] || [[ "$response" == 'Y' ]]; then
    git commit -m "$commitMessage" -m "Generated by commit $commitHash."
    git push -f origin $GH_PAGES_BRANCH
  fi

  popd > /dev/null
  rm -rf -- $REMOTE_DIR $OUTPUT_DIR && echo "Removed $REMOTE_DIR and $OUTPUT_DIR."
fi
