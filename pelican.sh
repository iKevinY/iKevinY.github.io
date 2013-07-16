#!/bin/bash
cd ~/Sites/Kevin\ Yap
pelican -s ./settings.py
cp robots.txt output/robots.txt && echo "robots.txt successfully copied."
cp .htaccess output/.htaccess && echo ".htaccess successfully copied."
rm settings.pyc && echo "settings.pyc removed from main directory."