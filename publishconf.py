# Add & modify settings that are only applied upon publish
# (import settings that already exist in `pelicanconf.py`).
import sys, os
sys.path.append(os.getcwd())

from pelicanconf import *

SITEURL = 'http://kevinyap.ca'
RELATIVE_URLS = False
OUTPUT_PATH = 'output/'

GOOGLE_ANALYTICS = 'UA-41937659-1'
