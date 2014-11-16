"""Settings that are only applied when being published."""

import sys, os
sys.path.append(os.getcwd())

from pelicanconf import *

SITEURL = 'http://kevinyap.ca'
RELATIVE_URLS = False
OUTPUT_PATH = 'output/'

DISQUS_SITENAME = 'kevinyap'
GOOGLE_ANALYTICS = 'UA-41937659-1'
